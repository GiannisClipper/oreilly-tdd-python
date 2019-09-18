from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(req):
    #return HttpResponse('<html><title>ToDo lists</title></html>')
    if req.method == 'POST':
        return render(req, 'lists/home.html', {
            'add_todo': req.POST.get('add_todo', ''),
        })
    else:
        return render(req, 'lists/home.html')