from django.db import models
from datetime import time, UTC

from global_use.serializers import django_model_to_json


class Interviewer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    start_time = models.TimeField(default=time(hour=9))
    end_time = models.TimeField(default=time(hour=17))
    timezone = models.CharField(max_length=50, default='UTC')


class InterviewTemplate(models.Model):
    interviewId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    durationMinutes = models.IntegerField()
    interviewers = models.ManyToManyField('Interviewer')

    @classmethod
    def get_json_by_id(cls, _id:int) -> dict:
        """
        Gets the json representation of the interview
        :param _id: interviewId of InterviewTemplate
        :returns: json object of InterviewTemplate
        """
        interview = InterviewTemplate.objects.get(interviewId=_id)
        return django_model_to_json(interview)
