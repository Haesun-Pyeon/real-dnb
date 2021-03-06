import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE","dnbookproject.settings")
import django
django.setup()
from bookmap.models import BookStore, Tag
import simplejson


if __name__ == '__main__':
    order = int(input("수정할 책방의 오더: "))
    print("아래부터는 수정할 사항만 입력해주세요.(안바꿀부분은 그냥 엔터)")
    name = input("수정할 책방 이름: ")
    addr = input("수정할 책방 주소: ")
    phone_number = input("수정할 책방 전화번호: ")
    site = input("수정할 책방 사이트: ")
    img = input("수정할 책방 이미지: ")
    insta = input("수정할 책방 인스타: ")
    email = input("수정할 책방 이메일: ")
    oh = input("수정할 책방 영업시간(엔터는 ;로입력): ")
    openhour=oh.replace(';','\n')
    tag = input("수정할 책방 태그(;로 구분)-바꿀거면 일부말고 전체다입력: ")
    if tag:
        tag = tag.split(';')
    else:
        pass

    store = BookStore.objects.get(order=order)
    if name: store.name = name
    if addr: store.addr = addr
    if insta: store.insta = insta
    if site: store.site = site
    if email: store.email = email
    if phone_number: store.phone_number = phone_number
    if openhour: store.openhour = openhour
    if img: store.img = img
    if tag:
        store.tag_set.clear()
        for t in tag:
            if len(t) == 0:
                continue
            try:
                temp = Tag.objects.get(title=t)
                store.tag_set.add(temp)
            except:
                temp = Tag.objects.create(title=t)
                store.tag_set.add(temp)
    store.save()
    
print('수정완료')