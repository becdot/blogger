from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('blog.views',
    # Examples:
    # url(r'^$', 'blogger.views.home', name='home'),
    # url(r'^blogger/', include('blogger.foo.urls')),

    # signup
    url(r'^signup$', 'signup'),
    # login
    url(r'^$', 'login_user'),
    # logout
    url(r'^logout$', 'logout_user'),
    # welcome form (on login)
    url(r'^welcome$', 'welcome'),
    # add new post
    url(r'^new$', 'new_post'),
    # view most recent % posts
    url(r'^view/recent/(\d+)$', 'view_recent'),
    # view specified post
    url(r'^view/(\d+)$', 'view_post'),

    url(r'^admin/', include(admin.site.urls)),
)
