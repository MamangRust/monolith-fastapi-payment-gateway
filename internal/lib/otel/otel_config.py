from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor


class OpenTelemetryManager:
    def __init__(self, service_name: str, endpoint: str = "http://localhost:4317"):
        self.tracer_provider = TracerProvider(
            resource=Resource.create({"service.name": service_name})
        )
        trace.set_tracer_provider(self.tracer_provider)
        otlp_exporter = OTLPSpanExporter(endpoint=endpoint, insecure=True)
        span_processor = BatchSpanProcessor(otlp_exporter)
        self.tracer_provider.add_span_processor(span_processor)
        self.tracer = trace.get_tracer(service_name)

    def start_trace(self, span_name: str):
        return self.tracer.start_as_current_span(span_name)