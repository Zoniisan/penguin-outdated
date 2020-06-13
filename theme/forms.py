from django import forms

from theme import models


class ThemeForm(forms.ModelForm):
    """PENGUIN アカウント（仮登録）
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
