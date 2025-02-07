from django.urls import path
from . import views
urlpatterns=[
    path('',views.shp_login),
    path('shp_login1/', views.shp_login1, name='shp_login1'),
    path('shp_logout',views.shp_logout),


    # ---------------shop--------------------


    path('shp_home',views.shp_home),
    path('add_prod/',views.add_prod),
    path('products/',views.products),
    path('products/edit_prod/<int:pid>/', views.edit_prod, name='edit_prod'),
    path('delete_prod/<pid>',views.delete_prod),
    path('bookings',views.bookings),


    # --------------user---------------------


   
    path('register/', views.register, name='register'),
    path('user_home',views.user_home ,name='user_home'),
    path('view_pro/<pid>/',views.view_pro),
    path('user_products',views.user_products),
    path('add_to_cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path("update_cart/", views.update_cart, name="update_cart"),
    path('delete_cart/<int:id>/', views.delete_cart, name='delete_cart'),
    path('user_buy/<int:cid>/', views.user_buy, name='user_buy'),
    path('user_buy1/<pid>',views.user_buy1),
    path('user_bookings',views.user_bookings),
    path('order/', views.order, name='order'),
    path('order/success/', views.order_success, name='order_success'),
    
    

]