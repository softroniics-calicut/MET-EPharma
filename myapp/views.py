from django.shortcuts import render,redirect
from .models import Pharmacy
from .models import user,product,booking,cart,Login, Prescription
from django.shortcuts import HttpResponse
from django.shortcuts import reverse
from django.contrib.auth import authenticate,login
from .forms import editproductform
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
# from django.contrib.auth import update_session_auth_hash

# Create your views here.


def registration (request):
    return render(request,'user/signuser.html')
def pharmacyreg(request):
    return render(request,'pharmacy/signpharmacy.html')


def regform(request):
    if request.method=='POST':
        name=request.POST['name']
        address= request.POST['address']
        email= request.POST['email']
        password=request.POST['password']
        phone_no = request.POST['phone_no']
        if Login.objects.filter(username=name).exists():
             return render(request,'user/signuser.html', {'message': "Username already exists"})
        if user.objects.filter(email=email).exists():
             return render(request,'user/signuser.html', {'message': "Email already exists"})
        if user.objects.filter(phone_no=phone_no).exists():
             return render(request,'user/signuser.html', {'message': "Phone number already exists"})
        login=Login.objects.create(username=name,password=password,type="user",status="APPROVED")
        login.save()
        # logindata=Login.objects.get(id=login.id)
        data1=user.objects.create(name=name,address=address,email=email,phone_no=phone_no,loginid=login)
        data1.save()
        return render(request,'lognew.html')
    else:
        return render(request,'user/signuser.html')
