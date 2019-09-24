from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
#from django.http import HttpResponse

from lists.models import Item, List


def home(req):
    #return HttpResponse('<html><title>ToDo lists</title></html>')
    return render(req, 'lists/home.html')


def new_list(req):
    listOfItems = List.objects.create()

    item = Item(text=req.POST['add_todo'], list=listOfItems)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        listOfItems.delete()
        error = 'Empty items not allowed'
        return render(req, 'lists/home.html', {'error': error})

    return redirect(listOfItems)
    #or return redirect('view_list', listOfItems.id)
    #or return redirect(f'/lists/{listOfItems.id}/')



def view_list(req, list_id, error=None):
    listOfItems = List.objects.get(id=list_id)
    items = Item.objects.filter(list=listOfItems)
    error = None

    if req.method == 'POST':
        item = Item(text=req.POST['add_todo'], list=listOfItems)
        try:
            item.full_clean()
            item.save()
        except ValidationError:
            error = 'Empty items not allowed'

    return render(req, 'lists/list.html', {'list_id': list_id, 'items': items, 'error': error})
