from django.shortcuts import render, redirect
#from django.http import HttpResponse

from lists.models import Item, List


def home(req):
    #return HttpResponse('<html><title>ToDo lists</title></html>')
    return render(req, 'lists/home.html')


def view_list(req, list_id):
    listOfItems = List.objects.get(id=list_id)
    items = Item.objects.filter(list=listOfItems)
    return render(req, 'lists/list.html', {'items': items, 'list_id': list_id})


def new_list(req):
    new_item_text = req.POST['add_todo']
    if new_item_text:
        listOfItems = List.objects.create()
        Item.objects.create(text=new_item_text, list=listOfItems)
        return redirect(f'/lists/{listOfItems.id}/')
    else:
        return redirect('/')


def add_item(req, list_id):
    new_item_text = req.POST['add_todo']
    if new_item_text:
        listOfItems = List.objects.get(id=list_id)
        Item.objects.create(text=new_item_text, list=listOfItems)

    return redirect(f'/lists/{list_id}/')