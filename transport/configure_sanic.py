from sanic import Sanic
from contextvars import ContextVar

from transport.routes import get_routes
from hooks import init_db_posgresql


def configure_app(database_context: ContextVar) -> Sanic:
    app = Sanic(__name__)

    init_db_posgresql(database_context)

    for handler in get_routes(database_context):
        app.add_route(
            handler=handler,
            uri=handler.uri,
            methods=handler.methods,
            strict_slashes=True
        )

    return app
