import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","dnbookproject.settings")
import django
django.setup()
from bookmap.models import BookStore, Tag
import pandas as pd

if __name__ == '__main__':
    f = pd.read_excel('bookDB2.xlsx')
    for l in range(len(f)):
        name = f.loc[l, 'name']
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

        BookStore.objects.create(
        name=name,
        addr=addr,
        insta=insta,
        site=site,
        email=email,
        phone_number=phone_number,
        openhour=openhour,
        img=img)
        
        try:
            store = BookStore.objects.get(name=name)
            for t in tag:
                try:
                    temp = Tag.objects.get(title=t)
                    store.tag_set.add(temp)
                except:
                    temp = Tag.objects.create(title=t)
                    store.tag_set.add(temp)
        except:
            pass
print('저장완료')