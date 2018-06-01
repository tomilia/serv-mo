from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from datetime import datetime
from django.http import JsonResponse
from django.core.serializers import serialize
from django.contrib.auth import login,logout, get_user_model
from django.contrib.auth.decorators import login_required
#from .form import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from .form import PostForm
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.
def post_list(request):
    query = Post.objects.all()
    print (query)
    response= render(request, 'blog/post_list.html', {'posts':query})
    visits = int(request.COOKIES.get('visits', '0'))

    # Does the cookie last_visit exist?
    if 'last_visit' in request.COOKIES:

        print ("Cookie:{}".format(request))
        last_visit = request.COOKIES['last_visit']
        # Cast the value to a Python date/time object.
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        print((datetime.now() - last_visit_time).days)
        # If it's been more than a day since the last visit...
        if (datetime.now() - last_visit_time).seconds > 5:
            # ...reassign the value of the cookie to +1 of what it was before...
            response.set_cookie('visits', visits+1)
            # ...and update the last visit cookie, too.
            response.set_cookie('last_visit', datetime.now())
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        response.set_cookie('last_visit', datetime.now())
    print(response)
    return response
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    request.session['posts'] = pk
    print(request.session.get('posts',default=None))
    res= render(request, 'blog/post_detail.html', {'post': post})

    return res
#@login_required(login_url="login")
#def post_ack(request):
#    if request.method=="POST":
#        form = PostForm(request.POST,request.FILES)
#        if form.is_valid():
#           post = form.save(commit=False)
#           post.author = request.user
#           post.published_date = timezone.now()
#           post.save()
#           return redirect('post',pk=post.pk)
#    else:
#        form = PostForm()
#        return render(request, 'blog/post_ack.html', {'form': form})

#def post_edit (request,pk):
#    print('odssck')
#    post = get_object_or_404(Post, pk=pk)
#    if request.method == "POST":
#        form = PostForm(request.POST, instance=post)
#        if form.is_valid():
#            post = form.save(commit=False)
#            post.author = request.user
#            post.published_date = timezone.now()
#            post.save()
#            print('odsck')
#            return redirect('post', pk=post.pk)
#    else:
#        form = PostForm(instance=post)
#    return render(request, 'blog/post_ack.html', {'form': form})
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request,'blog/signup.html',{'form':form})
def login_view(request):
    if request.method=='POST':
        print(request.POST)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            print(request.POST)
            if 'next' in request.POST:
                return render(request.POST.get("next"),'blog/index0.html',{'form':form})
            else:
                return redirect('index0')

    else:
        form = AuthenticationForm()
    return render(request,'blog/index0.html',{'form':form,'errorfield':True})
def logout_view(request):
    logout(request)
    return redirect('index')
#def ajax(request):
#
#    if request.method=='POST':
#        print(request.POST)
#
#        query=request.POST.get('phrase')
#
#        message = Post.objects.filter(title__contains=query).values('title','author')[0:8]
#        print(message)
#        return JsonResponse({'message':list(message)})
#    else:
#        print ("Cookie:{}".format(request.COOKIES ))
#        query = request.GET.get('q')
#        message = Post.objects.filter(title__contains=query).values('title','author')[0:8]
#
#        return render(request, 'blog/search.html',{'message':list(message)})
def index0(request):
        print(request)
        return render(request, 'blog/index0.html')
def search0(request):
        print(request)
        return render(request, 'blog/search0.html')
