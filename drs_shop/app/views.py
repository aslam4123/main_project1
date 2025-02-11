from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse,JsonResponse

 

# Create your views here.


def shp_login(req):
    if 'drs_shop' in req.session:
        return redirect(shp_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['pswd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['drs_shop']=uname   #create session
                return redirect(shp_home)
            else:
                login(req,data)
                req.session['user']=uname   #create session
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(shp_login)
    
    else:
        return render(req,'login.html')

def shp_login1(req):
    if 'drs_shop' in req.session:
        return redirect(shp_home)
    if 'user' in req.session:
        return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['pswd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['drs_shop']=uname   #create session
                return redirect(shp_home)
            else:
                login(req,data)
                req.session['user']=uname   #create session
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(shp_login)
    
    else:
        return render(req,'login.html')

def shp_home(req):
    if 'drs_shop' in req.session:
        data=Product.objects.all()
        return render(req,'shop/home.html',{'data':data})
    else:
        return redirect(shp_login)

def products(req):
    if 'drs_shop' in req.session:
        data=Product.objects.all()
        return render(req,'shop/Products.html',{'data':data})
    else:
        return redirect(shp_login)
    
def shp_logout(req):
    req.session.flush()          #delete session
    logout(req)
    return redirect(shp_login)

def add_prod(req):
    if 'drs_shop' in req.session:
        if req.method=='POST':
            prd_id=req.POST['prd_id']
            prd_name=req.POST['prd_name']
            prd_price=req.POST['prd_price']
            ofr_price=req.POST['ofr_price']
            img=req.FILES['img']
            prd_dis=req.POST['prd_dis']
            sizes = req.POST.getlist('sizes')
            quantity = int(req.POST['quantity'])  # Fetch quantity from form

            product = Product.objects.create(
                pro_id=prd_id,
                name=prd_name,
                price=prd_price,
                ofr_price=ofr_price,
                img=img,
                dis=prd_dis,
                quantity=quantity  # Add quantity to the product
            )

            for size in sizes:
                size_obj, created = Size.objects.get_or_create(size=size)
                product.sizes.add(size_obj)

            return redirect(add_prod)
        else:
            all_sizes = Size.objects.all()
            return render(req, 'shop/add_pro.html', {'all_sizes': all_sizes})
    else:
        return redirect(shp_login)
    
def edit_prod(req,pid):
    if 'drs_shop' in req.session:
        if req.method=='POST':
            prd_id=req.POST['prd_id']
            prd_name=req.POST['prd_name']
            prd_price=req.POST['prd_price']
            ofr_price=req.POST['ofr_price']
            prd_dis=req.POST['prd_dis']
            img=req.FILES.get('img')
            sizes = req.POST.getlist('sizes')  # selected sizes
            quantity = req.POST['quantity']  # quantity

            # Fetch the product to edit
            product = get_object_or_404(Product, id=pid)

            # Update product fields
            product.pro_id = prd_id
            product.name = prd_name
            product.price = prd_price
            product.ofr_price = ofr_price
            product.dis = prd_dis
            product.quantity = quantity  # Update quantity

            # Update image if a new one is uploaded
            if img:
                product.img = img

            # Update sizes
            product.sizes.clear()  # Clear existing sizes
            for size in sizes:
                size_obj, _ = Size.objects.get_or_create(size=size)
                product.sizes.add(size_obj)

            product.save()  # Save all changes
            return redirect(shp_home)
        else:
            all_sizes = Size.objects.all()  # Fetch all available sizes
            product = get_object_or_404(Product, pk=pid)  # Fetch the product to edit
            return render(req, 'shop/edit.html', {'product': product, 'all_sizes': all_sizes})
    else:
        return redirect(shp_login)
def delete_prod(req,pid):
    data=Product.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    return redirect(shp_home)

def bookings(req):
    buy=Buy.objects.all()[::-1]
    return render(req,'shop/bookings.html',{'buy':buy})





#------------------------user--------------------------------

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        # send_mail('user registration','eshop account created', settings.EMAIL_HOST_USER, [email])
        try:
           
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            return redirect(shp_login)
        except:
            messages.warning(req,'User already exists.')
            return redirect(register)
    else:
        return render(req,'user/register.html')

def main(req):
    data = Product.objects.all()  # Get all products from the database
    return render(req, 'main.html', {'data': data, 'user': req.user})

def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/home.html',{'data':data})
    else:
        return redirect(shp_login)

def user_products(req):
    if 'user' in req.session:
        data=Product.objects.all()
        return render(req,'user/user_products.html',{'data':data})
    else:
        return redirect(shp_login)


def view_pro(req, pid):
    # Get the product by its ID
    product = get_object_or_404(Product, pk=pid)

    # Pass the product data to the template
    return render(req, 'user/view_pro.html', {'data': product})



def add_to_cart(req, pid):
    if 'user' not in req.session:
        return redirect('shp_login')

    # Fetch the product and user
    product = Product.objects.get(pk=pid)
    user = User.objects.get(username=req.session['user'])

    # Get the selected size from the POST data
    size_id = req.POST.get('size')
    selected_size = Size.objects.get(id=size_id) if size_id else None  # Fetch the size object
    quantity = int(req.POST.get('quantity', 1))  # Get selected quantity

    if not selected_size:
        return HttpResponse("Size is required", status=400)

    # Check if the product with the selected size already exists in the cart
    cart_item, created = Cart.objects.get_or_create(user=user, product=product, size=selected_size)

    if created:
        # If it's a new cart item, set the total price based on quantity
        cart_item.quantity = quantity
        cart_item.total_price = quantity * product.ofr_price  # Set the total price
    else:
        # If the cart item already exists, simply update the quantity and total price
        cart_item.quantity += quantity  # Increment the existing quantity
        cart_item.total_price = cart_item.quantity * product.ofr_price  # Recalculate total price

    cart_item.save()

    # Decrease stock after adding to cart (this logic is based on how your stock system is designed)
    product.quantity -= quantity
    product.save()

    return redirect('view_cart')


def view_cart(req):
    if 'user' not in req.session:  # Ensure user is logged in
        return redirect('shp_login')

    user = User.objects.get(username=req.session['user'])

    # Use select_related to fetch related product and size data
    cart_det = Cart.objects.filter(user=user).select_related('product', 'size')

    # Calculate the total price for each cart item
    total_price = 0  # To calculate total price of all items in the cart
    for item in cart_det:
        item.total_price = item.product.ofr_price * item.quantity  # Calculate total price for each item
        total_price += item.total_price  # Add it to the grand total

    return render(req, 'user/cart.html', {'cart_det': cart_det, 'total_price': total_price})



def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_quantity = int(request.POST.get('new_quantity'))  # Get the new quantity from the form

        try:
            cart_item = Cart.objects.get(id=item_id, user=request.user)  # Get the cart item for the current user
            product = cart_item.product  # Get the associated product

            # Check if the new quantity is within stock limits
            if 1 <= new_quantity <= product.quantity:
                # Update quantity and recalculate total price
                cart_item.quantity = new_quantity
                cart_item.total_price = cart_item.quantity * product.ofr_price  # Recalculate total price

                # Save the updated cart item
                cart_item.save()
                messages.success(request, f"Quantity updated to {new_quantity}.")
            else:
                messages.error(request, f"Cannot update quantity. Max stock available: {product.quantity}.")
        except Cart.DoesNotExist:
            messages.error(request, "Item not found in your cart.")
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")

        return redirect('view_cart')  # Redirect back to the cart page

    return redirect('view_cart')  # If not a POST request, redirect back to the cart



def delete_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    product = cart_item.product

    # Restore stock when item is removed
    product.quantity += cart_item.quantity
    product.save()

    cart_item.delete()
    messages.success(request, "Item removed from cart. Stock updated.")
    return redirect('view_cart')

def user_buy(req,cid):
    user=User.objects.get(username=req.session['user'])
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    price=cart.product.ofr_price
    buy=Buy.objects.create(user=user,product=product,price=price)
    buy.save()
    return redirect(order)
def user_buy1(req,pid):
     user=User.objects.get(username=req.session['user'])
     product=Product.objects.get(pk=pid)
     price=product.ofr_price
     buy=Buy.objects.create(user=user,product=product,price=price)
     buy.save()
     return redirect(order)

def user_bookings(req):
    user=User.objects.get(username=req.session['user'])
    buy=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/user_bookings.html',{'buy':buy})



# Mock function to simulate email sending for verification
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'pswd_reset.html'
    email_template_name = 'pswd_reset_email.html'
    subject_template_name = 'pswd_reset_subject.txt'
    success_url = reverse_lazy('pswd_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'pswd_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'pswd_reset_confirm.html'
    success_url = reverse_lazy('pswd_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'pswd_reset_complete.html'





from django.shortcuts import render, redirect
from .form import OrderForm
from .models import Order

def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_success')  # Redirect to success page
    else:
        form = OrderForm()
    
    return render(request, 'user/product_booking.html', {'form': form})

def order_success(request):
    return render(request, 'user/order.html')






