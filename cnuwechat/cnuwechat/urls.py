from django.conf.urls import patterns, include, url
from django.contrib import admin
from chatplatform import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cnuwechat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.main,name='test'),
    url(r'^login/',views.login,name='login'),
    url(r'^index/',views.index,name='index'),
    url(r'^balance/',views.search_balance,name='balance'),
    url(r'^logout/',views.logout,name='logout'),
)

