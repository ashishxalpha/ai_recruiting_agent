from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource

def setup_metrics(service_name: str = "ai-recruiting-backend") -> None:
    """Initialize OpenTelemetry metrics."""
    resource = Resource.create({"service.name": service_name})
    provider = MeterProvider(resource=resource)
    
    # Note: Adding metric exporters (like Prometheus) is deferred to future sprints.
    metrics.set_meter_provider(provider)

def get_meter(module_name: str) -> metrics.Meter:
    return metrics.get_meter(module_name)
