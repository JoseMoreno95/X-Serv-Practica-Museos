from django.conf.urls import include, url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.mainPage),
    url(r'^updatedb/$', views.updateDB),
    url(r'^museos/$', views.museumsPage),
    url(r'^museos/(\d+)/$', views.museumPage),
    url(r'^about/$', views.aboutPage),
    url(r'^login/$', views.loginPage),
    url(r'^logout/$', views.logoutPage),
    url(r'^(\w+)/(\d+)?$', views.userPage),
    url(r'^(\w+)/preferencias/$', views.preferencesPage),
    url(r'^(\w+)/xml/$', views.userXMLPage),
]
