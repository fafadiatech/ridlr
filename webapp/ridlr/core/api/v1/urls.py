from django.conf.urls import url

from .views import QuestionsAPI

urlpatterns = [
    url(r'^questions/$', QuestionsAPI.as_view(),
        name="questions"),
]