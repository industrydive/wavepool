from django import forms
from django.contrib import admin
from wavepool.models import NewsPost


class NewsPostForm(forms.ModelForm):
    model = NewsPost
    fields = '__all__'

    def clean(self, *args, **kwargs):
        """ cleans form data
        """
        # user selected "is cover story checkbox":
        if self.data.get('is_cover_story') == 'on':
            all_newsposts = NewsPost.objects.all()
            # for each newspost, if it is the current cover story and NOT this newspost anyways,
            # unset it as cover story and save
            for n in all_newsposts:
                if n.is_cover_story == True:
                    if n != self.instance:
                        n.is_cover_story = False
            n.save()
        return super(NewsPostForm, self).clean(*args, **kwargs)


class NewsPostAdmin(admin.ModelAdmin):
    form = NewsPostForm


admin.site.register(NewsPost, NewsPostAdmin)
