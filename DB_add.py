import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE","dnbookproject.settings")
import django
django.setup()
from bookmap.models import BookStore, Tag
import simplejson

if __name__ == '__main__':
    order1 = int(input("저장할 책방의 오더: "))
    print("입력하지 않을거면 nan 입력!")
    name1 = input("저장할 책방 이름: ")
    addr1 = input("저장할 책방 주소: ")
    phone_number1 = input("저장할 책방 전화번호: ")
    site1 = input("저장할 책방 사이트: ")
    img1 = input("저장할 책방 이미지: ")
    insta1 = input("저장할 책방 인스타: ")
    email1 = input("저장할 책방 이메일: ")
    oh = input("저장할 책방 영업시간(엔터는 ;로입력): ")
    openhour1=oh.replace(';','\n')
    tag = input("저장할 책방 태그(;로 구분)-필수입력: ")
    tag = tag.split(';')
    all_num=len(BookStore.objects.all())
    if order1 <= all_num:
        idx = all_num - order1 + 1
        book=BookStore.objects.get(order=all_num)
        for i in range(idx):
            book.order += 1
            book.save()
            book = BookStore.objects.get(order=all_num - i -1)
    else:
        pass
            
    BookStore.objects.create(
        name=name1,
        addr=addr1,
        insta=insta1,
        site=site1,
        email=email1,
        phone_number=phone_number1,
        openhour=openhour1,
        img=img1,
        order=order1)
        
    try:
        store = BookStore.objects.get(name=name1)
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
    
print('추가완료')