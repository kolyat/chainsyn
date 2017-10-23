from django.conf.urls import url, include


urlpatterns = [
    url(r'^main/', include('main.urls')),
]
