"""
URL configuration for pharmacy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.registration,name="registration"),
    path('regform', views.regform, name="regform"),
    path('home',views.home,name="home"),
    path('store',views.store, name="store"),
    path('userpage',views.userpage, name="userpage"),
    path('pharpage',views.pharpage, name="pharpage"),
    path('login',views.log, name="login"),
    path('logout',views.logout, name="logout"),
    path('changepsw',views.changepsw, name="changepsw"),
    path('changepassword',views.changepassword, name="changepassword"),
    path('editprofile',views.editprofile, name="editprofile"),
    path('addproduct',views.addproduct, name="addproduct"),
    path('viewproduct',views.viewproduct,name='viewproduct'),
    # path('editproduct/<int:id>',views.editproduct, name='editproduct'),
    path('editproductt/<int:id>',views.editproductt,name='editproductt'),
    path('deleteproduct/<int:id>', views.deleteproduct, name='deleteproduct'),
    path('editpharmacyprofile',views.editpharmacyprofile, name='editpharmacyprofile'),
    path('book/<int:id>',views.book,name='book'),
    path('succsess',views.succsess,name='succsess'),
    path('already',views.already),
    path('buymedicine',views.buymedicine,name='buymedicine'),
    path('cart/<int:id>',views.Add_cart,name='cart'),
    path('cartdelete/<int:id>',views.cartdelete,name='cartdelete'),
    path('alreadycart',views.alreadycart),
    path('history',views.history,name="history"),
    path('phar_history', views.phar_history, name="phar_history"),
    path('view_cart',views.view_cart,name="view_cart"),
    path('payment/<int:id>',views.paymentt, name="payment"),
    path('searchbar',views.searchbar,name="searchbar"),
    path('pharmacyregform',views.pharmacyregform,name="pharmacyregform"),
    path('pharmacyreg',views.pharmacyreg,name="pharmacyreg")








]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

