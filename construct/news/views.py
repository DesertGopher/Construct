from django.shortcuts import render

from api.models import News, Profile
from api.views import NewsList, NewsDetail, UserProfile, LastNews
from modules.exceptions import *


@server_error_decorator
def index(request):
    latest_news = NewsList().get(request=request)
    filter = str(request.GET.get('newsId'))

    if filter:
        current_new = NewsDetail().get(request=request, id=int(filter))
        news_id = int(filter)
    else:
        current_new = LastNews().get(request=request)
        news_id = int(LastNews().get(request=request).id)
    context = {
        'latest_news': latest_news,
        'current_new': current_new,
        'newsId': news_id,
    }
    if request.user.is_active:
        profile = UserProfile().get(request=request, client=request.user)
        context['profile'] = profile
    return render(request, 'news/index.html', context)
