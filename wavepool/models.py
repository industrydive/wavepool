from django.db import models
from django.urls import reverse

import datetime
import re
from bs4 import BeautifulSoup

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

divesite_source_pattern = re.compile(r'www\.(.*)\.com')


class NewsPost(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField(max_length=3000)
    source = models.URLField()
    is_cover_story = models.BooleanField(default=False)
    publish_date = models.DateField(default=datetime.date.today())

    @property
    def clean_body(self):
        """We can't trust what's in the database to give us valid html. Normally
        I would fix this at the point of user input. For example give a validation
        error or just try to correct the error there.

        As it is I'm not changing the database, this is a quick fix to at least
        make it look a little bit cleaner for the browser (and testcases).
        """
        return BeautifulSoup(self.body, 'html.parser').prettify()

    @property
    def url(self):
        return reverse('newspost_detail', kwargs={'newspost_id': self.pk})

    @property
    def teaser(self):
        return self.body[:150]

    @property
    def source_divesite_name(self):
        """Try and pull the divesite name from the source url. If you find one,
        look it up in DIVESITE_SOURCE_NAMES. If not, default to Industry Dive"""
        match = divesite_source_pattern.findall(self.source)

        if match:
            return DIVESITE_SOURCE_NAMES[match[0]]

        return 'Industry Dive'

    def tags(self):
        return [
            'HR', 'Diversity & Inclusion', 'Culture'
        ]
