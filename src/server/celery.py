#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Celery application for background task processing."""

import typing as t

from .factory import create_app

if t.TYPE_CHECKING:
    from celery import Celery

flask_app = create_app(__name__)
celery_app: Celery = flask_app.extensions["celery"]
