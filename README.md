# DNBOOK
독립서점, 독립출판물 정보 사이트
**졸업작품으로 업그레이드**

## 기술
- Django

## pip
- django
- simplejson
- django-bootstrap4
- pillow
- (wheel)
- requests
- request
- django-detect
- django-allauth
- channels
- channels-redis
- websockets
- redis
- pandas
- xlrd
- pyyaml ua-parser user-agents
- django-user-agents

## 배포 시 추가 pip
- daphne
- boto3
- django-storages
- dj-database-url
- psycopg2-binary

## 모델 불러오기
- $python manage.py migrate

## 책방 DB 불러오기
- bookDB2.xlsx 파일 있는지 확인
- DB2.py 있는 위치에서 $python DB2.py 입력!

## 관리자계정 만들기
- $python manage.py createsuperuser
