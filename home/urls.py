from django.urls import path

from home.views import contact, csv, main, notice, notification

app_name = 'home'

urlpatterns = [
    path(
        '',
        main.IndexView.as_view(),
        name='index'
    ),
    path(
        'signup_token',
        main.SignUpTokenView.as_view(),
        name='signup_token'
    ),
    path(
        'signup_token_finish',
        main.SignUpTokenFinishView.as_view(),
        name='signup_token_finish'
    ),
    path(
        'signup/<token>',
        main.SignUpView.as_view(),
        name='signup'
    ),
    path(
        'signup_finish',
        main.SignUpFinishView.as_view(),
        name='signup_finish'
    ),
    path(
        'login',
        main.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout',
        main.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'profile',
        main.ProfileView.as_view(),
        name='profile'
    ),
    path(
        'notice',
        notice.NoticeView.as_view(),
        name='notice'
    ),
    path(
        'notice_delete/<pk>',
        notice.notice_delete,
        name='notice_delete'
    ),
    path(
        'notice_update/<pk>',
        notice.NoticeUpdateView.as_view(),
        name='notice_update'
    ),
    path(
        'contact',
        contact.ContactView.as_view(),
        name='contact'
    ),
    path(
        'contact_kind',
        contact.ContactKindView.as_view(),
        name='contact_kind'
    ),
    path(
        'contact_list/<pk>',
        contact.ContactListView.as_view(),
        name='contact_list'
    ),
    path(
        'contact_detail/<pk>',
        contact.ContactDetailView.as_view(),
        name='contact_detail'
    ),
    path(
        'notification',
        notification.NotificationView.as_view(),
        {'mode': None},
        name='notification'
    ),
    path(
        'notification/reply_to_contact/<contact_pk>',
        notification.NotificationView.as_view(),
        {'mode': 'reply_to_contact'},
        name='notification_reply_to_contact'
    ),
    path(
        'notification/all',
        notification.NotificationView.as_view(),
        {'mode': 'all'},
        name='notification_all'
    ),
    path(
        'notification_staff_list',
        notification.NotificationStaffListView.as_view(),
        name='notification_staff_list'
    ),
    path(
        'notification_staff_list/p=<page>',
        notification.NotificationStaffListView.as_view(),
        name='notification_staff_list'
    ),
    path(
        'notification_staff_detail/<pk>',
        notification.NotificationStaffDetailView.as_view(),
        name='notification_staff_detail'
    ),
    path(
        'notification_list',
        notification.NotificationListView.as_view(),
        name='notification_list'
    ),
    path(
        'notification_list/p=<page>',
        notification.NotificationListView.as_view(),
        name='notification_list'
    ),
    path(
        'notification_detail/<pk>',
        notification.NotificationDetailView.as_view(),
        name='notification_detail'
    ),
    path(
        'staff_list',
        main.StaffListView.as_view(),
        name='staff_list'
    ),
    path(
        'download_staff_vcards/<mode>',
        main.download_staff_vcards,
        name='download_staff_vcards'
    ),
    path(
        'csv_group',
        csv.CsvView.as_view(),
        {'mode': 'group'},
        name='csv_group'
    ),
    path(
        'csv_group_confirm',
        csv.CsvConfirmView.as_view(),
        {'mode': 'group'},
        name='csv_group_confirm'
    ),
    path(
        'csv_group_success',
        csv.CsvSuccessView.as_view(),
        {'mode': 'group'},
        name='csv_group_success'
    ),
    path(
        'csv_group_download',
        csv.csv_download,
        {'mode': 'group'},
        name='csv_group_download'
    ),
    path(
        'csv_contact_kind',
        csv.CsvView.as_view(),
        {'mode': 'contact_kind'},
        name='csv_contact_kind'
    ),
    path(
        'csv_contact_kind_confirm',
        csv.CsvConfirmView.as_view(),
        {'mode': 'contact_kind'},
        name='csv_contact_kind_confirm'
    ),
    path(
        'csv_contact_kind_success',
        csv.CsvSuccessView.as_view(),
        {'mode': 'contact_kind'},
        name='csv_contact_kind_success'
    ),
    path(
        'csv_contact_kind_download',
        csv.csv_download,
        {'mode': 'contact_kind'},
        name='csv_contact_kind_download'
    ),
    path(
        'csv_staff_register',
        csv.CsvView.as_view(),
        {'mode': 'staff_register'},
        name='csv_staff_register'
    ),
    path(
        'csv_staff_register_confirm',
        csv.CsvConfirmView.as_view(),
        {'mode': 'staff_register'},
        name='csv_staff_register_confirm'
    ),
    path(
        'csv_staff_register_success',
        csv.CsvSuccessView.as_view(),
        {'mode': 'staff_register'},
        name='csv_staff_register_success'
    ),
    path(
        'csv_staff_register_download',
        csv.csv_download,
        {'mode': 'staff_register'},
        name='csv_staff_register_download'
    ),
]
