from django.shortcuts import render
from bookmap.models import BookStore
from el_pagination.decorators import page_template

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
    instalist = simplejson.dumps(insta)
    context = {
        'instalist':instalist, 
        'insta':insta,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)