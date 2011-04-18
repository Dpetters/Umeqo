"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""

from django.contrib import admin
from models import Question, Topic
            
class TopicAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'sort_order', 'audience')
    list_filter = ['audience']
    search_fields = ['name']
    
class QuestionAdmin(admin.ModelAdmin):
    fields= ['audience', 'status', 'sort_order', 'question', 'answer', 'slug']
    prepopulated_fields = {'slug':('question',)}
    list_display = ['question', 'topic', 'audience', 'sort_order', 'created_by', 'created_on', 'updated_by', 'updated_on', 'status']
    list_filter = ['topic', 'audience', 'status']
    search_fields = ['question', 'answer']
    
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
