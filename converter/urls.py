from django.urls import path

from . import views

app_name = "converter"

urlpatterns = [
    path("convert/", views.convert_view, name="convert"),
    path("history/", views.history_view, name="history"),
    path("history/delete/<int:pk>/", views.delete_history_view, name="delete_history"),
    path("favorites/", views.favorite_list_view, name="favorites"),
    path("favorites/add/", views.favorite_add_view, name="favorite_add"),
    path(
        "favorites/delete/<int:pk>/",
        views.favorite_delete_view,
        name="favorite_delete",
    ),
]
