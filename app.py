import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from api.routes import api_router, api_router_v2
from fastapi_sqlalchemy import DBSessionMiddleware
from config import ConfigClass, SRV_NAMESPACE
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

app = FastAPI(
    title="Dataops Service",
    description="Dataops",
    docs_url="/v1/api-doc",
    version="0.3.0"
)
app.add_middleware(DBSessionMiddleware, db_url=ConfigClass.SQLALCHEMY_DATABASE_URI)
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

app.include_router(api_router, prefix="/v1")
app.include_router(api_router_v2, prefix="/v2")

def instrument_app(app) -> None:
    """Instrument the application with OpenTelemetry tracing."""

    tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: SRV_NAMESPACE}))
    trace.set_tracer_provider(tracer_provider)

    jaeger_exporter = JaegerExporter(
        agent_host_name='127.0.0.1', agent_port=6831
    )

    tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()
    LoggingInstrumentor().instrument()

if ConfigClass.opentelemetry_enabled:
    print("Opentelemetry activated")
    instrument_app(app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5063, log_level="info")
