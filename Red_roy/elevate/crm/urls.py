from django.urls import path,include
from .import views
from django.contrib.auth import views as auth_views
from django.views.i18n import set_language
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('delete_reservation_client/<int:reservation_id>/', views.delete_reservation_Client, name='delete_reservation_client'),
    path('reset_b/', views.reset_b, name='reset_b'),
    path('delete_reservation/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('', views.home, name='home'),
    path('v8/', views.v8_template, name='v8_template'),
    path('events/', views.events, name='events'),
    path('reservation/', views.reservation, name='reservation'),
    path('posts/', views.posts, name='posts'),
    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('admin-login/', views.login_admin, name='admin-login'),
    path('email/', views.email, name='email'),
    path('success/', views.success, name='success'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('update_event/<int:event_id>/', views.update_event, name='update_event'),
    path('login/', views.user_login, name='login'),  
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/edit/', views.update_post, name='update_post'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)