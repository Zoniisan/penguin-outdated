from django.contrib import admin


class AdminSite(admin.AdminSite):
    """ 管理サイトに関する設定
    """

    site_header = 'PENGUIN 管理サイト'
    site_title = site_header
    empty_value_display = '(Null)'
