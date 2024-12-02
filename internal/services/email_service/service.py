import json
import smtplib
from email.mime.text import MIMEText
from aiokafka import AIOKafkaConsumer
from prometheus_client import Counter, Summary, Histogram

class EmailService:
    def __init__(self, kafka_manager, smtp_server, smtp_port, smtp_user, smtp_password, otel_manager):
        self.kafka_manager = kafka_manager
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.otel_manager = otel_manager

        # Prometheus metrics
        self.email_processed_count = Counter('email_processed_count', 'Total number of emails processed')
        self.email_send_duration = Histogram('email_send_duration', 'Duration of sending emails', buckets=(0.1, 0.5, 1, 2, 5))
        self.email_send_failure_count = Counter('email_send_failure_count', 'Total number of failed email sends')

    async def start(self):
        """Start consuming messages from multiple topics."""
        consumer = await self.kafka_manager.get_consumer(
            topic=["email-service-topic-saldo", "email-service-topic-topup", "email-service-topic-transfer"],
            group_id="email-service-group",
        )
        try:
            async for msg in consumer:
                topic = msg.topic
                message = json.loads(msg.value.decode("utf-8"))
                with self.otel_manager.start_trace(f"Process Kafka Message: {topic}"):
                    await self.process_message(topic, message)
        finally:
            await consumer.stop()

    async def process_message(self, topic, message):
        """Process messages from different topics."""
        try:
            with self.otel_manager.start_trace(f"Handle Topic: {topic}"):
                if topic == "email-service-topic-saldo":
                    await self.handle_saldo_email(message)
                elif topic == "email-service-topic-topup":
                    await self.handle_topup_email(message)
                elif topic == "email-service-topic-transfer":
                    await self.handle_transfer_email(message)
        except Exception as e:
            print(f"Failed to process message from topic {topic}: {e}")

    async def handle_saldo_email(self, message):
        """Handle email notification for saldo creation."""
        email = message.get("email")
        subject = "Saldo Created Successfully"
        body = message.get("body", "Your saldo has been successfully created.")
        with self.otel_manager.start_trace("Send Saldo Email"):
            await self.send_email(email, subject, body)

    async def handle_topup_email(self, message):
        """Handle email notification for topup."""
        email = message.get("email")
        subject = "Topup Successful"
        body = message.get("body", "Your topup has been successfully processed.")
        with self.otel_manager.start_trace("Send Topup Email"):
            await self.send_email(email, subject, body)

    async def handle_transfer_email(self, message):
        """Handle email notification for transfer."""
        sender_email = message.get("sender_email")
        receiver_email = message.get("receiver_email")
        subject = message.get("subject")
        body = message.get("body")
        if sender_email:
            with self.otel_manager.start_trace("Send Transfer Email - Sender"):
                await self.send_email(sender_email, subject, body)
        if receiver_email:
            with self.otel_manager.start_trace("Send Transfer Email - Receiver"):
                await self.send_email(receiver_email, subject, body)

    async def send_email(self, to_email, subject, body):
        """Send email using SMTP."""
        if not to_email:
            print("Email address is missing, skipping.")
            return
        try:
            with self.email_send_duration.time():  # Measure the duration of sending the email
                with self.otel_manager.start_trace("SMTP Email Send"):
                    msg = MIMEText(body)
                    msg["Subject"] = subject
                    msg["From"] = self.smtp_user
                    msg["To"] = to_email

                    with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                        server.starttls()
                        server.login(self.smtp_user, self.smtp_password)
                        server.sendmail(self.smtp_user, to_email, msg.as_string())
                    print(f"Email sent to {to_email}")
                    self.email_processed_count.inc()  # Increment the counter for successfully processed emails
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")
            self.email_send_failure_count.inc()  # Increment the counter for failed email sends
