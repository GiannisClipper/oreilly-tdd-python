from django.shortcuts import render, redirect
#from django.http import HttpResponse

from lists.models import Item

def home_page(req):
    #return HttpResponse('<html><title>ToDo lists</title></html>')
    if req.method == 'POST':
        new_item = req.POST['add_todo']
        if new_item:
            Item.objects.create(text=new_item)

        return redirect('/')

    items = Item.objects.all()
    return render(req, 'lists/home.html', {'items': items})
