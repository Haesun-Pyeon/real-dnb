from django.shortcuts import render
from bookmap.models import BookStore
from el_pagination.decorators import page_template
from django.core.paginator import Paginator
import simplejson
import random
# Create your views here.

@page_template('list_page.html')
def board(request, 
    template='board.html',
    extra_context=None):
    bookstores = BookStore.objects.all()
    insta = []
    for a in bookstores:
        if (a.insta != 'nan') and (a.insta not in insta):
            insta.append(a.insta)
        else: pass
    random.shuffle(insta)
    context = {
        'insta':insta,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

def board2(request):
    bookstores = BookStore.objects.all()
    insta = []
    for a in bookstores:
        if (a.insta != 'nan') and (a.insta not in insta):
            insta.append(a.insta)
        else: pass
    random.shuffle(insta)
    insta_book = BookStore.objects.filter(insta__in =insta).order_by('?')
    paginator = Paginator(insta_book,10)
    page = request.GET.get('page')
    pageposts=paginator.get_page(page)
    return render(request, 'board2.html', {'pageposts':pageposts,})