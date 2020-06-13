from django.urls import path

from theme.views import main, staff

app_name = 'theme'

urlpatterns = [
    path(
        'application',
        main.ApplicationView.as_view(),
        name='application'
    ),
    path(
        'staff/period',
        staff.PeriodView.as_view(),
        name='period'
    ),
    path(
        'staff/period/application',
        staff.PeriodCreateView.as_view(),
        {'mode': 'application'},
        name='period_application'
    ),
    path(
        'staff/period/first_vote',
        staff.PeriodCreateView.as_view(),
        {'mode': 'first_vote'},
        name='period_first_vote'
    ),
    path(
        'staff/period/final_vote',
        staff.PeriodCreateView.as_view(),
        {'mode': 'final_vote'},
        name='period_final_vote'
    ),
    path(
        'staff/period/delete/<str:mode>/<int:pk>',
        staff.period_delete,
        name='period_delete'
    ),
    path(
        'staff/list',
        staff.ListView.as_view(),
        name='list'
    ),
    path(
        'staff/detail/<int:pk>',
        staff.DetailView.as_view(),
        name='detail'
    ),
    path(
        'staff/accept/<int:pk>',
        staff.accept,
        name='accept'
    ),
    path(
        'staff/disaccept/<int:pk>',
        staff.disaccept,
        name='disaccept'
    ),
    path(
        'staff/csv_download',
        staff.csv_download,
        name='csv_download'
    ),
]
