from django.contrib.auth.mixins import UserPassesTestMixin


class StaffOnlyMixin(UserPassesTestMixin):
    """is_staff = True の User のみアクセスできるようにする
    """
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff


class AdminOnlyMixin(UserPassesTestMixin):
    """is_superuser = True の User のみアクセスできるようにする
    """
    raise_exception = True

    def test_func(self):
        return self.request.user.is_superuser
