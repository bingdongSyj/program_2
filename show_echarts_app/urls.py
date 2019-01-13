from django.urls import include, path

from show_echarts_app import views

app_name = 'show_echarts_app'
urlpatterns = [
    path("echarts/", include([
        path('show_echarts_table/', views.show_echarts_table, name='show_table'),
        path('get_echarts/', views.get_echarts, name='get_echarts'),
    ])),
]