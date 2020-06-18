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


class FinalAcceptForm(forms.Form):
    """決選投票に進む件数を入力する

    1 以上 受理された統一テーマ案件数
    """
    final_accept = forms.IntegerField(
        label='決選投票進出件数',
        min_value=1,
    )
