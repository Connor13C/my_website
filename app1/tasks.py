import os
import re
from celery import chain
from celery.schedules import crontab

from app import create_celery
from models.db import ProjectModel, CommentModel
from input_handling import sanitize_input


celery = create_celery()


@celery.on_after_finalize.connect
def app_ready(**kwargs):
    """Sets up a task to run everyday automatically."""
    app_started()
    sender = kwargs.get('sender')
    sender.add_periodic_task(crontab(hour=10), run_all.s())


@celery.task(autoretry_for=(Exception,), time_limit=60)
def app_started():
    """Do something when application comes online"""
    pass


@celery.task
def run_all(user='system_startup'):
    """Sequential tasks run on startup and can be run by a user."""
    chain(task_1.s(user=user),
          task_2.s()).delay()


@celery.task(autoretry_for=(Exception,), time_limit=60)
def task_1(user):
    """Celery task 1"""
    return user


@celery.task(autoretry_for=(Exception,), time_limit=1800)
def task_2(user):
    """Celery task 2"""
    return user
