from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.forms import model_to_dict
import json

class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, models.Model):
            return model_to_dict(obj)
        return super().default(obj)
    
def django_model_to_json(model: models.Model):
    return json.loads(json.dumps(model, cls=ExtendedEncoder))
