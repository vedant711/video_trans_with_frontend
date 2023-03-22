from django.urls import path

from . import views

urlpatterns =[
    path('',views.index,name='index'),
    path('api',views.api),
    path('create',views.signup1),
    path('upload',views.upload),
    path('auth_token',views.user_token_view),
    path('check',views.check),
    path('track/<queueId>',views.track),
    path('logout',views.logout_view),
    path('view/<user>',views.indi_page),

]

handler404 = 'views.error404'
handler500 = 'views.error500'