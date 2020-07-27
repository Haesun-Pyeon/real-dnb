import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE","dnbookproject.settings")
import django
django.setup()
from bookmap.models import BookStore, Tag
import pandas as pd
import simplejson


if __name__ == '__main__':
    f = pd.read_excel('bookDB2.xlsx')
    order=0
    for l in range(len(f)):
        name = f.loc[l, 'name']
        print(name)
        addr = f.loc[l, 'addr']
        phone_number = f.loc[l, 'phone_number']
        site = f.loc[l, 'site']
        img = f.loc[l, 'img']
        insta = f.loc[l, 'insta']
        email = f.loc[l, 'email']
        oh = str(f.loc[l, 'openhour'])
        openhour=oh.replace(';','\n')
        tag = str(f.loc[l, 'tag_set'])
        tag = tag.split(';')
        order += 1
        BookStore.objects.create(
        name=name,
        addr=addr,
        insta=insta,
        site=site,
        email=email,
        phone_number=phone_number,
        openhour=openhour,
        img=img,
        order=order)
        
        try:
            store = BookStore.objects.get(name=name)
            for t in tag:
                if len(t) == 0:
                    continue
                try:
                    temp = Tag.objects.get(title=t)
                    store.tag_set.add(temp)
                except:
                    temp = Tag.objects.create(title=t)
                    store.tag_set.add(temp)
        except:
            pass
print('저장완료')