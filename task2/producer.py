import pika
from faker import Faker
from models import Contact

fake = Faker()

def main():
    # Підключення до RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Створюємо чергу
    channel.queue_declare(queue='email_queue')

    # Генеруємо фейкові контакти
    for _ in range(10):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            company=fake.company()
        ).save()
        # Відправляємо ObjectID контакту у чергу
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=str(contact.id)
        )
        print(f"Contact {contact.full_name} added to queue")

    connection.close()

if __name__ == "__main__":
    main()
