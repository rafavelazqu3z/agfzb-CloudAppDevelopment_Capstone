from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path('my-url/', views.my_view, name="static_page"),
    # path for about view
    path('about-us/', views.about, name='about-us'),
    # path for contact us view
    path('contact/', views.contact, name="contact"),
    # path for registration
    path('signup/', view=views.signup_request, name='signup'),
    # path for login
    path('login/', view=views.login_request, name='login'),
    # path for logout
    path('logout/', view=views.logout_request, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)