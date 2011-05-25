from django.db import models, connection
from django.contrib.contenttypes.models import ContentType

qn = connection.ops.quote_name

class RelationshipManagerMixin(object):
    """ A Mixin to add a `favorite__favorite` column via extra 
    """
    def with_relationship_for(self, user, type, all=True):
        """ Adds a column favorite__favorite to the returned object, which
        indicates whether or not this item is a favorite for a user
        """
        
        if user.is_authenticated():
            
            Relationship = models.get_model('relationships', 'Relationship')
            
            content_type = ContentType.objects.get_for_model(self.model)
            
            pk_field = "%s.%s" % (qn(self.model._meta.db_table),
                                  qn(self.model._meta.pk.column))

            relationship_sql = """(SELECT 1 FROM %(favorites_db_table)s 
    WHERE %(favorites_db_table)s.object_id = %(pk_field)s and
          %(favorites_db_table)s.content_type_id = %(content_type)d and
          %(favorites_db_table)s.user_id = %(user_id)d)
    """ % {'pk_field': pk_field, \
               'db_table': qn(self.model._meta.db_table), \
               'favorites_db_table': qn(Relationship._meta.db_table), \
               'user_id': user.pk, \
               'content_type': content_type.id, \
               'type' : type.id, \
               }

            extras = {
                'select': {'relationship': relationship_sql},
                }
            
            if not all:
                extras['where'] = ['relationship__relationship == 1']

        else:
            if not all:
                return self.get_query_set().none()
            else:
                extras = {
                    'select': {'relationship__relationship': '(SELECT 0)'}
                }

        return self.get_query_set().extra(**extras)

class RelationshipManager(models.Manager, RelationshipManagerMixin):
    @classmethod
    def create_relationship(cls, *args, **kwargs):
        print args
        print kwargs
        content_type = ContentType.objects.get_for_model(type(kwargs['content_object']))
        Relationship = models.get_model('relationships', 'Relationship')
        relationship = Relationship(
            user=kwargs['user'],
            content_type=content_type,
            type = kwargs['type'],
            object_id=kwargs['content_object'].pk,
            content_object=kwargs['content_object']
            )
        relationship.save()
        return relationship