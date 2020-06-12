from home.views.contact import (ContactDetailView, ContactKindView,
                                ContactListView, ContactView)
from home.views.csv import (CsvConfirmView, CsvSuccessView, CsvView,
                            csv_download)
from home.views.main import (IndexView, LoginView, LogoutView, ProfileView,
                             SignUpFinishView, SignUpTokenFinishView,
                             SignUpTokenView, SignUpView, StaffListView,
                             download_staff_vcards)
from home.views.notice import (NoticeUpdateView, NoticeView, notice_delete,
                               notice_form_valid)
from home.views.notification import (NotificationDetailView,
                                     NotificationListView,
                                     NotificationStaffDetailView,
                                     NotificationStaffListView,
                                     NotificationView)
