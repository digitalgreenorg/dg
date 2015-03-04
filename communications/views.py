from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render_to_response
from django.template import RequestContext
from communications.models import Article

def media_view(request):
    if (request.GET.get('latest', None) =="true"):
        media_list = Article.objects.all().order_by('-pub_date')[O:1]
        paginator = Paginator(media_list, 4) #dividing 4 articles per page
        page = request.GET.get('page')
        try:
            media = paginator.page(page)
        except PageNotAnInteger:
            media = paginator.page(1)
        except EmptyPage:
            media = paginator.page(paginator.num_pages)
    else:
        media_list = Article.objects.all().order_by('-pub_date')
        paginator = Paginator(media_list, 4) #dividing 4 articles per page
        page = request.GET.get('page')
        try:
            media = paginator.page(page)
        except PageNotAnInteger:
            media = paginator.page(1)
        except EmptyPage:
            media = paginator.page(paginator.num_pages)

    return render_to_response('press.html',{'media':media}, context_instance = RequestContext(request))
