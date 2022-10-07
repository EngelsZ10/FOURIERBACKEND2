from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from  ASCII.ImageToASCII import getAscii
from json import load
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return HttpResponse('<p>Hello from Python!<p\>')

@csrf_exempt
def Ascii(request):
    dir = load(request)
    txt = getAscii(dir["image"], False, 200, 2)
    return JsonResponse({"text": txt})
