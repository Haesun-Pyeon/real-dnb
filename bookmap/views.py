from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.contrib.auth.models import User
from .models import BookStore, Scrap, Review, Tag, Crawling, Stamp
from main.models import Profile
from django.core import serializers
import simplejson
from .forms import ReviewForm, AddThemaForm
from django.db.models import Avg
import os
from datetime import datetime


# Create your views here.

def dangol(request, bookstore_id):
    store = BookStore.objects.get(bookstore_id=bookstore_id)
    stamp = Stamp.objects.filter(store=store)
    dangol = {}
    for s in stamp:
        profile = Profile.objects.get(user=s.user)
        name = profile.nickname
        if name in dangol.keys():
            dangol[name] += 1
        else:
            dangol[name] = 1
    dangol_sort = sorted(dangol.items(), key=lambda x: x[1], reverse=True)
    return dangol_sort

def detail(request, bookstore_id):
    dan = dangol(request, bookstore_id)
    first = {}
    second = {}
    third = {}
    total_list = [first, second, third]
    for i,t in enumerate(total_list):
        try:
            t['name'] = dan[i][0]
            t['count'] = dan[i][1]
        except:
            t['name'] = '없음'
            t['count'] = 0
    store_detail = get_object_or_404(BookStore, pk = bookstore_id)
    scrap = Scrap.objects.filter(store=store_detail)
    rev = Crawling.objects.filter(store=store_detail)
    tot = 0
    reviews = store_detail.review_set.all().order_by('-created_at')
    for i in store_detail.review_set.all():
        tot += i.star
    if store_detail.review_set.all().count():
        star_avg = '%.1f' %(tot/(store_detail.review_set.all().count()))
    else:
        star_avg = 0
    if request.user.is_authenticated:
        store_scrap = scrap.filter(user=request.user)
        form = ReviewForm()
        return render(request, 'storedetail.html', {'reviews':reviews,'rev' : rev, 'store' : store_detail, 'scrap' : store_scrap, 'form':form, 'star_avg':star_avg, 'first':first, 'second':second, 'third':third, })
    else:
        return render(request, 'storedetail.html', {'reviews':reviews,'rev' : rev, 'store' : store_detail, 'star_avg':star_avg, 'first':first, 'second':second, 'third':third, })
      
def stamp(request, bookstore_id):
    user = request.user
    store = BookStore.objects.get(bookstore_id=bookstore_id)
    prev_stamp = Stamp.objects.filter(user=user, store=store)
    overlap = False
    if (prev_stamp):
        for s in prev_stamp:
            date = str(s.created_at)
            stamp_date = date.split()[0]
            date = str(datetime.today())
            today_date = date.split()[0]
            if (stamp_date == today_date):
                overlap = True
                break
            else:
                pass
        if overlap == True:
            content = "<script type='text/javascript'>alert('하루에 한 번만 적립 가능합니다.');history.back();</script>"
            return HttpResponse(content)
    if overlap == False:
        stamp = Stamp(user=user, store=store, count=1)
        stamp.save()
        content = "<script type='text/javascript'>alert('스탬프 1개 적립 완료');history.back();</script>"
        return HttpResponse(content)

def realmap(request):
    bookstores = BookStore.objects.all()
    addr = []
    name = []
    storepk = []
    for a in bookstores:
        addr.append(a.addr)
        name.append(a.name)
        storepk.append(a.bookstore_id)
    addrlist = simplejson.dumps(addr)
    namelist = simplejson.dumps(name)
    pklist = simplejson.dumps(storepk)
    return render(request, 'realmap.html', {
        'bs':bookstores, 
        'bsaddr' : addrlist, 
        'bsname' : namelist,
        'pklist' : pklist})

def scrap(request, bookstore_id):
    store = get_object_or_404(BookStore, pk=bookstore_id)
    scrapped = Scrap.objects.filter(user=request.user, store=store)
    if not scrapped:
        Scrap.objects.create(user=request.user, store=store)
    else:
        scrapped.delete()
    return redirect('storedetail', bookstore_id=bookstore_id)

def reviewcreate(request, bookstore_id):
    store = get_object_or_404(BookStore, pk=bookstore_id)
    if request.method=='POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            star=request.POST["star"]
            review.star = star
            review.user = request.user
            review.store = store
            review.save()
            return redirect('storedetail', bookstore_id=bookstore_id)
        else:
            redirect('bookstore')
    else:
        return redirect('storedetail', bookstore_id=bookstore_id)

def reviewdelete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    return redirect('storedetail', bookstore_id=review.store.pk)

