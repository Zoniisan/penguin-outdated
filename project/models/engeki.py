from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# from project.models import Project


class Engeki(models.Model):
    """自主制作演劇企画
    """

    class Meta:
        verbose_name = '自主制作演劇企画'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.project)

    project = GenericRelation(
        'project.Project',
        related_query_name='engeki'
    )
