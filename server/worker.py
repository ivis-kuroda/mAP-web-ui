from typing import TYPE_CHECKING

from factory import create_app

if TYPE_CHECKING:
    from celery import Celery

flask_app = create_app()
celery_app: Celery = flask_app.extensions["celery"]
