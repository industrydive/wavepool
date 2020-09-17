from django.db import models
from django.urls import reverse

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
        """ Return the real divesite source name for the newspost's source
        """
        source_dive = 'Industry Dive'
        for dive_source in DIVESITE_SOURCE_NAMES:
            url_parts = self.source.split('/')
            dive_domain = url_parts[2]
            domain_parts = dive_domain.split('.')
            dive_domain = domain_parts[1]
            if dive_domain == dive_source:
                return DIVESITE_SOURCE_NAMES[dive_domain]
        return source_dive

    def tags(self):
        return [
            'HR', 'Diversity & Inclusion', 'Culture'
        ]
