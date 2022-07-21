from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import CreateView
import time
from django.http import JsonResponse, HttpResponse
import asyncio
from time import sleep
import httpx

from .models import Person
from .serializer import *


class DaybookView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DaybookSerializer
    queryset = Daybook.objects.all()

    def get_object(self):
        return Daybook.objects.get(id=self.request.GET.get('id'))


def index(request):
    context = {'list': Daybook.objects.all()}
    return render(request, 'first_page.html', context)


def filter_request(request):
    param = request.GET.get('param', 'all')
    name = request.GET.get('name', None)
    point = request.GET.get('point', 1)

    if param == 'all':
        queryset = Daybook.objects.all()
    elif param == 'filter':
        queryset = Daybook.objects.filter(name=name).order_by('-point')
    elif param == 'exclude':
        queryset = Daybook.objects.exclude(point=2)
    else:
        queryset = Daybook.objects.filter(name=name).union(Daybook.objects.filter(point=point))
        queryset = Daybook.objects.all().intersection(Daybook.objects.filter(name=name))


def get_request(request, id=0):
    param = request.GET.get('param', 0)
    head = request.headers.get('Accept-Language')

    context = Daybook.objects.filter(id=id, param=param)
    return render(request, 'first_page.html', context)


def post_request(request):
    print(request.data)
    name = request.data.get('lesson')
    point = request.data.get('point')

    if request.method == 'POST':
        context = Daybook.objects.create(name=name, point=point)
    else:
        context = Daybook.objects.get(id=1).update(name=name, point=point)
    return render(request, 'first_page.html', context)


def delete_request(request, id):
    try:
        Daybook.objects.get(id=id).delete()
    except Daybook.DoesNotExist:
        return Http404("Daybook does not exist")
    return HttpResponse({'status': 'delete'})


class DaybookViewW(View):
    def get(self):
        pass

    def post(self):
        pass


class PersonCreateView(CreateView):
    template_name = 'person_form.html'
    model = Person
    fields = ('name', 'email', 'job_title', 'bio')


def api(request):
    time.sleep(1)
    payload = {"message": "Hello from Crowdbotics!"}
    if "task_id" in request.GET:
        payload["task_id"] = request.GET["task_id"]
    return JsonResponse(payload)


async def http_call_async():
    for num in range(1, 6):
        await asyncio.sleep(1)
        print(num)
    async with httpx.AsyncClient() as client:
        r = await client.get("https://httpbin.org")
        print(r)


async def async_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_call_async())
    return HttpResponse('Non-blocking HTTP request')


def http_call_sync():
    for num in range(1, 6):
        sleep(1)
        print(num)
    r = httpx.get("https://httpbin.org/")
    print(r)


def sync_view(request):
    http_call_sync()
    return HttpResponse("Blocking HTTP request")
