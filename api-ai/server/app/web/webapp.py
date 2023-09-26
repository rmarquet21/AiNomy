from flask import Flask

from server.app import injector
from server.app.injector import configure_global_injector


def create_app():
    configure_global_injector()

    _injector = injector.get_injector()
    app = _injector.get(Flask)

    return app


if __name__ == "__main__":
    create_app().run(port=4000, processes=1, debug=True, threaded=False)
