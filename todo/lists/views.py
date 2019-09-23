from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
#from django.http import HttpResponse

from lists.models import Item, List


def home(req):
    #return HttpResponse('<html><title>ToDo lists</title></html>')
    return render(req, 'lists/home.html')


def view_list(req, list_id, error=None):
    listOfItems = List.objects.get(id=list_id)
    items = Item.objects.filter(list=listOfItems)
    return render(req, 'lists/list.html', {'items': items, 'list_id': list_id, 'error': error})


def new_list(req):
#    new_item_text = req.POST['add_todo']
#    if new_item_text:
#        listOfItems = List.objects.create()
#        Item.objects.create(text=new_item_text, list=listOfItems)
#        return redirect(f'/lists/{listOfItems.id}/')
#    else:
#        return redirect('/')

    listOfItems = List.objects.create()
    item = Item(text=req.POST['add_todo'], list=listOfItems)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        listOfItems.delete()
        error = 'Empty items not allowed'
        return render(req, 'lists/home.html', {'error': error})
    return redirect(f'/lists/{listOfItems.id}/')

def add_item(req, list_id):
#    new_item_text = req.POST['add_todo']
#    if new_item_text:
#        listOfItems = List.objects.get(id=list_id)
#        Item.objects.create(text=new_item_text, list=listOfItems)
#    return redirect(f'/lists/{list_id}/')

    listOfItems = List.objects.get(id=list_id)
    item = Item(text=req.POST['add_todo'], list=listOfItems)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        error = 'Empty items not allowed'
        return view_list(req, list_id, error)
        #return render(req, 'lists/home.html', {'error': error})
    return redirect(f'/lists/{listOfItems.id}/')
