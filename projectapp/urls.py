from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    path('logout/', logoutUser, name='logoutpage'),
    path('login/', loginUser, name='loginpage'),
    path('signup/', signupUser, name='signuppage'),
    path('sendmail/', sendmailUser, name='sendmailpage'),
    path('verify/<auth_token>', verify, name='verify'),
    path('', home, name='homepage'),
    path('form/', form, name='formpage'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)