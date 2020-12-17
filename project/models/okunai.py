from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Okunai(models.Model):
    """屋内企画
    """

    class Meta:
        verbose_name = '屋内企画'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.project)

    project = GenericRelation(
        'project.Project',
        related_query_name='okunai'
    )
