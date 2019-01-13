from django.urls import path

from admin_app import views

urlpatterns=[
    path("getcaptcha/",views.getcaptcha,name="getcaptcha"),
    path("login_page/",views.login_page,name="login_page"),
    path("login_logic/", views.login_logic, name="login_logic"),
    path("regist_page/", views.regist_page, name="regist_page"),
    path("regist_logic/", views.regist_logic, name="regist_logic"),
    # path("check_captcha/",views.check_captcha,name="check_captcha"),
    # path("check_pwd/", views.check_pwd, name="check_pwd"),
    # path("check_repwd/", views.check_repwd, name="check_repwd"),
    # path("check_nike/", views.check_nike, name="check_nike"),
    # path("del_session/", views.del_session, name="del_session")
]