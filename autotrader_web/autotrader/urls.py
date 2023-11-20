"""autotrader URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from search.views import *
from myroot.views import *
from car_details.views import *
from myroot.admin import *
from home.views import *
from django.urls import re_path


admin.site.__class__ = MyrootAdminSite

urlpatterns = [
    path("admin/", admin.site.urls),
    path("search", SearchView.as_view()),
    path("lots/<int:id>", CarDetailsView.as_view()),
    path("calculator", Calculator.as_view()),
    path("get_city", GetCity.as_view()),
    path("order_now", OrderNow.as_view()),
    path("", HomeView.as_view()),
    path("calc-page", CalculatorView.as_view()),
    path("about/gallery", GalleryView.as_view()),
    path("about", AboutView.as_view()),
    path("contact", ContactView.as_view()),
    path("about/services", AboutServicesView.as_view()),
    path("team", TeamView.as_view()),
    path("blog", BlogView.as_view()),
    path("blog/details/<int:postid>", BlogDetailsView.as_view()),
    path("team/details/<int:member_id>", TeamDetailsView.as_view()),
    path("cars", CarsView.as_view()),
    path("cars/details/<int:lotid>", CarsDetailsView.as_view()),
    path("home", HomePageView.as_view()),
    path("shop", ShopPageView.as_view()),
    path("post-message", PostMessage.as_view()),
    path("home-calculator", HomeCalculator.as_view()),
    # path("__debug__/", include("debug_toolbar.urls")),

]
