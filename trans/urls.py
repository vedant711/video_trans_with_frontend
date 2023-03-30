from django.urls import path

from . import views
from django.views.generic.base import RedirectView

urlpatterns =[
    path('',views.index,name='index'),
    path('api',views.api),
    path('create',views.signup1),
    path('upload',views.upload),
    path('auth_token',views.user_token_view),
    path('track/<queueId>',views.track),
    path('logout',views.logout_view),
    path('view/<user>',views.indi_page),
    path('adminportal',views.admin_portal),
    path('remove/<user>',views.remove_user),
]

handler404 = 'trans.views.error404'
handler500 = 'trans.views.error500'