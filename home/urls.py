from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup_token', views.SignUpTokenView.as_view(), name='signup_token'),
    path(
        'signup_token_finish', views.SignUpTokenFinishView.as_view(),
        name='signup_token_finish'
    ),
    path(
        'signup/<token>', views.SignUpView.as_view(), name='signup'
    ),
    path(
        'signup_finish', views.SignUpFinishView.as_view(), name='signup_finish'
    ),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('notice', views.NoticeView.as_view(), name='notice'),
    path('notice_delete/<pk>', views.notice_delete, name='notice_delete'),
    path(
        'notice_update/<pk>',
        views.NoticeUpdateView.as_view(), name='notice_update'
    ),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('contact_kind', views.ContactKindView.as_view(), name='contact_kind'),
    path(
        'contact_list/<pk>', views.ContactListView.as_view(),
        name='contact_list'
    ),
    path(
        'contact_detail/<pk>', views.ContactDetailView.as_view(),
        name='contact_detail'
    ),
]
