from django.urls import path

from . import views

app_name = "converter"

urlpatterns = [
    path("convert/", views.convert_view, name="convert"),
    path("history/", views.history_view, name="history"),
    path("history/delete/<int:pk>/", views.delete_history_view, name="delete_history"),
]
