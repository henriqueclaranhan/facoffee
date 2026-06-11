import os
import pika
import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class RabbitMQPublisher:
    def __init__(self):
        self.rabbitmq_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            params = pika.URLParameters(self.rabbitmq_url)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            # Declare exchange
            self.channel.exchange_declare(exchange='facoffee.events', exchange_type='topic', durable=True)
            logger.info("Connected to RabbitMQ successfully")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            self.connection = None
            self.channel = None

    def publish(self, routing_key: str, message: Dict[str, Any]):
        if not self.connection or self.connection.is_closed:
            self.connect()

        if self.channel:
            try:
                self.channel.basic_publish(
                    exchange='facoffee.events',
                    routing_key=routing_key,
                    body=json.dumps(message).encode('utf-8'),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # make message persistent
                        content_type='application/json'
                    )
                )
                logger.info(f"Message published to {routing_key}: {message.get('eventId')}")
            except Exception as e:
                logger.error(f"Failed to publish message: {e}")
                self.connection = None
        else:
            logger.error("Channel not initialized, message not sent")

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

rabbitmq_publisher = RabbitMQPublisher()
