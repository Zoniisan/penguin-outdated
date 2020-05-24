from django.views import generic


class IndexView(generic.TemplateView):
    """ホーム画面
    """

    template_name = 'home/index.html'
