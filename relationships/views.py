from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.db import models

Relationship = models.get_model('relationships', 'Relationship')
RelationshipType = models.get_model('relationships', 'RelationshipType')

@login_required
def toggle_relationship_ajax(request, content_type_id, object_id, relationship_type_slug):
    """ View that toggles the status of a relationship, for AJAX requests. """
    if request.is_ajax():
        content_type = get_object_or_404(ContentType, id=content_type_id)
        relationship_object = get_object_or_404(content_type.model_class(), pk=object_id)
        relationship_type = RelationshipType.objects.get(slug=relationship_type_slug)
        relationship, created = Relationship.objects.get_or_create(type=relationship_type, user=request.user, content_type=content_type, object_id=relationship_object.id)
        context = {'valid': True, 'created' : created}
        return HttpResponse(simplejson.dumps(context), mimetype="application/json")
    return redirect('home')
                            
