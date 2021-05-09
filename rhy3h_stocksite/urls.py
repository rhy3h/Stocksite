"""rhy3h_stocksite URL Configuration

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
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from . import views, dashboard, apis
from . import settings

handler404 = views.page_not_found
handler500 = views.internal_server_error

urlpatterns = [
    path('admin/', admin.site.urls),

    url('^HelloWorld/$', views.HelloWorld),

    url('index/', dashboard.index),
    url('^$', dashboard.index),

    url('^apis/fubon/query', apis.fubon),
    url('^apis/wantgoo/query', apis.wantgoo),
    
    url('^dashboard/$', dashboard.index),
    url('^dashboard/query', dashboard.index),
    url('^dashboard/update', dashboard.update),
    url('^dashboard/export/query', dashboard.export_list),
    url('^dashboard/import/query', dashboard.import_list),
    url('^create_group/$', dashboard.create_group),
    url('^del_group/query', dashboard.del_group),
    url('^add_broker/query', dashboard.add_broker),
    url('^del_broker/query', dashboard.del_broker),
    
    path('accounts/register/', views.register, name='register'),
    url('^accounts/login', LoginView.as_view()),
    url('^accounts/logout', views.logout),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)