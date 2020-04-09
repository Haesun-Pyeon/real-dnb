import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE","dnbookproject.settings")
import django
django.setup()
from bookmap.models import BookStore

if __name__ == '__main__':
    order = 1
    while True:
        store = BookStore.objects.get(bookstore_id=order)
        store.order = order
        order += 1
        store.save()
        if order == 406:
            break
print('수정완료')