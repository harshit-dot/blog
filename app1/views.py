from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# import pyautogui
from django.contrib.auth.models import  User
from django.core.files.storage import FileSystemStorage

#
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        password1=request.POST['password1']
        if password1!=password:
#             pyautogui.alert('password not matched')
            return redirect('/')

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('/')
        else:
#             pyautogui.alert('username or password not matched')
            return redirect('/')
def main(request):
    from .models import blogpost
    blog=blogpost.objects.all()
    return render(request, 'app1/index.html', {'blog': blog })
def createblog(request,names):
    if request.method=='POST':
        print(names)
        try:
            image = request.FILES['image']
            fs=FileSystemStorage()
            filename=fs.save(image.name,image)
            url=fs.url(filename)
        except:
#             pyautogui.alert('Upload image')
            bar = get_user_model().objects.get(username=names)
            return render(request, 'app1/createblog.html', {'bar': bar})
        catagoy=request.POST['catagory1']
        catagory=catagoy.lower()
        title=request.POST['title']
        textarea=request.POST['textarea1']
        print(url)
        name1=request.POST['name']
        if catagoy=='' or title=='' or textarea=='' or name1=='':
#             pyautogui.alert('enter all the fields')
            bar = get_user_model().objects.get(username=names)
            return render(request, 'app1/createblog.html', {'bar': bar})
        from .models import blogpost
        blog=blogpost(catagory=catagory, title=title, textarea=textarea, email=name1, name=names, image=url)
        blog.save()
        return redirect('/')
    else:
        bar=get_user_model().objects.get(username=names)
        return render(request, 'app1/createblog.html' , {'bar':bar})
def about(request):
    return render(request, 'app1/about.html')
def contact(request):
    if request.method=='POST':
        email=request.POST['email']
        regarding=request.POST['catagory']
        text=request.POST['textarea']
        if email=='' or regarding=='' or text=='':
#             pyautogui.alert('Enter All The Fields')
            return render(request, 'app1/contact.html')
        send_mail(
            'we have just get your query (BLOGGERS POINT)',
            'we get your query, we will reply it as soon as possible till enjoy blogging....',
            'khannaharshit064@gmail.com',
            [email],
            fail_silently=False,
        )
        from .models import contact
        con=contact(email=email, regarding=regarding, text=text)
        con.save()
#         pyautogui.confirm(' send')
        return redirect('/')
    else:
        return render(request, 'app1/contact.html')

def signup(request):
    if request.method=='POST':
        username=request.POST['username']

        password=request.POST['password']

        password1=request.POST['password1']
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        email=request.POST['email']
        if username=='' or password=='' or password1=='' or first_name=='' or last_name=='' or email=='':
#             pyautogui.alert('Enter All The Fields')
            return redirect('/')


        if password1!=password:
#             pyautogui.alert(request, 'password not matched')
            return redirect('/')

        send_mail(
            'Wow you have just signed up in BLOGGERS POINT',
            'congratulations your account is now setup. you can login through the main website and enjoy by creating more blogs.....',
            'khannaharshit064@gmail.com',
            [email],
            fail_silently=False,
        )
        myuser = User.objects.create_user(username,email,password)
        myuser.first_name=first_name
        myuser.last_name=last_name
        myuser.save()
#         pyautogui.confirm('user created')
        return redirect('/')





def logout(request):
    auth_logout(request)
    return redirect('/')
def forgot(request):
    if request.method=='POST':
        email=request.POST['email']
        username=request.POST['username']
        # password=request.POST['password']
        # password1=request.POST['password1']
        # if password1!=password:
        #     pyautogui.alert('password did not matched')
        #     return redirect('/')
        bog=User.objects.get(username=username, email=email)
        if bog is None:
#             pyautogui.alert('username or email wrong')
            return redirect('/')
        # pyautogui.confirm('saved')
        # return redirect('/')
        harsh='this is the link, click it http://127.0.0.1:8000/forgotpass/'+str(bog.id)
        print(harsh)
        print(bog.password)
        send_mail(
            'click the link to change your password BLOGGERS POINT',
            harsh,
            'khannaharshit064@gmail.com',
            [email],
            fail_silently=False,
        )
#         pyautogui.confirm('mail has been sent to your email')
        return render(request, 'app1/forgot.html')

    else:
        return render(request, 'app1/forgot.html')
def search(request):
    searchtex=request.POST['search']

    print(searchtex)
    searchtext=searchtex.lower()
    print(searchtext)
    if len(searchtext)==0:
#         pyautogui.alert('enter something!')
        return redirect('/')
    from .models import blogpost
    blog=blogpost.objects.filter(catagory=searchtext)
    if len(blog)==0:
#         pyautogui.alert('not found anything')
        return redirect('/')
    else:
        return render(request,'app1/index.html', {'blog':blog})

def blogpost(request, id):
    from .models import blogpost
    blog=blogpost.objects.filter(ids=id)
    return render(request,'app1/blopost.html', {'blog':blog})
def forgotpass(request, id):


    bog = get_user_model().objects.get(id=int(id))
    return render(request, 'app1/forgetpass.html', {'bog': bog})
def changepassword(request,id):
    if request.method=='POST':
        password=request.POST['password']
        password1=request.POST['password1']
        if password!=password1:
#             pyautogui.alert("password not matched")
            bog = get_user_model().objects.get(id=int(id))
            return render(request, 'app1/forgetpass.html', {'bog': bog})
        bog = get_user_model().objects.get(id=int(id))
        bog.set_password(password)
        bog.save()
#         pyautogui.confirm('password saved')
        return render(request, 'app1/forgot.html')
def myprofile(request, name):
    bog=get_user_model().objects.get(username=name)
    print(name)
    from .models import image
    from .models import blogpost
    # iar=image.objects.get(names=name)
    har=blogpost.objects.filter(name=name)
    print(har)

    kar=len(har)
    return render(request,'app1/myprofile.html', {'bog': bog , 'har': har, 'kar':kar})
def deletepost(request,id):
    from .models import blogpost
    blog=blogpost.objects.get(ids=id)
    name=blog.name
    print(name)
    bog=get_user_model().objects.get(username=name)
    blog.delete()
    har = blogpost.objects.filter(name=name)
    print(har)
    kar = len(har)


    return render(request,'app1/myprofile.html',{'bog':bog,'har':har, 'kar':kar})

