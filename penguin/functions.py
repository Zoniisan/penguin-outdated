from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404


def set_paging_parameter(kwargs, context, object_list, count=20):
    """ページング処理を行う際のパラメーターを context に登録する

    Args:
        kwargs(dict): self.kwargs
        context(dict): パラメーターを設定したい context
        list(list): ページング処理したいリスト
        count(int): 1 ページに表示する件数

    Examples:
        views.py:
            context = super().get_context_data(**kwargs)
            set_paging_parameter(context, object_list)
    """
    paginator = Paginator(object_list, count)

    # url で page が指定されていればそのページを、なければ 1 ページ目を表示
    page_no = kwargs.get('page', 1)

    # 存在しないページを指定した場合は失格（404 エラー）
    try:
        context['page_object'] = paginator.page(page_no)
    except (EmptyPage, PageNotAnInteger):
        raise Http404

    # その他描画に必要なパラメーターを登録
    context['page_no'] = int(page_no)
    context['page_range'] = paginator.page_range
