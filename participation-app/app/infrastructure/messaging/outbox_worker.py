import asyncio
import traceback
import json
from app.infrastructure.database.database import SessionLocal
from app.infrastructure.database.repositories.sqlalchemy_outbox_repository import SQLAlchemyOutboxRepository
from app.infrastructure.messaging.rabbitmq_publisher import rabbitmq_publisher

async def process_outbox_events():
    while True:
        try:
            db = SessionLocal()
            try:
                outbox_repo = SQLAlchemyOutboxRepository(db)
                events = outbox_repo.find_pending(limit=50)
                
                for event in events:
                    try:
                        payload = json.loads(event.payload)
                        rabbitmq_publisher.publish(event.event_type, payload)
                        event.status = "PROCESSED"
                        outbox_repo.save(event)
                    except Exception as e:
                        print(f"Error publishing event {event.id}: {e}")
                        
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error in outbox worker db loop: {e}")
            finally:
                db.close()
                
        except Exception as e:
            traceback.print_exc()
            
        await asyncio.sleep(5)
