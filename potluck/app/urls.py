from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'potluck'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('create', views.create_event, name='create'),
    path('event/<int:event_id>', views.detail, name='detail'),
    path('event/<int:event_id>/update', views.update, name='update'),
    path('event/<int:event_id>/attend', views.attend, name='attend'),
    path('friends', views.friends, name='friends'),
    path('add_friend', views.add_friend, name='add_friend'),
    path('add_item/<int:event_id>', views.addItem, name='addItem'),
    path('finish/<int:event_id>', views.finish, name='finish'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
