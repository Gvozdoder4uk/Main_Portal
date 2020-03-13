from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'Main_Templates/index.html')

def daynight(request):
    return render(request, 'Main_Templates/DayNight.html')
