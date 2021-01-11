from django.db import models
from django.urls import reverse

import datetime
import re

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
        # use regex to match source url against DIVESITE_SOURCE_NAMES
        # will search up to two domain groups for a match (see illustration) 
        # https://subdomain.somewebsite.co.uk/other-stuff
        #         [   #1  ] [   #2    ]
        

        match_string = r'(?:https?\:\/\/)([a-zA-Z0-9\-]+)\.([a-zA-Z0-9\-]+)'
        domains = re.findall(match_string, self.source)

        # search through capture groups for a match
        if domains:
            for d in domains[0]: 
                if exists := DIVESITE_SOURCE_NAMES.get(d, False):
                    return exists

        # default
        return 'Industry Dive'       

    def tags(self):
        return [
            'HR', 'Diversity & Inclusion', 'Culture'
        ]
