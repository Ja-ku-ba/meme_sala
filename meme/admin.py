from django.contrib import admin

from . import models
# Register your models here.

class SettingAdminPost(admin.ModelAdmin):
    list_display = ('owner', 'title'[:25], 'interactions', 'added')

class SettingAdminComent(admin.ModelAdmin):
    list_display = ('post', 'owner', 'body'[:25])

class SettingAdminInteractions(admin.ModelAdmin):
    list_display = ('post', 'owner', 'added')

admin.site.register(models.Account)
admin.site.register(models.Post, SettingAdminPost)
admin.site.register(models.Like)
admin.site.register(models.Dislike)
admin.site.register(models.Coment, SettingAdminComent)
admin.site.register(models.Interaction)