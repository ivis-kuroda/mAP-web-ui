#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Factory for creating and configuring the Flask application."""

import os

from celery import Celery, Task
from flask import Flask

from server.config import setup_config
from server.const import DEFAULT_CONFIG_PATH


def create_app(import_name: str) -> Flask:
    """Factory function to create and configure the Flask application.

    Args:
        import_name (str): The name of the application package.

    Returns:
        Flask: The configured Flask application instance.

    """
    app = Flask(import_name)
    config = setup_config(DEFAULT_CONFIG_PATH)
    app.config.from_object(config)
    app.config.from_prefixed_env()
    celery_init_app(app)

    return app


def celery_init_app(app: Flask) -> Celery:
    """Initialize and configure a Celery application with the Flask app context.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        Celery: The configured Celery application instance.
    """

    class FlaskTask(Task):
        """Task with Flask application context."""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app

    return celery_app
