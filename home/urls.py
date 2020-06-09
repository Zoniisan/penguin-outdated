from django.urls import path

from home.views import (view_contact, view_csv, view_main, view_notice,
                        view_notification)

app_name = 'home'

urlpatterns = [
    path(
        '',
        view_main.IndexView.as_view(),
        name='index'
    ),
    path(
        'signup_token',
        view_main.SignUpTokenView.as_view(),
        name='signup_token'
    ),
    path(
        'signup_token_finish',
        view_main.SignUpTokenFinishView.as_view(),
        name='signup_token_finish'
    ),
    path(
        'signup/<token>',
        view_main.SignUpView.as_view(),
        name='signup'
    ),
    path(
        'signup_finish',
        view_main.SignUpFinishView.as_view(),
        name='signup_finish'
    ),
    path(
        'login',
        view_main.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout',
        view_main.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'profile',
        view_main.ProfileView.as_view(),
        name='profile'
    ),
    path(
        'notice',
        view_notice.NoticeView.as_view(),
        name='notice'
    ),
    path(
        'notice_delete/<pk>',
        view_notice.notice_delete,
        name='notice_delete'
    ),
    path(
        'notice_update/<pk>',
        view_notice.NoticeUpdateView.as_view(),
        name='notice_update'
    ),
    path(
        'contact',
        view_contact.ContactView.as_view(),
        name='contact'
    ),
    path(
        'contact_kind',
        view_contact.ContactKindView.as_view(),
        name='contact_kind'
    ),
    path(
        'contact_list/<pk>',
        view_contact.ContactListView.as_view(),
        name='contact_list'
    ),
    path(
        'contact_detail/<pk>',
        view_contact.ContactDetailView.as_view(),
        name='contact_detail'
    ),
    path(
        'notification',
        view_notification.NotificationView.as_view(),
        {'mode': None},
        name='notification'
    ),
    path(
        'notification/reply_to_contact/<contact_pk>',
        view_notification.NotificationView.as_view(),
        {'mode': 'reply_to_contact'},
        name='notification_reply_to_contact'
    ),
    path(
        'notification/all',
        view_notification.NotificationView.as_view(),
        {'mode': 'all'},
        name='notification_all'
    ),
    path(
        'notification_staff_list',
        view_notification.NotificationStaffListView.as_view(),
        name='notification_staff_list'
    ),
    path(
        'notification_staff_list/p=<page>',
        view_notification.NotificationStaffListView.as_view(),
        name='notification_staff_list'
    ),
    path(
        'notification_staff_detail/<pk>',
        view_notification.NotificationStaffDetailView.as_view(),
        name='notification_staff_detail'
    ),
    path(
        'notification_list',
        view_notification.NotificationListView.as_view(),
        name='notification_list'
    ),
    path(
        'notification_list/p=<page>',
        view_notification.NotificationListView.as_view(),
        name='notification_list'
    ),
    path(
        'notification_detail/<pk>',
        view_notification.NotificationDetailView.as_view(),
        name='notification_detail'
    ),
    path(
        'staff_list',
        view_main.StaffListView.as_view(),
        name='staff_list'
    ),
    path(
        'download_staff_vcards/<mode>',
        view_main.download_staff_vcards,
        name='download_staff_vcards'
    ),
    path(
        'csv_group',
        view_csv.CsvView.as_view(),
        {'mode': 'group'},
        name='csv_group'
    ),
    path(
        'csv_group_confirm',
        view_csv.CsvConfirmView.as_view(),
        {'mode': 'group'},
        name='csv_group_confirm'
    ),
    path(
        'csv_group_success',
        view_csv.CsvSuccessView.as_view(),
        {'mode': 'group'},
        name='csv_group_success'
    ),
    path(
        'csv_group_download',
        view_csv.csv_download,
        {'mode': 'group'},
        name='csv_group_download'
    ),
    path(
        'csv_contact_kind',
        view_csv.CsvView.as_view(),
        {'mode': 'contact_kind'},
        name='csv_contact_kind'
    ),
    path(
        'csv_contact_kind_confirm',
        view_csv.CsvConfirmView.as_view(),
        {'mode': 'contact_kind'},
        name='csv_contact_kind_confirm'
    ),
    path(
        'csv_contact_kind_success',
        view_csv.CsvSuccessView.as_view(),
        {'mode': 'contact_kind'},
        name='csv_contact_kind_success'
    ),
    path(
        'csv_contact_kind_download',
        view_csv.csv_download,
        {'mode': 'contact_kind'},
        name='csv_contact_kind_download'
    ),
    path(
        'csv_staff_register',
        view_csv.CsvView.as_view(),
        {'mode': 'staff_register'},
        name='csv_staff_register'
    ),
    path(
        'csv_staff_register_confirm',
        view_csv.CsvConfirmView.as_view(),
        {'mode': 'staff_register'},
        name='csv_staff_register_confirm'
    ),
    path(
        'csv_staff_register_success',
        view_csv.CsvSuccessView.as_view(),
        {'mode': 'staff_register'},
        name='csv_staff_register_success'
    ),
    path(
        'csv_staff_register_download',
        view_csv.csv_download,
        {'mode': 'staff_register'},
        name='csv_staff_register_download'
    ),
]
