from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def index(req):
    if not req.user.is_authenticated:
        if req.method == 'POST':
            username = req.POST['username']
            password = req.POST['password']

            user = authenticate(username=username, password=password)
            if user:
                if user.is_staff:
                    login(req, user)
                    return HttpResponseRedirect('/main')
                else:
                    return HttpResponse("You are not Authorized to access this panel.")
            else:
                return HttpResponse("Not logged in")
        else:
            return render(req, "authentication/login/index.html")
    else:
        return HttpResponseRedirect('/main')
