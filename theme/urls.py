from django.urls import path

from theme.views import main, staff

app_name = 'theme'

urlpatterns = [
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
]
