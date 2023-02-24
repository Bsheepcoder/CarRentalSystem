"""DB_Project01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from app01 import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 首页
    path('', views.index),
    # 客户信息
    path('client/list/', views.client_list),
    path('client/add/', views.client_add),
    path('client/<str:no>/edit/', views.client_edit),
    path('client/delete/', views.client_delete),
    # 雇员信息
    path('employee/list/', views.employee_list),
    path('employee/add/', views.employee_add),
    path('employee/<str:no>/edit/', views.employee_edit),
    path('employee/delete/', views.employee_delete),
    # 部门信息
    path('outlet/list/', views.outlet_list),
    path('outlet/add/', views.outlet_add),
    path('outlet/<str:no>/edit/', views.outlet_edit),
    path('outlet/delete/', views.outlet_delete),
    path('outlet/<str:no>/manager/', views.outlet_manager),
    # 租凭信息
    path('rental/list/', views.rental_list),
    path('rental/add/', views.rental_add),
    path('rental/<str:no>/edit/', views.rental_edit),
    path('rental/delete/', views.rental_delete),
    # 故障报告信息
    path('fault/list/', views.fault_list),
    path('fault/add/', views.fault_add),
    path('fault/<str:no>/edit/', views.fault_edit),
    path('fault/delete/', views.fault_delete),
    # 车辆信息
    path('vehicle/list/', views.vehicle_list),
    path('vehicle/add/', views.vehicle_add),
    path('vehicle/<str:no>/edit/', views.vehicle_edit),
    path('vehicle/delete/', views.vehicle_delete),
    # 图表
    path('chart/bar/', views.chart_bar),
    path('chart/pie/', views.chart_pie),
    path('chart/map/', views.chart_map),
]

