from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cambio.views import RateViewSet  # <-- novo
from cambio import views_html

router = DefaultRouter()
router.register(r'rates', RateViewSet, basename='rate')  # <-- novo

#router.register(r'tarefas', TarefaViewSet, basename='tarefa')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("", views_html.home, name="home"),
    path("rates/", views_html.rate_list, name="rate_list"),
    path("rates/new/", views_html.rate_create, name="rate_create"),
    path("rates/<int:pk>/edit/", views_html.rate_edit, name="rate_edit"), 
    path("rates/<int:pk>/delete/", views_html.rate_delete, name="rate_delete"),
    path("rates/<int:pk>/history/", views_html.rate_history, name="rate_history"),
    path("rates/batch/", views_html.rate_batch, name="rate_batch"),
    path("convert/", views_html.convert_view, name="convert_view"),
]