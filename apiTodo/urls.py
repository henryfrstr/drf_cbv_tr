from django.urls import path
from .views import home, todoList, todoListCreate, toDo_list, todoListUpdate, todoListDelete, toDo_detail, TodoList, TodoDetail


urlpatterns = [
    path('', home),
    # path('todoList/', todoList),
    # path('todoListCreate/', todoListCreate),
    # path('toDo_list/', toDo_list),
    # path('todoListUpdate/<int:pk>/', todoListUpdate),
    # path('todoListDelete/<int:pk>/', todoListDelete),
    # path('toDo_detail/<int:pk>/', toDo_detail),
    path('todo-list/', TodoList.as_view()),
    path('todo-detail/<int:pk>', TodoDetail.as_view()),

]
