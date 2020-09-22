from django.db import models
from django.urls import reverse
from django.db import transaction

import datetime

DIVESITE_SOURCE_NAMES = {
    'retaildive': 'Retail Dive',
    'ciodive': 'CIO Dive',
    'educationdive': 'Education Dive',
    'supplychaindive': 'Supply Chain Dive',
    'restaurantdive': 'Restaurant Dive',
    'grocerydive': 'Grocery Dive',
    'biopharmadive': 'BioPharma Dive',
    'hrdive': 'HR Dive',
}


class NewsPost(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=300)
    body = models.TextField(max_length=3000)
    source = models.URLField()
    is_cover_story = models.BooleanField(default=False)
    publish_date = models.DateField(default=datetime.date.today())

    @property
    def url(self):
        return reverse('newspost_detail', kwargs={'newspost_id': self.pk})

    @property
    def teaser(self):
        return self.body[:150]

    @property
    def source_divesite_name(self):
        return 'Industry Dive'

    def tags(self):
        return [
            'HR', 'Diversity & Inclusion', 'Culture'
        ]

    # Override save() to also reset other potential cover stories upon setting current as a cover story
    def save(self, *args, **kwargs):
        if not self.is_cover_story:
            return super(NewsPost, self).save(*args, **kwargs)
        with transaction.atomic():
            NewsPost.objects.filter(is_cover_story=True).update(is_cover_story=False)
            return super(NewsPost, self).save(*args, **kwargs)
