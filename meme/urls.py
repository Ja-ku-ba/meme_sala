from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
         
    path('zarejestruj', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('wyloguj', views.logout_user, name='logout'),
         
    path('dodaj_post', views.post_add, name='post_add'),
    path('post/<str:pk>', views.post, name='post'),
    path('usun_post/<str:pk>', views.post_delete, name='post_delete'),
    path('polub/<str:pk>', views.like, name='like'),
    path('znielub/<str:pk>', views.dislike, name='dislike'),
    path('usun_komentarz/<str:pk>', views.coment_delete, name='coment_delete'),
         
    
    path('profil/<str:pk>', views.user_page, name='user_page'),
    path('interakcje', views.user_interactions, name='user_interactions'),
    path('powiadomienia', views.user_notifications, name='user_notifications'),
    path('ustawienia', views.user_settings_page, name='user_settings_page'),
]