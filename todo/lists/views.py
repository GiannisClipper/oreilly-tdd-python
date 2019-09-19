from django.shortcuts import render, redirect
#from django.http import HttpResponse

from lists.models import Item

def enter_item(req):
    new_item = req.POST['add_todo']
    if new_item:
        Item.objects.create(text=new_item)

def home_page(req):
    #return HttpResponse('<html><title>ToDo lists</title></html>')
    if req.method == 'POST':
        enter_item(req)
        return redirect('/lists/unique_name')

    items = []
    return render(req, 'lists/home.html', {'items': items})

def list_page(req):
    if req.method == 'POST':
        enter_item(req)

    items = Item.objects.all()
    return render(req, 'lists/home.html', {'items': items})

