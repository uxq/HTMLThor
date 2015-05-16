from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.shortcuts import render
from htmlthorapp import check
import sys
import json
import logging
logger = logging.getLogger('')


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def thorpedoFile(request):

    if request.method == 'POST':
        errorData = list()
        print request.FILES
        for filename, file in request.FILES.iteritems():
            extension = request.FILES[filename].name.split(".")
            errorData.append(check.checkFile(request.FILES[filename], extension[-1]))
        return HttpResponse(json.dumps(errorData), content_type="application/json")

    return HttpResponse(json.dumps("error, no request"), content_type="application/json")
        
@csrf_exempt
def thorpedoUrl(request):
    return HttpResponse(json.dumps("error, no request"), content_type="application/json")
    # if request.is_ajax() and request.method == 'POST':
    #     errorData = check.checkUrl(request.FILES)
    #     return HttpResponse(json.dumps(errorData), content_type="application/json")

@csrf_exempt
def thorpedoDirect(request):
    
    if request.method == 'POST':
        errorData = check.checkDirect(request.POST['body'])
        return HttpResponse(json.dumps(errorData), content_type="application/json")

    return HttpResponse(json.dumps("error, no request"), content_type="application/json")
