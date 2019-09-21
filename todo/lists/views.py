from django.shortcuts import render, redirect
#from django.http import HttpResponse

from lists.models import Item

def enter_item(req):
    new_item = req.POST['add_todo']
    if new_item:
        Item.objects.create(text=new_item)

def home(req):
    #return HttpResponse('<html><title>ToDo lists</title></html>')
    return render(req, 'lists/home.html')

def list(req):
    items = Item.objects.all()
    return render(req, 'lists/list.html', {'items': items})

def new_list(req):
    enter_item(req)
    return redirect('/lists/unique-name/')

