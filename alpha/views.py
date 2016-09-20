from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from chat_app import settings
from chat_app import Kernel
from django.contrib.auth.models import User
from .models import Chat

kernel = Kernel()
kernel.learn("chat_app/std-startup.xml")
kernel.respond("load aiml")

kernel.respond("Hi")
kernel.learn("std-startup.xml")

def askquestion(stringinput):
    return kernel.respond(stringinput)

chatbotuser = User.objects.get(username='chatbot')



def Login(request):
    Chat.objects.all().delete()
    next = request.GET.get('next', '/home/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Account is not active at the moment.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    return render(request, "alpha/login.html", {'next': next})

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def Home(request):
    c = Chat.objects.all()
    return render(request, "alpha/home.html", {'home': 'active', 'chat': c})

def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(user=request.user, message=msg)
        chatbotresponse = Chat(user=chatbotuser, message=askquestion(str(msg)))
        if msg != '':
            c.save()
        chatbotresponse.save()
        return JsonResponse({ 'msg': msg, 'user': c.user.username })
    else:
        return HttpResponse('Request must be POST.')

def Messages(request):
    c = Chat.objects.all()
    return render(request, 'alpha/messages.html', {'chat': c})