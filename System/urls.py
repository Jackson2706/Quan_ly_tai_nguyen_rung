"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from App import HodViews, StaffViews, views
from System import settings

urlpatterns = (
    [
        path("demo", views.showDemoPage),
        #     path("signup_admin", views.signup_admin, name="signup_admin"),
        #     path("signup_student", views.signup_student, name="signup_student"),
        #     path("signup_staff", views.signup_staff, name="signup_staff"),
        #     path("do_admin_signup", views.do_admin_signup, name="do_admin_signup"),
        #     path("do_staff_signup", views.do_staff_signup, name="do_staff_signup"),
        #     path(
        #         "do_signup_student",
        #         views.do_signup_student,
        #         name="do_signup_student",
        #     ),
        #     path("admin/", admin.site.urls),
        #     path("accounts/", include("django.contrib.auth.urls")),
        path("", views.ShowLoginPage, name="show_login"),
        #     path("get_user_details", views.GetUserDetails),
        path("logout_user", views.logout_user, name="logout"),
        path(
            "check_email_exist",
            HodViews.check_email_exist,
            name="check_email_exist",
        ),
        path(
            "check_username_exist",
            HodViews.check_username_exist,
            name="check_username_exist",
        ),
        path("doLogin", views.doLogin, name="do_login"),
        path("admin_home", HodViews.admin_home, name="admin_home"),
        path("them_don_vi", HodViews.Them_donvi, name="them_don_vi"),
        path(
            "them_don_vi_save",
            HodViews.Them_donvi_save,
            name="them_don_vi_save",
        ),
        path("manage_don_vi", HodViews.manage_don_vi, name="manage_donvi"),
        path(
            "edit_don_vi/<str:donvi_id>",
            HodViews.edit_don_vi,
            name="edit_don_vi",
        ),
        path(
            "edit_donvi_save", HodViews.edit_don_vi_save, name="edit_donvi_save"
        ),
        path("add_staff", HodViews.add_staff, name="add_staff"),
        path("add_staff_save", HodViews.add_staff_save, name="add_staff_save"),
        path("manage_staff", HodViews.manage_staff, name="manage_staff"),
        path(
            "edit_staff/<str:staff_id>", HodViews.edit_staff, name="edit_staff"
        ),
        path(
            "edit_staff_save", HodViews.edit_staff_save, name="edit_staff_save"
        ),
        path(
            "add_loai_cay_giong",
            HodViews.add_loai_cay_giong,
            name="add_loai_cay_giong",
        ),
        path(
            "add_loai_cay_giong_save",
            HodViews.add_loai_cay_giong_save,
            name="add_loai_cay_giong_save",
        ),
        path(
            "manage_loai_cay_giong",
            HodViews.manage_loai_cay_giong,
            name="manage_loai_cay_giong",
        ),
        path(
            "edit_loai_cay_giong/<str:id_giong_cay>",
            HodViews.edit_loai_cay_giong,
            name="edit_loai_cay_giong",
        ),
        path(
            "edit_loai_cay_giong_save",
            HodViews.edit_loai_cay_giong_save,
            name="edit_loai_cay_giong_save",
        ),
        path(
            "add_co_so_san_xuat_cay_giong",
            HodViews.add_co_so_san_xuat_cay_giong,
            name="add_co_so_san_xuat_cay_giong",
        ),
        path(
            "add_co_so_san_xuat_cay_giong_save",
            HodViews.add_co_so_san_xuat_cay_giong_save,
            name="add_co_so_san_xuat_cay_giong_save",
        ),
        path(
            "manage_co_so_san_xuat_cay_giong",
            HodViews.manage_co_so_san_xuat_cay_giong,
            name="manage_co_so_san_xuat_cay_giong",
        ),
        path(
            "edit_co_so_san_xuat_cay_gong/<str:co_so_sx_cay_giong_id>",
            HodViews.edit_co_so_san_xuat_cay_gong,
            name="edit_co_so_san_xuat_cay_gong",
        ),
        path(
            "edit_co_so_san_xuat_cay_gong_save",
            HodViews.edit_co_so_san_xuat_cay_gong_save,
            name="edit_co_so_san_xuat_cay_gong_save",
        ),
        path("admin_profile", HodViews.admin_profile, name="admin_profile"),
        # Staff
        path("staff_home", StaffViews.staff_home, name="staff_home"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
