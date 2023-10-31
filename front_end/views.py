from django.shortcuts import render, HttpResponse

# Create your views here.
def say_hello(request):
    return render(request, 'front_end/front_end.html')
