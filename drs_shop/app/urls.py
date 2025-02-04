from django.urls import path
from . import views
urlpatterns=[
    path('',views.shp_login),
    path('shp_logout',views.shp_logout),


    # ---------------shop--------------------


    path('shp_home',views.shp_home),
    path('add_prod',views.add_prod),
    path('products',views.products),
    path('edit_prod/<pid>',views.edit_prod),
    path('delete_prod/<pid>',views.delete_prod),
    path('bookings',views.bookings),


    # --------------user---------------------


    path('register',views.register),
     path('user_home',views.user_home ,name='user_home'),
    path('view_pro/<pid>',views.view_pro),
    path('user_products',views.user_products),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart/',views.view_cart),
    path('delete_cart/<int:id>/', views.delete_cart, name='delete_cart'),
    path('user_buy/<int:cid>/', views.user_buy, name='user_buy'),
    path('user_buy1/<pid>',views.user_buy1),
    path('user_bookings',views.user_bookings),
    path('order/', views.order, name='order'),
    path('order/success/', views.order_success, name='order_success'),
    
    

]