from django import http
from django.shortcuts import render


def index(request):
    return http.HttpResponse('root')