def mapsearch(request):
    bookstores = BookStore.objects.all()
    query = request.GET.get('query','')
    if query:
        stype = request.GET['searchtype']
        if stype == 'searchname':
            bookstores = bookstores.filter(name__contains=query)
        else:
            bookstores = bookstores.filter(addr__contains=query)
        addr = []
        name = []
        storepk = []
        for a in bookstores:
            addr.append(a.addr)
            name.append(a.name)
            storepk.append(a.bookstore_id)
        addrlist = simplejson.dumps(addr)
        namelist = simplejson.dumps(name)
        pklist = simplejson.dumps(storepk)
        return render(request, 'realmap.html', {
            'bs':bookstores, 
            'bsaddr' : addrlist, 
            'bsname' : namelist,
            'pklist' : pklist})
    else:
        return redirect('realmap')

def get_stamp_info(request,tf):
    stamp = Stamp.objects.all()
    stamp_month = []
    stamp_ic = []
    stamp_idx = []
    user_img = {}
    user_nick = {}
    user_count = {}
    result = {}
    for s in stamp:
        d = str(s.created_at)
        d=d.split()[0]
        date = datetime.strptime(d, "%Y-%m-%d")
        stamp_month.append(date.month)
        stamp_ic.append([str(s.user), int(s.count)])
        profile = Profile.objects.get(user=s.user)
        try:
            user_img[str(s.user)] = profile.profileimg
        except:
            user_img[str(s.user)] = None
        user_nick[str(s.user)]=profile.nickname
    today = datetime.today().month
    for i,m in enumerate(stamp_month):
        if m == today:
            stamp_idx.append(i)
    if tf == True:
        for i in stamp_idx:
            name = stamp_ic[i][0]
            count = stamp_ic[i][1]
            if name in user_count:
                user_count[name] += count
            else:
                user_count[name] = count
    else:
        for i,s in enumerate(stamp_ic):
            name = s[0]
            count = s[1]
            if name in user_count:
                user_count[name] += count
            else:
                user_count[name] = count
    result = [user_nick, user_count, user_img]
    return result

def ranking(request):
    total = get_stamp_info(request,False)
    month = get_stamp_info(request, True)
    nickname = [total[0], month[0]]
    count = [total[1], month[1]]
    img = [total[2], month[2]]
    res_first = {}
    res_second = {}
    res_third = {}
    res_total = [res_first, res_second, res_third]
    key_arr = ['total_nickname', 'month_nickname', 'total_stamp', 'month_stamp', 'total_img', 'month_img']

    for idx,cnt in enumerate(count): #idx가 0이면 전체, 1이면 월별
        first, second, third = [-1, '없음'], [-1, '없음'], [-1, '없음']
        for k,v in cnt.items(): #k는 id, v는 갯수
            if first[0] <= v:
                third = second
                second = first
                first = [v,k]
            elif second[0] <= v:
                third = second
                second = [v,k]
            elif third[0] <= v:
                third = [v, k]
            else:
                pass
        
        if first != [-1, '없음']:
            nick_f = nickname[idx][first[1]]
            img_f = img[idx][first[1]]
        else:
            nick_f = first[1]
            img_f = None

        if second != [-1, '없음']:
            nick_s = nickname[idx][second[1]]
            img_s = img[idx][second[1]]
        else:
            nick_s = second[1]
            img_s = None

        if third != [-1, '없음']:
            nick_t = nickname[idx][third[1]]
            img_t = img[idx][third[1]]
        else:
            nick_t = third[1]
            img_t = None

        nick_tot = [nick_f, nick_s, nick_t]
        img_tot = [img_f, img_s, img_t]
        count_tot = [first[0], second[0], third[0]]
        
        for i, t in enumerate(res_total):
            t[key_arr[idx]] = nick_tot[i]
            t[key_arr[idx + 2]] = count_tot[i]
            t[key_arr[idx + 4]] = img_tot[i]

    return render(request, 'ranking.html', {'first': res_first, 'second': res_second, 'third': res_third})
    
def my_thema(request):
    thema = Tag.objects.filter(user=request.user)
    return render(request, 'themamap.html', {'thema': thema})
    
def themamap(request):
    thema = Tag.objects.filter(private=False)
    return render(request, 'themamap.html',{'thema':thema})

def themadetail(request, tag_id):
    thema = get_object_or_404(Tag, pk=tag_id)
    stores = BookStore.objects.filter(tag_set=thema)
    addr = []
    name = []
    storepk = []
    for a in stores:
        addr.append(a.addr)
        name.append(a.name)
        storepk.append(a.bookstore_id)
    addrlist = simplejson.dumps(addr)
    namelist = simplejson.dumps(name)
    pklist = simplejson.dumps(storepk)
    content = {'thema':thema,
            'stores':stores,
            'bsaddr':addrlist,
            'bsname':namelist,
            'pklist':pklist}

    return render(request, 'themadetail.html', content)

def addthema(request):
    if request.method == 'POST':
        form = StoreEditForm(request.POST, request.FILES)
        if form.is_valid():

            return redirect('my_thema')
        else:
            pass #폼이 유효하지 않은 경우,,
    else:
        form = AddThemaForm()
        stores = BookStore.objects.all()
        return render(request, 'addthema.html', {'form': form, 'stores': stores})