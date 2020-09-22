from django import forms
from django.contrib import admin
from wavepool.models import NewsPost


class NewsPostForm(forms.ModelForm):
    model = NewsPost
    fields = '__all__'


class NewsPostAdmin(admin.ModelAdmin):
    form = NewsPostForm
    list_display = ('title', 'publish_date', 'is_cover_story')
    ordering = ('publish_date',)


admin.site.register(NewsPost, NewsPostAdmin)
