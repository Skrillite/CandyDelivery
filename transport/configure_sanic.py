from sanic import Sanic
from contextvars import ContextVar

from .routes import get_routes
from hooks import init_db_posgresql
from .exception_handlers import get_exc_handlers


def configure_app(database_context: ContextVar) -> Sanic:
    app = Sanic(__name__)

    app.config.FALLBACK_ERROR_FORMAT = "json"

    init_db_posgresql(database_context)

    for handler in get_exc_handlers():
        app.error_handler.add(handler.exception, handler.handler)

    for handler in get_routes(database_context):
        app.add_route(
            handler=handler,
            uri=handler.uri,
            methods=handler.methods,
            strict_slashes=True
        )

    return app
