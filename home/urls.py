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
]
