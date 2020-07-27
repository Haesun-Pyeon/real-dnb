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
    for l in range(len(f)):
        name = f.loc[l, 'name']
        print(name)
        img = f.loc[l, 'img']
        try:
            store = BookStore.objects.get(name=name)
            if img:
                store.img = img
            store.save()
        except:
            print("실패")
            pass
    
print('수정완료')