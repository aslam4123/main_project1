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
    return redirect(products)

def bookings(request):
    # Get all Buy objects with related product and user data
    buy = Buy.objects.select_related('product', 'user').all().order_by('-date')
    
    # Get all Order objects related to the Buy objects (assuming there's a way to link Buy to Order)
    orders = Order.objects.all()

    # Create combined data
    combined_data = zip(buy, orders)

    return render(request, 'shop/bookings.html', {'combined_data': combined_data})

    # View to delete a booking
def delete_bookings(request, order_id):
    # Fetch the booking (order) object
    order = get_object_or_404(Order, id=order_id)  # Assuming `Order` is your model
    order.delete()  # Delete the order from the database

    # Redirect back to the bookings page after deletion
    return redirect(bookings)  # Replace 'bookings' with the name of your bookings view URL






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




from django.db.utils import IntegrityError
from .models import Product, User, Size, Cart  # Ensure correct model imports

def add_to_cart(req, pid):
    if 'user' not in req.session:
        return redirect('shp_login')

    try:
        # Fetch product and user
        product = Product.objects.get(pk=pid)
        user = User.objects.get(username=req.session['user'])

        # Get selected size (even though stock is managed at the product level)
        size_id = req.POST.get('size')
        selected_size = Size.objects.get(id=size_id) if size_id else None

        # Get quantity
        quantity = int(req.POST.get('quantity', 1))
        if quantity <= 0:
            return HttpResponse("Quantity must be greater than zero.", status=400)

        # Check if the product with the selected size already exists in the cart
        cart_item, created = Cart.objects.get_or_create(user=user, product=product, size=selected_size)

        if created:
            cart_item.quantity = quantity  # Set quantity for a new cart item
        else:
            cart_item.quantity += quantity  # Increase quantity if already in cart

        # Update total price
        cart_item.total_price = cart_item.quantity * product.ofr_price  
        cart_item.save()

        return redirect('view_cart')

    except Product.DoesNotExist:
        return HttpResponse("Product not found.", status=404)

    except Size.DoesNotExist:
        return HttpResponse("Selected size not found.", status=404)

    except ValueError:
        return HttpResponse("Invalid quantity value.", status=400)











def view_cart(request):
    if 'user' not in request.session:  # Ensure user is logged in
        return redirect('shp_login')

    user = User.objects.get(username=request.session['user'])

    # Use select_related to fetch related product and size data
    cart_det = Cart.objects.filter(user=user).select_related('product', 'size')

    # Calculate the total price for each cart item
    total_price = 0  # To calculate total price of all items in the cart
    for item in cart_det:
        item.total_price = item.product.ofr_price * item.quantity  # Calculate total price for each item
        total_price += item.total_price  # Add it to the grand total

    return render(request, 'user/cart.html', {'cart_det': cart_det, 'total_price': total_price})






def delete_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    product = cart_item.product

    

    cart_item.delete()
    messages.success(request, "Item removed from cart. Stock updated.")
    return redirect('view_cart')

def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_quantity = request.POST.get('new_quantity')

        try:
            # Convert new quantity to integer
            new_quantity = int(new_quantity)

            # Ensure the quantity is greater than 0
            if new_quantity <= 0:
                messages.error(request, "Quantity must be at least 1.")
                return redirect('view_cart')

            cart_item = Cart.objects.get(id=item_id, user=request.user)
            product = cart_item.product  # Fetch associated product

            # Check if stock is sufficient
            if new_quantity > product.quantity:
                messages.error(request, f"Only {product.quantity} items in stock.")
                return redirect('view_cart')

            
            cart_item.quantity = new_quantity
            cart_item.total_price = cart_item.quantity * product.ofr_price  # Recalculate total price
            cart_item.save()

            messages.success(request, f"Quantity updated to {new_quantity}.")
            return redirect('view_cart')

        except ValueError:
            messages.error(request, "Invalid quantity value.")
        except Cart.DoesNotExist:
            messages.error(request, "Item not found in your cart.")
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")

    return redirect('view_cart')








from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Cart, Product, Order
from django.utils import timezone

from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Buy, Order, Cart, Product

def user_buy(request, cid):
    cart_item = get_object_or_404(Cart, id=cid, user=request.user)
    product = cart_item.product

    # Retrieve the selected size from the cart item, default to 'M' if not found
    selected_size = cart_item.size if cart_item.size else "M"  

    # Debugging print to check if the size is correctly retrieved
    print(f"Selected Size in Buy: {selected_size}")

    # Check if stock is available
    if cart_item.quantity > product.quantity:
        messages.error(request, f"Not enough stock available for {product.name}! Only {product.quantity} left.")
        return redirect('view_cart')

    # Reduce stock permanently
    product.quantity -= cart_item.quantity
    product.save()

    # Create an Order object
    order = Order.objects.create(
        name=request.user.username,  
        email=request.user.email,    
        phone_number="1234567890",
        shipping_address="Default Address",
        status="Processing",
        created_at=timezone.now(),
    )

    # Ensure quantity is not NULL
    quantity = cart_item.quantity

    # Save the order in `Buy`
    buy_order = Buy.objects.create(
        user=request.user,
        product=product,
        size=selected_size,  # Save the selected size
        quantity=quantity,
        price=product.ofr_price * cart_item.quantity,
        date=timezone.now()
    )

    # Remove the item from the cart after purchase
    cart_item.delete()

    messages.success(request, f"Order placed successfully for {product.name} (Size: {selected_size})!")
    return redirect('order')



from django.contrib import messages
from django.shortcuts import redirect
from .models import User, Product, Buy

