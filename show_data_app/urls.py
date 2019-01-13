from django.urls import include, path

from show_data_app import views

app_name = 'show_data_app'
urlpatterns = [
    path("show_data/", include([
        path('show_index/', views.show_index, name='show_index'),
        path('show_introduce/', views.show_introduce, name='show_introduce'),
        path('show_menu/', views.show_menu, name='show_menu'),
        path('ajax_show_menu/', views.ajax_show_menu, name='ajax_show_menu'),
    ])),
    path("prohibit_crawl/", include([
        path('show_pro_page/', views.show_prohibit_page, name='show_pro_page'),
        path('get_pro_code/', views.pro_crawl_captcha, name='get_pro_code'),
        path('validate_pro_code/', views.validate_pro_crawl_captcha, name='validate_pro_code')
    ])),
]