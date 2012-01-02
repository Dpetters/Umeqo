from django.core.management.base import CommandError
from django.db.models import AutoField

def parse_apps_and_models(label):
    apps_and_models = []
    for chunk in label.split():
        try:
            app, model = chunk.split('.', 1)
        except ValueError:
            raise CommandError("Invalid arguments: %s" % label)
        apps_and_models.append((app, model))
    return apps_and_models

def get_model_cls(appname, modelname):
    from django.db.models import get_model
    try:
        model = get_model(appname, modelname)
    except Exception, e:
        raise CommandError("%s occurred: %s" %
                (e.__class__.__name__, e))
    if not model:
        raise CommandError("Unknown model: %s.%s" %
                (appname, modelname))
    else:
        return model
    
def copy_model_instance(obj):
    initial = dict([(f.name, getattr(obj, f.name)) for f in obj._meta.fields if not isinstance(f, AutoField) and not f in obj._meta.parents.values()])
    return obj.__class__(**initial)