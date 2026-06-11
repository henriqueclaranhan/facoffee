import pika
import json
import threading
import logging
import os
from datetime import datetime

from app.infrastructure.database.database import SessionLocal
from app.infrastructure.database.repositories.sqlalchemy_participation_repository import SQLAlchemyParticipationRepository
from app.application.use_cases.cancel_participation import CancelParticipationUseCase
from app.application.dtos.participation import CancelParticipationRequest
from app.domain.exceptions.participation import ParticipationNotFoundException

logger = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "facoffee")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "facoffee")


def process_user_deactivated(ch, method, properties, body):
    logger.info(f"Received message: {body}")
    try:
        data = json.loads(body)

        # eventId, eventType, occurredAt, version, payload
        event_type = data.get("eventType")
        if event_type != "UserDeactivated":
            logger.warning(f"Ignorando evento desconhecido: {event_type}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        payload = data.get("payload", {})
        user_id = payload.get("userId")

        if not user_id:
            logger.warning("Evento UserDeactivated recebido sem userId.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        logger.info(f"Processando desativação para o usuário: {user_id}")

        # busca participação ativa e cancelar
        db = SessionLocal()
        try:
            repo = SQLAlchemyParticipationRepository(db)
            participation = repo.find_active_by_user(user_id)

            if participation:
                logger.info(f"Cancelando participação {participation.id} do usuário {user_id}")
                use_case = CancelParticipationUseCase(repo)

                current_cycle = datetime.utcnow().strftime("%Y-%m")
                request = CancelParticipationRequest(effectiveCycle=current_cycle)

                use_case.execute(participation.id, request)
                db.commit()
                logger.info(f"Participação {participation.id} cancelada com sucesso.")
            else:
                logger.info(f"Nenhuma participação ativa encontrada para o usuário {user_id}.")

        except Exception as db_exc:
            db.rollback()
            logger.error(f"Erro no banco ao cancelar participação: {db_exc}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            return
        finally:
            db.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logger.error(f"Erro ao processar mensagem do RabbitMQ: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_rabbitmq_consumer():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300
    )

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        queue_name = "participation.user-deactivated"

        channel.queue_declare(queue=queue_name, durable=True, arguments={"x-consumer-timeout": 300000})

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=process_user_deactivated)

        logger.info(f"RabbitMQ consumer iniciado na fila: {queue_name}")
        channel.start_consuming()
    except Exception as e:
        logger.error(f"Falha ao iniciar RabbitMQ consumer: {e}")


def run_consumer_in_background():
    thread = threading.Thread(target=start_rabbitmq_consumer, daemon=True)
    thread.start()
    return thread
