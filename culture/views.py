from django.shortcuts import render
from bookmap.models import BookStore
import simplejson
import random
# Create your views here.

def board(request):
    bookstores = BookStore.objects.all()
    insta = []
    for a in bookstores:
        if a.insta != 'nan':
            insta.append(a.insta)
        else: pass
    random.shuffle(insta)
    insta=insta[:9]
    instalist = simplejson.dumps(insta)
    return render(request, 'board.html', {'instalist':instalist,'stores':bookstores,})