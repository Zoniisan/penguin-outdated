from django import forms

from theme import models


class ThemeForm(forms.ModelForm):
    """統一テーマ応募
    """
    class Meta:
        model = models.Theme
        fields = (
            'theme', 'description'
        )
        widgets = {
            "theme": forms.TextInput(
                attrs={
                    'onKeyUp': 'countLength(value, "count_theme");',
                }
            ),
            "description": forms.Textarea(
                attrs={
                    'onKeyUp': 'countLength(value, "count_description");',
                }
            ),
        }


class FinishVoteCountForm(forms.Form):
    """決選投票に進める件数を指定
    """
    # max_value は予選進出した（受理された）統一テーマの件数
    count = forms.IntegerField(
        label='決勝進出件数',
        max_value=models.Theme.objects.filter(first_id__isnull=False).count(),
        min_value=1
    )
