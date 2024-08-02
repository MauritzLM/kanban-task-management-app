from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("board/new-board", views.new_board, name="new-board"),
    path("board/<str:id>" , views.board_detail_view, name="board-detail"),
    path("board/<str:id>/new-column", views.new_column, name="new-column")
    
]