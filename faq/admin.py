"""
 OpenSource
"""

from django.contrib import admin
from models import Question, Topic
            
class TopicAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug':('name',)}

    
class QuestionAdmin(admin.ModelAdmin):
  
    list_display = ['text', 'sort_order', 'created_by', 'created_on', 'updated_by', 'updated_on', 'status']

    def save_model(self, request, obj, form, change): #@UnusedVariable
        '''
        Overrided because I want to also set who created this instance.
        '''
        instance = form.save( commit=False )
        if instance.id is None:
            instance.created_by = request.user
                
        instance.updated_by = request.user
        instance.save()
        
        return instance

admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)
