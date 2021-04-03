from contextvars import ContextVar

from configs.configs import ApplicationConfigs
from transport.configure_app import configure_app


def main():
    database_context = ContextVar('database')

    app = configure_app(database_context)

    app.run(
        host=ApplicationConfigs.sanic.host,
        port=ApplicationConfigs.sanic.port,
        workers=ApplicationConfigs.sanic.workers,
        debug=ApplicationConfigs.sanic.debug,
    )


if __name__ == '__main__':
    main()
