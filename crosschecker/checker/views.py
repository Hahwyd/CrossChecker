from django.shortcuts import render
import logging
from django.http import HttpResponse

# Create your views here.

logger = logging.getLogger("checker")

#Used as test only if not working, otherwise delete
'''def my_view(request):
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    return HttpResponse('Hello, world!')'''
