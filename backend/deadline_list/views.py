from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def view_item(req):
    if req.method == 'GET':
        pass
    else:
        return JsonResponse()