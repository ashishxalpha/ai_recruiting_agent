from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

def setup_tracing(service_name: str = "ai-recruiting-backend") -> None:
    """Initialize OpenTelemetry tracing."""
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    
    # For Sprint 2, we just log traces to console.
    # Future sprints will add OTLP exporters (e.g. Jaeger)
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    
    trace.set_tracer_provider(provider)

def get_tracer(module_name: str) -> trace.Tracer:
    return trace.get_tracer(module_name)
