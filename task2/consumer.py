import pika
import time
from bson import ObjectId
from models import Contact

def send_email_stub(contact: Contact):
    """Функція-заглушка для імітації відправлення email"""
    print(f"Sending email to {contact.email}...")
    time.sleep(1)  # імітація затримки
    print(f"Email sent to {contact.email}")

def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=ObjectId(contact_id)).first()
    if contact:
        send_email_stub(contact)
        contact.update(set__message_sent=True)
        print(f"Updated contact {contact.full_name}: message_sent=True")
    else:
        print(f"Contact with id {contact_id} not found")

    # Підтвердження обробки повідомлення
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # Підключення до RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Гарантуємо наявність черги
    channel.queue_declare(queue='email_queue')

    # Споживач слухає чергу
    channel.basic_consume(queue='email_queue', on_message_callback=callback)

    print("Waiting for messages. Press Ctrl+C to exit.")
    channel.start_consuming()

if __name__ == "__main__":
    main()
