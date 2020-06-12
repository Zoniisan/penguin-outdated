from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms


class PeriodForm(forms.Form):
    """Period 登録用のフォーム
    """
    start = forms.DateTimeField(
        label='開始',
        widget=DateTimePickerInput(
            options={
                'format': 'YYYY-MM-DD HH:mm',
                'locale': 'ja'
            }
        ).start_of('period')
    )

    finish = forms.DateTimeField(
        label='終了',
        widget=DateTimePickerInput(
            options={
                'format': 'YYYY-MM-DD HH:mm',
                'locale': 'ja'
            }
        ).end_of('period')
    )
