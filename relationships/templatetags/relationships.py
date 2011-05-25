from django.template import Library
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

register = Library()

Relationship = models.get_model('relationships', 'Relationship')
RelationshipType = models.get_model('core', 'RelationshipType')

@register.simple_tag
def get_toggle_relationship_url(object, relationship_type_slug="favorite"):
    """
    Given an object, returns the URL for "toggle favorite for this item".
    Optionally takes a second argument, which is the slug of a 
    FaveType object. If this is provided, will return the URL for
    that FaveType. If not, will use the first FaveType (which, by
    default, is "Favorite".)
    
    Example usage:
    
    {% load faves %}
    <p><a href="{% get_toggle_fave_url photo favorite %}">{% if request.user|has_faved:photo %}Unfavorite{% else %}Favorite{% endif %} this photo</a></p>
    
    """
    print "WHAOOO"
    relationship_type = RelationshipType.objects.get(slug=relationship_type_slug)
    content_type = ContentType.objects.get(app_label=object._meta.app_label, model=object._meta.module_name)
    return reverse('toggle_relationship', args=(relationship_type.slug, content_type.id, object.id))
