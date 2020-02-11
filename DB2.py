import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","dnbookproject.settings")
import django
django.setup()
from bookmap.models import BookStore, Tag
import pandas as pd

if __name__ == '__main__':
    f = pd.read_excel('561.xlsx')
    for l in range(len(f)):
        name = f.loc[l, 'name']
        tag = str(f.loc[l, 'tag'])
        tag = tag.split(',')
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