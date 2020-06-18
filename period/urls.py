from django.urls import path

from period import views

app_name = 'period'

urlpatterns = [
    path(
        'list',
        views.ListView.as_view(),
        name='list'
    ),
]
