"""first_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.contrib.staticfiles import *
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from rest_framework_jwt.views import obtain_jwt_token

from . import views
import api


urlpatterns = [
    url(r'^$', RedirectView.as_view(url='main/')),
    url(r'^accounts/', include("accounts.urls", namespace='accounts')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls', namespace='api')),
    url(r'^api/auth/login/$', obtain_jwt_token, name='api-login'),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^contacts/', views.contacts, name='contacts'),
    url(r'^delivery/', views.delivery, name='delivery'),
    url(r'^main/', views.main, name='main'),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^filtered_products/', views.filteredProducts, name='filtered_products'),
    # url(r'^forging_comments/', views.forging_comments, name='forging_comments'),
    # url(r'^comments/', include("comments.urls", namespace='comments')),
]



urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)