def pharmacyregform(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone_no=request.POST['phone_no']
        address=request.POST['address']
        password=request.POST['password']
        if Login.objects.filter(username=name).exists():
                 return render(request,'pharmacy/signpharmacy.html', {'message': "Username already exists"})
        if Pharmacy.objects.filter(email=email).exists():
                 return render(request,'pharmacy/signpharmacy.html', {'message': "Email already exists"})
        if Pharmacy.objects.filter(phone_no=phone_no).exists():
             return render(request,'pharmacy/signpharmacy.html', {'message': "Phone number already exists"})
        login = Login.objects.create(username=name, password=password, type="pharmacy")
        login.save()
        data2=Pharmacy.objects.create(name=name,email=email,address=address,phone_no=phone_no,loginid=login)
        data2.save()
        return render(request, 'lognew.html')
    else:
        return render(request, 'pharmacy/signpharmacy.html')





def log(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        try:
            admin_user = authenticate(request, username=username, password=password)
            if admin_user is not None and admin_user.is_staff:
                login(request, admin_user)
                return redirect(reverse('admin:index'))
            data=Login.objects.get(username=username,password=password)
            if data.type == "user" and data.status=='APPROVED' :
                request.session['id']=data.id
                return redirect(userpage)
            elif data.type =="pharmacy" and data.status=='APPROVED':
                request.session['id'] = data.id
                return redirect(pharpage)
            else:
                context = {
                    'message': ' wait for admins approval'
                }
                return render(request,'lognew.html',context)

        except Exception:
                         context = {
                             'message2': 'invalid credentials'
                         }
                         return render(request,'lognew.html',context)
    else:
        return render(request,'lognew.html')






def logout(request):
     if 'id' in request.session:
         request.session.flush()
         return redirect(log)




####################################################        PHARMACY         ##########################################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pharpage(request):
    if 'id' in request.session:
        userid = request.session['id']
        use1 = Login.objects.get(id=userid)
        return render(request, 'pharmacy/pharmacyhome.html',{'data3': use1})
    else:
        return redirect(log)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addproduct(request):
    if 'id' in request.session:
        data1=request.session['id']
        data=Login.objects.get(id=data1)
        userdata=Pharmacy.objects.get(loginid=data)
        image=request.FILES['image']
        medicinename=request.POST['medicinename']
        stock = request.POST['stock']
        price=request.POST['price']
        company=request.POST['company']
        type=request.POST['type']
        if 'prescription' in request.POST :
            prescription = request.POST['prescription']
        # Convert prescription value to boolean
        else :
            prescription='False'
        data=product.objects.create(
            pharmacyid=userdata,
            image=image,
            medicinename=medicinename,
            quantity = stock,
            price=price,
            company=company,
            type=type,
            prescription_required=prescription
            )
        data.save()
        return redirect(viewproduct)
    else:
         return redirect(log)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewproduct(request):
    if 'id' in request.session:
        data1=request.session['id']
        logindata=Login.objects.get(id=data1)
        userdata=Pharmacy.objects.get(loginid=logindata)
        data=product.objects.filter(pharmacyid=userdata)
        items_per_page = 5
        # Use Paginator to paginate the products
        paginator = Paginator(data, items_per_page)
        page = request.GET.get('page', 1)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver the last page of results
            products = paginator.page(paginator.num_pages)
        return render(request,'pharmacy/viewproduct.html',{'products':products})
    else:
        return redirect(log)

def searchproduct(request):
    if request.method=='GET':
        result=request.GET.get('search')
        if result:
            products = product.objects.all().filter(medicinename__icontains=result)
            return render(request,'pharmacy/viewproduct.html',{'products':products})





def editproductt(request,id):
    if 'id' in request.session:
        use2 = product.  objects.get(id=id)
        print(use2)
        userpr2 = editproductform(instance=use2)
        if request.method=='POST':
            userpr2=editproductform(request.POST,request.FILES,instance=use2)
            if userpr2.is_valid():
                userpr2.save()
                return redirect(viewproduct)
        else:
            return render(request,'pharmacy/editproduct.html',{'form2':userpr2,'user1':use2})
    else:
        return redirect(log)

def deleteproduct(request,id):
    data=product.objects.get(id=id)
    data.delete()
    return redirect(viewproduct)

def editpharmacyprofile(request):
    if 'id' in request.session:
        use_id =request.session['id']
        data=Login.objects.get(id=use_id)
        userdata=Pharmacy.objects.get(loginid=data)
        if request.method == 'POST':
            newshopname=request.POST['newshopname']
            newemail=request.POST['newemail']
            newaddress=request.POST['newemail']
            newphone_no=request.POST['newphone_no']
            print(userdata)
            print(data)
            userdata.name=newshopname
            userdata.adress=newaddress
            userdata.email=newemail
            userdata.phone_no=newphone_no
            data.username=newshopname
            userdata.save()
            data.save()
            return redirect(pharpage)
        else:
            return render(request, 'pharmacy/pharmacyeditprofile.html', {'data':userdata})
    else:
        return redirect(log)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def phar_history(request):
    if 'id' in request.session:
        id =request.session['id']
        data=Login.objects.get(id=id)
        userdata=Pharmacy.objects.get(loginid=data)
        data5=booking.objects.filter(medicinename__pharmacyid=userdata)
        items_per_page = 10
        # Use Paginator to paginate the products
        paginator = Paginator(data5, items_per_page)
        page = request.GET.get('page', 1)

        try:
            bookings = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page
            bookings = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver the last page of results
            bookings = paginator.page(paginator.num_pages)
    return render(request,'pharmacy/history.html',{'result':bookings})



###################################################       USER        ###########################################################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userpage(request):
    if 'id' in request.session:
        userid = request.session['id']
        use1=Login.objects.get(id=userid)
        return render(request, 'user/userhome.html', {'data2': use1})
    else:
        return redirect(log)


def changepsw(request):
    return render(request,'user/changepsw.html')


def changepassword(request):
    if 'id' in request.session:
        data6=request.session['id']
        if request.method == "POST":
           currentpsw = request.POST['cpsw']
           newpsw=request.POST['npsw']
           conpsw = request.POST['cnpsw']
           try:
              data7 =Login.objects.get(id=data6)
              if newpsw==conpsw:
                      data7.password=newpsw
                      data7.save()
                      context = {
                          'message': 'password change successfully'
                      }
                      return render(request, 'user/userhome.html', context)
              else:
                 return HttpResponse(" password does not match")
           except Exception:
                return HttpResponse(" error")
    else:
         return redirect(log)

def editprofile(request):
    if 'id' in request.session:
        user_id = request.session['id']
        data = Login.objects.get(id=user_id)
        userdata = user.objects.get(loginid=data)
        if request.method=='POST':
            newname = request.POST['newname']
            newemail = request.POST['newemail']
            newaddres = request.POST['newaddress']
            newphone_no = request.POST['newphone_no']

            userdata.name = newname
            userdata.email = newemail
            userdata.address = newaddres
            userdata.phone_no = newphone_no
            data.username= newname
            userdata.save()
            data.save()
            return redirect(userpage)
        else:
            return render(request, 'user/editprofile.html', {'data': userdata})

    else:
        return redirect(log)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
        return render(request,'user/userhome.html')

def view_pharmacy(request):
    pharmacy_data = Pharmacy.objects.all()
    items_per_page = 5

    # Use Paginator to paginate the products
    paginator = Paginator(pharmacy_data, items_per_page)
    page = request.GET.get('page', 1)

    try:
        pharmacy = paginator.page(page)
    except PageNotAnInteger:

        pharmacy = paginator.page(1)
    except EmptyPage:

        pharmacy = paginator.page(paginator.num_pages)
    return render(request, 'user/pharmacy.html', {'pharmacy':pharmacy})

def pharmacy_search(request):
        if request.method=='GET':
            result=request.GET.get('search')
            if result:
                pharmacy = Pharmacy.objects.filter(
                    Q(name__icontains=result) |
                    Q(address__icontains=result)
                )
                return render(request,'user/pharmacy.html',{'pharmacy':pharmacy})
           
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def store(request):
    data = product.objects.all()
    items_per_page = 9

    # Use Paginator to paginate the products
    paginator = Paginator(data, items_per_page)
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        products = paginator.page(paginator.num_pages)
    return render(request, 'user/store.html', {'products':products})

def prescription(request,id):
    if 'id' in request.session:
        useid=request.session['id']
        user2=Login.objects.get(id=useid)
        userdata=user.objects.get(loginid=user2)
        product_data=product.objects.get(id=id)
        if request.method == 'POST':
            prescription = request.FILES['prescription']
            data = Prescription.objects.create(file=prescription, medicine_id=product_data)
            data.save()
            quantity_range = range(1, 11)
            requested_quantity = int(request.POST['quantity'])
            if requested_quantity > product_data.quantity:
                context = {
                    'message': "Out Of Stock",
                    'quantity_range':quantity_range,
                    'medicine': product_data
                }
                return render(request, 'user/book.html', context)

            # Check if the medicine is already in the cart
            if cart.objects.filter(medicineid=product_data, userid=userdata).exists():
                return redirect(alreadycart)
            else:
                # Add the medicine to the cart
                data = cart.objects.create(userid=userdata, medicineid=product_data, quantity=requested_quantity)
                data.save()

                return redirect(view_cart)
    else:
        return redirect(log)


def book(request,id):
    if 'id' in request.session:
        data=product.objects.get(id=id)
        quantity_range = range(1, 11)
        context = {
            'quantity_range':quantity_range,
            'medicine':data
        }
        return render(request,'user/book.html', context)



def succsess(request):
    return render(request,'user/booksuccess.html')



def buymedicine(request):
    return render(request,'user/booksuccess.html')

def alreadycart(request):
    return render(request, 'user/cartalready.html')

def Add_cart (request,id):
    if 'id' in request.session:
        useid=request.session['id']
        user2=Login.objects.get(id=useid)
        userdata=user.objects.get(loginid=user2)
        medicine=product.objects.get(id=id)
        quantity_range = range(1, 11)
        # Check if the requested quantity is greater than the available quantity
        requested_quantity = int(request.POST['quantity'])
        if requested_quantity > medicine.quantity:
            context = {
                'message': "Out Of Stock",
                'quantity_range':quantity_range,
                'medicine': medicine
            }
            return render(request, 'user/book.html', context)

        # Check if the medicine is already in the cart
        if cart.objects.filter(medicineid=medicine, userid=userdata).exists():
            return redirect(alreadycart)
        else:
            # Add the medicine to the cart
            data = cart.objects.create(userid=userdata, medicineid=medicine, quantity=requested_quantity)
            data.save()

            return redirect(view_cart)
    else:
        return redirect(log)
def cartdelete(request,id):
    if 'id' in request.session:
        useid = request.session['id']
        user2 = Login.objects.get(id=useid)
        userdata=user.objects.get(loginid=user2)
        data1=cart.objects.get(medicineid=id,userid=userdata)
        print(data1)
        data1.delete()
        data = cart.objects.filter(userid=userdata)
        return redirect(view_cart)
    else:
        return redirect(log)




def history (request):
    if 'id' in request.session:
        useid=request.session['id']
        user1=Login.objects.get(id=useid)
        userdata=user.objects.get(loginid=user1)
        history=booking.objects.filter(name=userdata)
        items_per_page = 5

        # Use Paginator to paginate the products
        paginator = Paginator(history, items_per_page)
        page = request.GET.get('page', 1)

        try:
            bookings = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page
            bookings = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver the last page of results
            bookings = paginator.page(paginator.num_pages)
        return render(request, 'user/history.html', {'hist': bookings})
    else:
        return redirect(log)




def view_cart(request):
    if 'id' in request.session:
        use1=request.session['id']
        use2=Login.objects.get(id=use1)
        userdata = user.objects.get(loginid=use2)
        view=cart.objects.filter(userid=userdata)
        return render(request,'user/viewcart.html',{'view':view})
def payment(request):
    if 'id' in request.session:
        userid=request.session['id']
        user1 =Login.objects.get(id=userid)
        userdata=user.objects.get(loginid=user1)
        cart_items = cart.objects.filter(userid=userdata)
        total_amount = 0
        for i in cart_items:
            total_amount += i.medicineid.price * i.quantity
        print(total_amount)
        context = {
            'total_amount':total_amount
        }
        return render(request,'user/payment.html', context)

def booking_confirm(request):
    if 'id' in request.session:
        userid = request.session['id']
        user1 = Login.objects.get(id=userid)
        userdata = user.objects.get(loginid=user1)
        cart_items = cart.objects.filter(userid=userdata)

        total_amount = 0
        for item in cart_items:
            total_amount += item.medicineid.price * item.quantity

            # Check if a prescription exists for the current item's medicine
            try:
                prescription = Prescription.objects.get(medicine_id=item.medicineid)
            except Prescription.DoesNotExist:
                prescription = None
            except MultipleObjectsReturned:
    # Handle multiple prescriptions for the same medicine
                prescriptions = Prescription.objects.filter(medicine_id=item.medicineid)
    # You may need additional logic here to decide which prescription to use
                prescription = prescriptions.first() 
            booking_entry = booking.objects.create(
                cart_id=item,  
                name=userdata,
                medicinename=item.medicineid,
                quantity=item.quantity,
                total_amount=item.medicineid.price * item.quantity,
                prescription_id=prescription if prescription else None
            )
            print(booking_entry.name)
            
            booking_entry.save() 
            booked_medicine = item.medicineid
            booked_medicine.quantity -= item.quantity
            booked_medicine.save()
        
        cart_items.delete()
        
        return render(request, 'user/booksuccess.html', {'total_amount': total_amount})
    else:
        return redirect(log)


def searchbar(request):
    if request.method=='GET':
        result=request.GET.get('search')
        if result:
            products = product.objects.filter(
                Q(medicinename__icontains=result) |
                Q(pharmacyid__address__icontains=result)
            )
            return render(request,'user/searchresult.html',{'products':products})
        else:
            print("no information to show")
            return render(request,'user/searchresult.html',{})


