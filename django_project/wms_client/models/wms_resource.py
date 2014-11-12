# coding=utf-8
"""Model class for WMS Resource"""
__author__ = 'ismailsunni'
__project_name = 'django-wms-client'
__filename = 'wms_resource.py'
__date__ = '11/11/14'
__copyright__ = 'imajimatika@gmail.com'
__doc__ = ''

from django.contrib.gis.db import models
from django.conf.global_settings import MEDIA_ROOT
from django.utils.text import slugify
import os
from owslib.wms import WebMapService


class WMSResource(models.Model):
    """WMS Resource model."""
    class Meta:
        """Meta class."""
        app_label = 'wms_client'

    slug = models.SlugField(
        unique=True,
        primary_key=True
    )

    name = models.CharField(
        help_text='The identifier for the WMS Resource.',
        null=False,
        blank=False,
        unique=True
    )

    uri = models.CharField(
        help_text='URI for the WMS resource',
        null=False,
        blank=False
    )

    layers = models.CharField(
        help_text='The layers that you want to retrieve.',
        blank=True,
        null=False,
    )

    descriptions = models.TextField(
        help_text='This is similar to abstract part of a wms resources.',
        blank=False,
    )

    preview = models.ImageField(
        help_text='Preview image for this WMS Resource.',
        upload_to=os.path.join(MEDIA_ROOT, 'wms_preview'),
        blank=True
    )

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Overloaded save method."""
        self.populate_wms_resource()
        self.slug = slugify(self.name)
        if not self.layers:
            self.layers = self.name
        super(WMSResource, self).save(*args, **kwargs)

    def populate_wms_resource(self):
        """Populate the model fields based on a uri."""
        wms = WebMapService(self.uri)
        self.name = wms.identification.title
        self.descriptions = wms.identification.abstract