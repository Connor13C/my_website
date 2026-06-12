import os

from celery import Celery
from fastapi import FastAPI

from users import urls

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(urls.router, prefix="/users")


    @app.get("/")
    async def root():
        return {"message": "Hello World"}


    @app.get("/hello/{name}")
    async def say_hello(name: str):
        return {"message": f"Hello {name}"}

    return app

def create_celery():
    """Configures and creates celery application to run background tasks with the same abilities as the flask
    application but allows asynchronous tasks to be run during in background."""
    # app = create_app()
    celery = Celery(
        'worker',
        backend=os.environ.get('CELERY_RESULT_BACKEND'),
        broker=os.environ.get('CELERY_BROKER_URL')
    )
    # celery.conf.update(app.config)
    #
    # class ContextTask(celery.Task):
    #     def __call__(self, *args, **kwargs):
    #         with app.app_context():
    #             return self.run(*args, **kwargs)
    #
    # celery.Task = ContextTask
    celery_task_dirs = ['users']
    celery.autodiscover_tasks(celery_task_dirs)
    return celery
