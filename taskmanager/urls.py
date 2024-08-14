from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("board/new-board", views.board_form, name="new-board"),
    path("board/column/<int:current_total_formsets>", views.column_form, name="add-column"),
    path("board/subtask/<int:current_total_formsets>", views.subtask_form, name="add-subtask"),
    path("board/<str:id>" , views.board_detail_view, name="board-detail"),
    path("board/<str:id>/edit-board", views.edit_board, name="edit-board"),
    path("board/<str:id>/delete-board", views.delete_board, name="delete-board"),
    path("board/<str:id>/new-task", views.new_task, name="new-task"),
    path("board/<str:t_id>/delete-task", views.delete_task, name="delete-task"),
    path("board/<str:id>/view-task/<str:t_id>", views.task_view, name="view-task"),
    path("board/<str:id>/edit-task/<str:t_id>", views.edit_task, name="edit-task")
]