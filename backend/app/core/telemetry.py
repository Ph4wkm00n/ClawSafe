"""Telemetry — OpenTelemetry trace context propagation."""

from __future__ import annotations

import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


def setup_telemetry(app) -> None:  # noqa: ANN001
    """Configure OpenTelemetry tracing if enabled."""
    if not settings.otel_enabled:
        logger.info("OpenTelemetry disabled (set CLAWSAFE_OTEL_ENABLED=true to enable)")
        return

    try:
        from opentelemetry import trace
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import (
            ConsoleSpanExporter,
            SimpleSpanProcessor,
        )

        resource = Resource.create({
            "service.name": "clawsafe-backend",
            "service.version": settings.version,
        })

        provider = TracerProvider(resource=resource)

        if settings.otel_endpoint:
            try:
                from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                    OTLPSpanExporter,
                )
                exporter = OTLPSpanExporter(endpoint=settings.otel_endpoint)
                provider.add_span_processor(SimpleSpanProcessor(exporter))
                logger.info("OTEL OTLP exporter configured: %s", settings.otel_endpoint)
            except ImportError:
                logger.warning("OTLP exporter not available, falling back to console")
                provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
        else:
            provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

        trace.set_tracer_provider(provider)

        try:
            from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
            FastAPIInstrumentor.instrument_app(app)
            logger.info("OpenTelemetry FastAPI instrumentation enabled")
        except ImportError:
            logger.warning("FastAPI OTEL instrumentation not available")

    except ImportError:
        logger.warning("OpenTelemetry SDK not installed, skipping telemetry setup")
