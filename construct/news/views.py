from django.shortcuts import render

from api.models import News, Profile
from modules.exceptions import *


@server_error_decorator
def index(request):
    latest_news = News.objects.filter(is_active=True).order_by('-pub_date')
    filter = str(request.GET.get('newsId'))

    if filter:
        current_new = News.objects.get(id=int(filter))
        news_id = int(filter)
    else:
        current_new = News.objects.filter(is_active=True).last()
        news_id = int(News.objects.filter(is_active=True).last().id)
    context = {
        'latest_news': latest_news,
        'current_new': current_new,
        'newsId': news_id,
    }
    if request.user.is_active:
        profile = Profile.objects.get(client_id=request.user)
        context['profile'] = profile
    return render(request, 'news/index.html', context)
