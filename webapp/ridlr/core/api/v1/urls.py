from django.conf.urls import url

from .views import QuestionBank

urlpatterns = [
    url(r'^questions/$', QuestionBank.as_view(),
        name="questions"),
]