
from django.http import HttpResponse
from time import sleep

def fake_long_request(request):
    seconds = int(request.GET['seconds'])
    sleep(seconds)
    html = "<html><body>Slept %s seconds.</body></html>" % seconds
    return HttpResponse(html)