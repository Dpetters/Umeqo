from django.contrib import admin
from notification.models import NoticeType, NoticeSetting, Notice, ObservedItem, NoticeQueueBatch

class NoticeTypeAdmin(admin.ModelAdmin):
    list_display = ('label', 'display', 'description', 'default')

class NoticeSettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'notice_type', 'medium', 'send')

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('message', 'message_full', 'recipient', 'sender', 'notice_type', 'added', 'unseen', 'archived')
    search_fields = ['message', 'message_full']
admin.site.register(NoticeQueueBatch)
admin.site.register(NoticeType, NoticeTypeAdmin)
admin.site.register(NoticeSetting, NoticeSettingAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(ObservedItem)
