from django.shortcuts import render, get_object_or_404, redirect
from .models import *
import json
from .serializer import *
from datetime import datetime
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from django.contrib.auth import login,logout, get_user_model,authenticate
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from .form import PostForm

from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, InvalidPage

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

        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('index0')
        else:
            return HttpResponse('你的密碼應該要有英文和數字')
    else:
        form = CustomUserCreationForm()
    return render(request,'blog/signup.html',{'form':form})
def login_view(request):
    print(request.POST)
    if request.method=='POST':

        form = LoginForm(data=request.POST)

        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user = authenticate(request,username=username,password=password)

            print (user)
            if user is not None:
                login(request,user)
            else:
                return JsonResponse({'found':False})
            if 'next' in request.POST:
                return render(request.POST.get("next"),'blog/index0.html',{'form':form})
            else:
                return redirect('index0')

    else:
        form = AuthenticationForm()
    return redirect('index0')
def logout_view(request):
    logout(request)
    return redirect('index0')
def profile(request):
    return render(request, 'blog/userprofile.html')
def filter(request):
   if request.method=='GET':
                query = request.GET.get('q')
                page= request.GET.get('page')
                district=request.GET.get('district')
                if district is not None:
                    district=district.split(',')
                print(district);
                sort=request.GET.get('sort')

                num_post=switch_demo((district,sort),query)
                print(num_post)
                paginator = Paginator(num_post, 3)
                temp=[]
                for x in num_post:
                    temp+=CNSExtraField.objects.filter(cnsx_id=x.id).values()
                try:
                     page = int(request.GET.get('page','1'))
                except ValueError:
                     page = 1
                try:
                     num_post = paginator.page(page)
                except (EmptyPage, InvalidPage):
                     num_post = paginator.page(1)


                num_post=json.dumps([{'id':i.id,'CHtitle':i.CHtitle,'ENGtitle':i.ENGtitle,'full_address':i.full_address,'telephone':i.telephone,'number':num_post.number,'count':num_post.paginator.num_pages} for i in num_post])

                context={'numpost':num_post,'exattr':list(temp)}

                return JsonResponse(context)
def switch_demo(argument,query):
        print(argument);
        if (argument[0] is None or argument[0] == [''])  and argument[1] is None:
            t=CNS.objects.filter(CHtitle__contains=query).order_by('id')
        elif (argument[0] is not None and argument[0] != ['']) and argument[1] is None:
            t=CNS.objects.filter(CHtitle__contains=query,district__in=argument[0]).order_by('id')
        elif (argument[0] is None or argument[0] == ['']) and argument[1] is not None:

            if argument[1] == 'popular':

                t=CNS.objects.filter(CHtitle__contains=query).order_by('-promote_rank')
            elif argument[1] == 'default':
                t=CNS.objects.filter(CHtitle__contains=query).order_by('promote_rank')
            else:
                t=CNS.objects.filter(CHtitle__contains=query).order_by('id')
        else:
            if argument[1] == 'popular':
                t=CNS.objects.filter(CHtitle__contains=query,district__in=argument[0]).order_by('-promote_rank')
            elif argument[1] == 'default':
                t=CNS.objects.filter(CHtitle__contains=query,district__in=argument[0]).order_by('promote_rank')
            else:
                t=CNS.objects.filter(CHtitle__contains=query,district__in=argument[0]).order_by('promote_rank')
        return t
def search0(request):

   if request.method=='POST':
        print(request.POST)

        query=request.POST.get('phrase')

        print(query)

        message = CNS.objects.filter(CHtitle__contains=query).values('CHtitle','full_address')[0:8]
        print(message)
        return JsonResponse({'message':list(message)})
   else:

        return render(request, 'blog/search0.html',{'me':[{"id":1,'keyx':'LK','name':'中國'},{"id":2,'keyx':'LW','name':'英國'},{"id":3,'keyx':'JR','name':'德國'},{"id":4,'keyx'
        :'SR','name':'法國'}]})
def index0(request):
        print(request)
        form=LoginForm()
        sform=CustomUserCreationForm()
        print('kvsodv')
        return render(request, 'blog/index0.html',{'form':form,'sform':sform})
def map(request):
        print(request)
        return render(request, 'blog/map.html')
