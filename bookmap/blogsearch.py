import os
import sys
import urllib.request


def blog_search(name, addr):
    client_id = "T8MZqPcXGrKd5jgkfQqD"
    client_secret = "WwJGey2Jx8"
    address = addr.split()
    city = address[1]
    encText = urllib.parse.quote(city+" "+name)
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=5" # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        return response_body.decode('utf-8')
    else:
        return "Error Code:" + rescode