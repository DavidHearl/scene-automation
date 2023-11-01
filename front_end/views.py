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
            ship = form.cleaned_data['ship']
            area_name = form.cleaned_data['area_name']

            if not ship:
                custom_ship_name = form.cleaned_data['custom_ship_name']
                custom_company = form.cleaned_data['custom_company']
                custom_contract_number = form.cleaned_data['custom_contract_number']
                ship = Ship(
                    name=custom_ship_name,
                    company=custom_company,
                    contract_number=custom_contract_number
                )
                ship.save()

            area = Area(ship=ship, area_name=area_name)
            area.save()

            return redirect('success_page')
    else:
        form = AddItemForm()

    context = {
        'form': form
    }

    return render(request, 'front_end/add_item.html', context)


def success_page(request):
    return render(request, 'front_end/success_page.html')
