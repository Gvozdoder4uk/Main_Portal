from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'relax_portal/index.html')

def panels(request):
    return render(request, 'relax_portal/info_panels.html')