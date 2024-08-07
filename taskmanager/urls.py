from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("board/new-board", views.board_form, name="new-board"),
    path("board/column/<int:current_total_formsets>", views.column_form, name="add-column"),
    path("board/<str:id>" , views.board_detail_view, name="board-detail"),
    path("board/<str:id>/edit-board", views.edit_board, name="edit-board"),
    path("board/<str:id>/delete-board", views.delete_board, name="delete-board")
]