from mongoengine import Document, StringField, EmailField, BooleanField, connect

# Підключення до MongoDB
connect(db="email_service", host="localhost", port=27017)


class Contact(Document):
    full_name = StringField(required=True)
    email = EmailField(required=True)
    message_sent = BooleanField(default=False)
    phone = StringField()
    company = StringField()

    def __str__(self):
        return f"{self.full_name} ({self.email})"
