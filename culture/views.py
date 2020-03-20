from django.shortcuts import render
from bookmap.models import BookStore
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def board(request):
    insta_book = BookStore.objects.filter(~Q(insta='nan')).order_by('?')
    paginator = Paginator(insta_book,10)
    page = request.GET.get('page')
    pageposts=paginator.get_page(page)
    return render(request, 'board.html', {'pageposts':pageposts,})