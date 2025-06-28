from django.urls import path, include   
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.TodosViewsetApiVew)


urlpatterns = [
    path('', views.all_todos),
    path('<int:todo_id>', views.todo_detail_view),
    path('cbv/', views.TodoListApiView.as_view()),
    path('cbv/<int:todo_id>', views.TodoDetailApiView.as_view()),
    path('mixins/', views.TodoListMixinsApiView.as_view()),
    path('mixins/<pk>', views.TodoDetailMixinsApiView.as_view()),
    path('generics/', views.TodoGenericsApiVeiw.as_view()),
    path('generics/<pk>', views.TodoGenericsDetailApiVew.as_view()),
    path('viewsets/', include(router.urls)),
    path('Users/', views.UserGenericsApiVeiw.as_view()),
]