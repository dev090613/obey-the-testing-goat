from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import Item, List
from .forms import ItemForm, ExistingListItemForm


def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        return render(request, "home.html", {"form": form})


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=our_list)

    if request.method == "POST":
        form = ExistingListItemForm(for_list=our_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(our_list)
    else:
        form = ExistingListItemForm(for_list=our_list)
    return render(request, "list.html", {"list": our_list, "form": form})
