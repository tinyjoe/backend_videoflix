from django.urls import path
from .views import RegistrationView, LoginView, LogoutTokenDeleteView, CookieTokenRefreshView

urlpatterns=[
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutTokenDeleteView.as_view(), name='logout'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
]