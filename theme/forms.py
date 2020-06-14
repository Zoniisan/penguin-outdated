from django import forms

from theme import models
from countable_field.widgets import CountableWidget


class SubmitForm(forms.ModelForm):
    """統一テーマ応募
    """
    class Meta:
        model = models.Theme
        fields = (
            'theme', 'description'
        )
        widgets = {
            'theme': CountableWidget(attrs={
                'data-count': 'characters',
                'data-min-count': 1,
                'data-max-count': 100,
            }),
            'description': CountableWidget(attrs={
                'data-count': 'characters',
                'data-min-count': 100,
                'data-max-count': 400,
            })
        }
