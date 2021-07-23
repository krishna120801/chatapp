from datetime import timedelta
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
import online_users.models
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Create your views here.
def register(request):
    if request.method=="POST":
        arr=[]
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)
            return redirect("home")
        else:
            username=request.POST['username']
            r = User.objects.filter(username__icontains=username)
            if '@' in username:
                arr.append("Please use underscore instead of @ in Username.")
            elif (r.count()):
                arr.append("Username already exists.")
            else:
                for msg in form.error_messages:
                    arr.append(form.error_messages[msg])
            return render(request,"registration.html",{"form":form,'messages':arr})
    form = UserCreationForm
    return render(request,"registration.html",{"form":form})
@receiver(user_logged_in)
def checkstatus(request,**kwargs):
    user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(minutes=0.2))
    users=(user for user in  user_status)
    context={'userss':users}
    return context
@login_required(login_url='/login/')
def home(request):
    if "firstname" in request.POST:
        request.user.first_name= request.POST["firstname"]
        request.user.save()
    if "email" in request.POST:
        request.user.email= request.POST["email"]
        request.user.save()
    return render(request,"home.html")
@login_required
def search(request):
    status=checkstatus(request)
    query= request.GET['query']
    if len(query)>71 or len(query)<1:
        search=User.objects.none()
        params = {'search': search}
    else:
        username = User.objects.filter(username__icontains=query)
        Nickname = User.objects.filter(first_name__icontains=query)
        search= username.union(Nickname)
        status["query"]=query
        status["itrsearch"]=search
        print(status)
    return render(request,"search.html",status)
@login_required
def chatlist(request):
    is_online=checkstatus(request)
    users=User.objects.exclude(username=request.user)
    is_online['users']=users
    return render(request,'chatlist.html',is_online)
@login_required(login_url="/login/")
def chat(request,room_name):
    is_online=checkstatus(request)
    is_online["room_name"]=room_name
    is_online["user"]=request.user
    return render(request,"chat.html",is_online)

