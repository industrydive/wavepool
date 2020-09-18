from django.db import models
from django.urls import reverse

import datetime
from urllib.parse import urlparse

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
        """
        Parses the source field to determine the divesite.
        Assume the source field is of format "http://www.[site].com/rest-of-url"
        """
        site = urlparse(self.source)[1].split('.')[1]
        return DIVESITE_SOURCE_NAMES[site]

    def tags(self):
        return [
            'HR', 'Diversity & Inclusion', 'Culture'
        ]
