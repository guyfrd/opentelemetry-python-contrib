import logging  # pylint: disable=import-self
import os
from typing import Collection

from opentelemetry.instrumentation.instrumentor import BaseInstrumentor

import wrapt

from opentelemetry import context
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.instrumentation.os.package import _instruments
from opentelemetry.instrumentation.os.version import __version__
from opentelemetry.instrumentation.utils import unwrap

from opentelemetry.trace import Span, SpanKind, Tracer, get_tracer, get_tracer_provider

def _instrument(
    tracer: Tracer
):
    def instrumented_os(wrapped, instance, args, kwargs):
         with tracer.start_as_current_span(
            "os", kind=SpanKind.CLIENT
        ) as span:
            span.set_attribute("command", args[0])
            response = wrapped(*args, **kwargs)
         
    wrapt.wrap_function_wrapper(
        __name__,
        "os.system",
        instrumented_os,
    )
class OsInstrumentor(BaseInstrumentor): 

    def instrumentation_dependencies(self) -> Collection[str]:
        return _instruments
    
    def _instrument(self, **kwargs):
        tracer_provider = get_tracer_provider()
        tracer = get_tracer(__name__, __version__, tracer_provider)
        _instrument(
            tracer
        )
            
    def _uninstrument():
        unwrap(__name__, "os.system")
