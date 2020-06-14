from django.urls import path

from theme.views import main, staff

app_name = 'theme'

urlpatterns = [
    path(
        'submit',
        main.SubmitView.as_view(),
        name='submit'
    ),
]
