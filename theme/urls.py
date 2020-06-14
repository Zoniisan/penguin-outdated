from django.urls import path

from theme.views import main, staff

app_name = 'theme'

urlpatterns = [
    path(
        'submit',
        main.SubmitView.as_view(),
        name='submit'
    ),
    path(
        'first_vote',
        main.FirstVoteView.as_view(),
        name='first_vote'
    ),
    path(
        'first_vote/<int:pk>',
        main.first_vote,
        name='first_vote_pk'
    ),
    path(
        'staff/list',
        staff.ListView.as_view(),
        name='staff_list'
    ),
    path(
        'staff/detail/<int:pk>',
        staff.DetailView.as_view(),
        name='staff_detail'
    ),
    path(
        'staff/accept/<int:pk>',
        staff.accept,
        name='staff_accept'
    ),
    path(
        'staff/disaccept/<int:pk>',
        staff.disaccept,
        name='staff_disaccept'
    ),
    path(
        'staff/csv_download',
        staff.csv_download,
        name='csv_download'
    ),
    path(
        'staff/first_vote',
        staff.FirstVoteView.as_view(),
        name='staff_first_vote'
    ),
]
