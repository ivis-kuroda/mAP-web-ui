from celery import Celery, Task
from flask import Flask

from ext import MapWebUI


def create_app(config_object="config.config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    celery_init_app(app)
    _map_web_ui = MapWebUI(app)

    @app.route("/")
    def home():
        return "Welcome to the mAP Web UI!"

    return app


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