def user_buy1(req, pid):
    user = User.objects.get(username=req.session['user'])  # Fetch logged-in user
    product = Product.objects.get(pk=pid)

    # Extract size and quantity from the request
    size = req.GET.get('size', 'M')  # Get size from URL parameter, default to 'M' if not provided
    quantity = int(req.GET.get('quantity', 1))  # Default to 1 if not provided in the URL

    print(f"Selected size: {size}")  # Debugging print

    # Check if there's enough stock available
    if product.quantity >= quantity:
        price = product.ofr_price * quantity  # Adjust price based on quantity
        
        # Create Buy object with size and quantity
        buy = Buy.objects.create(user=user, product=product, price=price, size=size, quantity=quantity)
        buy.save()

        # Decrease stock
        product.quantity -= quantity
        product.save()

        return redirect('order')  # Redirect after purchase
    else:
        messages.error(req, "Sorry, not enough stock available.")
        return redirect('view_cart')  # Redirect to view cart if stock is not enough



from django.shortcuts import render
from .models import Buy

def user_bookings(request):
    user = request.user  # Get the currently logged-in user

    # Fetch bookings related to this user
    bookings = Buy.objects.filter(user=user)  # Correct query

    return render(request, 'user/user_bookings.html', {'buy': bookings})

from django.shortcuts import render, redirect
from .models import *
def delete_booking(request, booking_id):
    if request.method == 'POST':
        # Get the booking (order)
        booking = Buy.objects.get(id=booking_id)
        
        # Access the product associated with the booking and restock it
        product = booking.product  # assuming Buy model has a foreign key to Product model
        
        # Increase the product stock by the quantity in the booking
        product.quantity += booking.quantity  # assuming Buy has a quantity field
        product.save()

        # Delete the booking
        booking.delete()

        # Redirect to the user's bookings page
        return redirect('user_bookings')





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

import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from .form import OrderForm
from .models import Order  # Assuming you have an Order model

# Razorpay client setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save the order form and create a new order in the database
            order = form.save()

            # Step 1: Create an order on Razorpay
            amount = 1000  # Calculate the total amount for the order, here it's 1000 paise (₹10)
            currency = 'INR'
            order_data = {
                'amount': amount * 100,  # Razorpay expects the amount in paise (100 paise = 1 INR)
                'currency': currency,
                'payment_capture': '1',  # 1 means automatic payment capture after successful payment
            }

            # Create the Razorpay order
            try:
                razorpay_order = razorpay_client.order.create(data=order_data)
                # Save the Razorpay order ID in your order model
                order.razorpay_order_id = razorpay_order['id']
                order.save()

                # Step 2: Pass the Razorpay order details to the template for frontend
                context = {
                    'order': order,
                    'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                    'razorpay_order_id': razorpay_order['id'],
                    'razorpay_amount': amount * 100,  # Amount in paise
                    'razorpay_currency': currency,
                }

                # Render the payment page for the user to complete the payment
                return render(request, 'user/payment.html', context)

            except razorpay.errors.BadRequestError as e:
                # Handle error if something goes wrong with creating the order on Razorpay
                return render(request, 'user/error_page.html', {'error': str(e)})

    else:
        form = OrderForm()

    return render(request, 'user/product_booking.html', {'form': form})




def order_success(request):
    return render(request, 'user/order.html')



from django.shortcuts import render, redirect
from .models import Order, Buy
import razorpay

def payment(request, order_id):
    try:
        # Fetch the order from the database using the order_id
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return render(request, 'error.html', {'message': 'Order not found'})

    # Fetch the associated 'buy' object (assuming it's related to the Order object)
    try:
        buy = Buy.objects.get(order=order)  # Assuming Buy model has a foreign key to Order
    except Buy.DoesNotExist:
        buy = None  # If there's no associated Buy object, set it to None

    # Debugging information to check if 'buy' and related data are present
    print("Buy object:", buy)
    if buy:
        print("Product details:", buy.product)
        print("Quantity:", buy.quantity)
        print("Total amount:", buy.total_amount)

    # Razorpay configuration
    razorpay_key_id = "your_razorpay_key_id"
    razorpay_amount = order.total_amount * 100  # Convert to paise (1 INR = 100 paise)
    razorpay_currency = "INR"
    
    # Create Razorpay order
    razorpay_client = razorpay.Client(auth=("rzp_test_fGXBbOpWsXJ5K7", "8r97uL39w4etyjunuKYO4tpE"))
    razorpay_order = razorpay_client.order.create(dict(
        amount=razorpay_amount,
        currency=razorpay_currency,
        payment_capture='1'
    ))

    context = {
        'buy': buy,  # Passing the buy object (which should include the product details)
        'razorpay_key_id': razorpay_key_id,
        'razorpay_amount': razorpay_amount,
        'razorpay_currency': razorpay_currency,
        'razorpay_order_id': razorpay_order['id'],
        'user': request.user
    }

    return render(request, 'user/payment.html', context)

















import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Razorpay client setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        try:
            # Extract the payment details sent by Razorpay
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            
            # Create a dictionary of payment verification details
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature
            try:
                razorpay_client.utility.verify_payment_signature(params_dict)
                
                # Handle success: Mark the order as paid in the database
                order = Order.objects.get(razorpay_order_id=order_id)
                order.payment_status = 'Paid'
                order.payment_id = payment_id
                order.save()

                # Redirect or render the success page
                return render(request, 'user/order.html', {'order': order})
            
            except razorpay.errors.SignatureVerificationError:
                return render(request, 'user/order.html')
        except Exception as e:
            return render(request, 'user/order.html')
