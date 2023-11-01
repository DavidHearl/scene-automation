from django.shortcuts import render, HttpResponse, redirect
from .models import Ship, Area
from .forms import AddItemForm


def ships_and_areas(request):
    ships = Ship.objects.all()
    areas = Area.objects.all()

    context = {
        'ships': ships,
        'areas': areas,
    }

    return render(request, 'front_end/front_end.html', context)


def add_item(request):
    if request.method == 'POST':
        form = AddItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = AddItemForm()

    context = {
        'form': form
    }

    return render(request, 'front_end/add_item.html', context)


def success_page(request):
    return render(request, 'front_end/success_page.html')
