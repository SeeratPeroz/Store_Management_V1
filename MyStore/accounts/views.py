from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import User


# Create your views here.

# Admin User
def register(request):
    if request.method == 'POST':
        Uname = request.POST['username']
        passwd = request.POST['password']
        passwd1 = request.POST['Password1']
        phone = request.POST['Phone']

        if User.objects.filter(username=Uname).exists():
            messages.info(request, "Username is taken!!!")
            return redirect("login")
        else:
            if User.objects.filter(userPhone=phone).exists():
                messages.info(request, "Please enter a unique Phone number")
                return redirect('login')
            else:
                if passwd == passwd1:
                    user = User.objects.create_superuser(username=Uname, userPhone=phone, password=passwd)
                    user.save()
                    messages.info(request, "Account has successfully created for " + Uname)
                    return redirect('login')
                else:
                    messages.info(request, "Password doesnt' match!!!")
                    return redirect('login')
    else:
        return render(request, "login", {})


# Staff User
def register_staff(request):
    if request.method == 'POST':
        Uname = request.POST['username']
        passwd = request.POST['password']
        passwd1 = request.POST['Password1']
        phone = request.POST['Phone']

        if User.objects.filter(username=Uname).exists():
            messages.info(request, "Username is taken!!!")
            return redirect("login")
        else:
            if User.objects.filter(userPhone=phone).exists():
                messages.info(request, "Please enter a unique Phone number")
                return redirect('login')
            else:
                if passwd == passwd1:
                    user = User.objects.create_superuser(username=Uname, userPhone=phone, password=passwd)
                    user.save()
                    messages.info(request, "Account has successfully created for " + Uname)
                    return redirect('login')
                else:
                    messages.info(request, "Password doesnt' match!!!")
                    return redirect('login')
    else:
        return render(request, "login", {})


# Creating account for cashier
@login_required
def create_Stuff(request):
    if request.method == 'POST':
        Fname = request.POST['empName']
        Epass = request.POST['empPass']
        Epass1 = request.POST['empPass1']
        Ephone = request.POST['empPhone']
        Eadd = request.POST['empAdd']

        if User.objects.filter(username=Fname).exists():
            messages.info(request, "Username already exits.")
            return redirect("create_stuff")
        else:
            if User.objects.filter(userPhone=Ephone).exists():
                messages.info(request, "Please enter a unique Phone number")
                return redirect("create_stuff")
            else:
                if Epass == Epass1:
                    EmpUser = User.objects.create_staff(username=Fname, userPhone=Ephone, userAdd=Eadd, password=Epass)
                    EmpUser.save()
                    messages.info(request, "Account has successfully created for " + Fname)
                    return redirect('create_stuff')
                else:
                    messages.info(request, "Password does not match.")
                    return redirect("create_stuff")
    else:
        return render(request, "create_stuff.html", {})


@login_required
def Search_Cashier(request):
    if request.method == 'POST':
        empNam = request.POST['sField']
        if User.objects.filter(username=empNam).exists():
            empDetails = User.objects.all().filter(username=empNam)
            return render(request, 'update_stuff.html', {'stf': empDetails})
        else:
            messages.info(request, 'Invalid User')
        return redirect('Search_Cashier')
    else:
        return render(request, 'update_stuff.html', {})


@login_required
def Update_Cashier(request):
    if request.method == 'POST':
        eName = request.POST['empName']
        Epass1 = request.POST['empPass']
        Ephone1 = request.POST['empPhone']
        Eadd1 = request.POST['empAdd']
        hidd = request.POST['hid']
        upd = User.objects.select_related().filter(username=eName).update(userPhone=Ephone1, userAdd=Eadd1)
        print(hidd)
        messages.info(request, 'Changes successfully made.')
        return redirect('Update_Cashier')
    else:
        return render(request, 'update_stuff.html', {})


def logout(request):
    auth.logout(request)
    return render(request, 'registration/login.html',{})