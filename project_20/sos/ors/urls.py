from django.urls import path
from . import views

urlpatterns = [

    path('', views.index),

    path("<str:page>/preload/", views.preload_router),

    # /ORS/auth/Login
    # /ORS/auth/CP  - Change password
    # /ORS/auth/FP  - Forgot Password
    # /ORS/auth/Registration  - Forgot Password
    path('auth/<page>', views.auth_action),

    # /ORS/User/search
    path('<page>/<action>/<int:id>', views.action_id),

    # /ORS/User/search
    path('<page>/<action>/', views.action),

    # /ORS/User/1
    # /ORS/Account/1
    path('<page>/<int:id>', views.actionId),

    # /ORS/Login
    # /ORS/ChangePassword
    path('<page>/', views.actionId),
    path('<page>/', views.actionId),


]
