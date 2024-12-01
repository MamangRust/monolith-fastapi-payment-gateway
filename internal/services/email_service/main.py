from internal.services.email_service.service import EmailService

from internal.lib.kafka.kafka_config import KafkaManager 
from internal.lib.otel.otel_config import OpenTelemetryManager
from internal.lib.config.main import get_app_settings
from prometheus_client import start_http_server

import asyncio

async def main():   
    settings = get_app_settings()

    kafka_manager = KafkaManager(bootstrap_servers="kafka:9092")
    otel_manager = OpenTelemetryManager(service_name="email-service", endpoint="http://jaeger:4317")

    email_service = EmailService(
        kafka_manager=kafka_manager,
        smtp_server="smtp.ethereal.email",
        smtp_port=587,
        smtp_user=settings.smtp_user,
        smtp_password=settings.smtp_password,
        otel_manager=otel_manager
    )

    start_http_server(8007)  

    await email_service.start()





if __name__ == "__main__":
    asyncio.run(main())