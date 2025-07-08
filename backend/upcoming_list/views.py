from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def upcoming(req):
    if req.method == 'GET':
        pass
    else:
        return JsonResponse()