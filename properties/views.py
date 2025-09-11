from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties
# Cache this view for 15 minutes (900 seconds)
@cache_page(60 * 15)
def property_list(request):
    properties = get_all_properties
    return JsonResponse(list(properties), safe=False) #data


# "return JsonResponse({"
