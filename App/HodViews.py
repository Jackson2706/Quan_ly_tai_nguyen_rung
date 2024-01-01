import json

import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from App.models import (
    CanBoNghiepVu,
    CoSoSanXuatCayGiong,
    CustomUser,
    Donvi,
    LoaiCayGiong,
    LoaiDongVatQuy,
)


def admin_home(request):
    CanBoNghiepVu_count = CanBoNghiepVu.objects.all().count()
    LoaiCayGiong_count = LoaiCayGiong.objects.all().count()
    LoaiDongVatQuyHiem_count = LoaiDongVatQuy.objects.all().count()
    CoSoSanXuatCayGiong_count = CoSoSanXuatCayGiong.objects.all().count()

    return render(
        request,
        "hod_template/home_content.html",
        {
            "CanBoNghiepVu_count": CanBoNghiepVu_count,
            "LoaiCayGiong_count": LoaiCayGiong_count,
            "LoaiDongVatQuyHiem_count": LoaiDongVatQuyHiem_count,
            "CoSoSanXuatCayGiong_count": CoSoSanXuatCayGiong_count,
        },
    )


def add_staff(request):
    don_vi_all = Donvi.objects.all()
    return render(
        request,
        "hod_template/add_staff_template.html",
        {"don_vi_all": don_vi_all},
    )


def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        chuc_vu = request.POST.get("chuc_vu")
        don_vi_id = request.POST.get("don_vi")
        don_vi_ = Donvi.objects.get(id=don_vi_id)
        try:
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                last_name=last_name,
                first_name=first_name,
                user_type=2,
            )
            user.canbonghiepvu.don_vi = don_vi_
            user.canbonghiepvu.chuc_vu = chuc_vu
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def manage_staff(request):
    staffs = CanBoNghiepVu.objects.all()
    return render(
        request, "hod_template/manage_staff_template.html", {"staffs": staffs}
    )


def edit_staff(request, staff_id):
    staff = CanBoNghiepVu.objects.get(admin=staff_id)
    don_vi_all = Donvi.objects.all()
    return render(
        request,
        "hod_template/edit_staff_template.html",
        {"staff": staff, "don_vi_all": don_vi_all},
    )


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        chuc_vu = request.POST.get("chuc_vu")
        don_vi_id = request.POST.get("don_vi")
        don_vi_ = Donvi.objects.get(id=don_vi_id)
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.password = password
            user.save()

            staff_model = CanBoNghiepVu.objects.get(admin=staff_id)
            staff_model.don_vi = don_vi_
            staff_model.chuc_vu = chuc_vu
            staff_model.save()

            messages.success(request, "Successfully update Staff")
            return HttpResponseRedirect(
                reverse("edit_staff", kwargs={"staff_id": staff_id})
            )
        except:
            messages.error(request, "Failed to update Staff")
            return HttpResponseRedirect(
                reverse("edit_staff", kwargs={"staff_id": staff_id})
            )


def Them_donvi(request):
    return render(request, "hod_template/add_donvi.html")


def Them_donvi_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        ten_don_vi = request.POST.get("don_vi")
        dia_chi = request.POST.get("dia_chi")
        try:
            donvi = Donvi(ten_don_vi=ten_don_vi, vi_tri=dia_chi)
            donvi.save()
            messages.success(request, "Successfully Added don vi")
            return HttpResponseRedirect(reverse("them_don_vi"))
        except:
            messages.error(request, "Failed to Add don vi")
            return HttpResponseRedirect(reverse("them_don_vi"))


def manage_don_vi(request):
    donvi_all = Donvi.objects.all()
    return render(
        request, "hod_template/manage_don_vi.html", {"donvi_all": donvi_all}
    )


def edit_don_vi(request, donvi_id):
    don_vi = Donvi.objects.get(id=donvi_id)
    return render(request, "hod_template/edit_donvi.html", {"don_vi": don_vi})


def edit_don_vi_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        don_vi_id = request.POST.get("donvi_id")
        ten_don_vi = request.POST.get("don_vi")
        dia_chi = request.POST.get("dia_chi")
        try:
            donvi = Donvi.objects.get(id=don_vi_id)
            donvi.ten_don_vi = ten_don_vi
            donvi.vi_tri = dia_chi
            donvi.save()
            messages.success(request, "Successfully Updated don vi")
            return HttpResponseRedirect(
                reverse("edit_don_vi", kwargs={"donvi_id": don_vi_id})
            )
        except:
            messages.error(request, "Failed to update don vi")
            return HttpResponseRedirect(
                reverse("manage_donvi", kwargs={"donvi_id": don_vi_id})
            )


def add_loai_cay_giong(request):
    return render(request, "hod_template/add_loai_cay_giong.html")


def add_loai_cay_giong_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        ten_loai_cay_giong = request.POST.get("loai_cay_giong")
        ngay_cap_phep = request.POST.get("ngay_cap_phep")
        try:
            loai_cay_giong = LoaiCayGiong(
                ten_giong=ten_loai_cay_giong, Ngay_cap_phep=ngay_cap_phep
            )
            loai_cay_giong.save()
            messages.success(request, "Successfully Create loai giong cay moi")
            return HttpResponseRedirect(reverse("add_loai_cay_giong"))
        except:
            messages.error(request, "Failed Create loai giong cay moi")
            return HttpResponseRedirect(reverse("add_loai_cay_giong"))


def manage_loai_cay_giong(request):
    loai_cay_giong_all = LoaiCayGiong.objects.all()
    return render(
        request,
        "hod_template/manage_loai_cay_giong.html",
        {"loai_cay_giong_all": loai_cay_giong_all},
    )


def edit_loai_cay_giong(request, id_giong_cay):
    giong_cay = LoaiCayGiong.objects.get(id=id_giong_cay)
    return render(
        request,
        "hod_template/edit_loai_cay_giong.html",
        {"giong_cay": giong_cay},
    )


def edit_loai_cay_giong_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        cay_giong_id = request.POST.get("giong_cay_id")
        ten_loai_cay_giong = request.POST.get("loai_cay_giong")
        ngay_cap_phep = request.POST.get("ngay_cap_phep")
        try:
            loai_cay_giong = LoaiCayGiong.objects.get(id=cay_giong_id)
            loai_cay_giong.ten_giong = ten_loai_cay_giong
            loai_cay_giong.Ngay_cap_phep = ngay_cap_phep
            loai_cay_giong.save()
            messages.success(request, "Successfully update loai giong cay moi")
            return HttpResponseRedirect(
                reverse(
                    "edit_loai_cay_giong", kwargs={"id_giong_cay": cay_giong_id}
                )
            )
        except:
            messages.error(request, "Failed Update loai giong cay moi")
            return HttpResponseRedirect(
                reverse(
                    "edit_loai_cay_giong", kwargs={"id_giong_cay": cay_giong_id}
                )
            )


def add_co_so_san_xuat_cay_giong(request):
    return render(request, "hod_template/add_co_so_san_xuat_cay_giong.html")


def add_co_so_san_xuat_cay_giong_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        ten_co_so = request.POST.get("ten_co_so")
        dia_chi = request.POST.get("dia_chi")
        ngay_cap_phep = request.POST.get("ngay_cap_phep")
        try:
            co_so_sx_cay_giong = CoSoSanXuatCayGiong(
                ten_co_so=ten_co_so,
                dia_diem=dia_chi,
                ngay_cap_phep=ngay_cap_phep,
            )
            co_so_sx_cay_giong.save()
            messages.success(
                request, "Successfully create co so san xuat giong cay moi"
            )
            return HttpResponseRedirect(reverse("add_co_so_san_xuat_cay_giong"))
        except:
            messages.error(
                request, "Failed create co so san xuat giong cay moi"
            )
            return HttpResponseRedirect(reverse("add_co_so_san_xuat_cay_giong"))


def manage_co_so_san_xuat_cay_giong(request):
    co_so_san_xuat_cay_giong_all = CoSoSanXuatCayGiong.objects.all()
    return render(
        request,
        "hod_template/manage_cs_sx_cay_giong.html",
        {"co_so_san_xuat_cay_giong_all": co_so_san_xuat_cay_giong_all},
    )


def edit_co_so_san_xuat_cay_gong(request, co_so_sx_cay_giong_id):
    co_so_sx_cay_giong = CoSoSanXuatCayGiong.objects.get(
        id=co_so_sx_cay_giong_id
    )
    return render(request, "hod_template/edit_cs_sx_cay_giong.html", {"co_so_sx_cay_giong": co_so_sx_cay_giong})

def edit_co_so_san_xuat_cay_gong_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        co_so_id = request.POST.get("co_so_id")
        ten_co_so = request.POST.get("ten_co_so")
        dia_chi = request.POST.get("dia_chi")
        ngay_cap_phep = request.POST.get("ngay_cap_phep")
        try:
            co_so_sx_cay_giong = CoSoSanXuatCayGiong.objects.get(id=co_so_id)
            co_so_sx_cay_giong.ten_co_so = ten_co_so
            co_so_sx_cay_giong.dia_diem = dia_chi
            co_so_sx_cay_giong.ngay_cap_phep = ngay_cap_phep
            co_so_sx_cay_giong.save()
            messages.success(request, "Successfully update co so sx cay giong")
            return HttpResponseRedirect(
                reverse(
                    "edit_co_so_san_xuat_cay_gong", kwargs={"co_so_sx_cay_giong_id": co_so_id}
                )
            )
        except:
            messages.error(request, "Failed Update loai giong cay moi")
            return HttpResponseRedirect(
                reverse(
                    "edit_co_so_san_xuat_cay_gong", kwargs={"co_so_sx_cay_giong_id": co_so_id}
                )
            )
        
@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


# def staff_feedback_message(request):
#     feedbacks=FeedBackStaffs.objects.all()
#     return render(request,"hod_template/staff_feedback_template.html",{"feedbacks":feedbacks})

# def student_feedback_message(request):
#     feedbacks=FeedBackStudent.objects.all()
#     return render(request,"hod_template/student_feedback_template.html",{"feedbacks":feedbacks})

# @csrf_exempt
# def student_feedback_message_replied(request):
#     feedback_id=request.POST.get("id")
#     feedback_message=request.POST.get("message")

#     try:
#         feedback=FeedBackStudent.objects.get(id=feedback_id)
#         feedback.feedback_reply=feedback_message
#         feedback.save()
#         return HttpResponse("True")
#     except:
#         return HttpResponse("False")

# @csrf_exempt
# def staff_feedback_message_replied(request):
#     feedback_id=request.POST.get("id")
#     feedback_message=request.POST.get("message")

#     try:
#         feedback=FeedBackStaffs.objects.get(id=feedback_id)
#         feedback.feedback_reply=feedback_message
#         feedback.save()
#         return HttpResponse("True")
#     except:
#         return HttpResponse("False")

# def staff_leave_view(request):
#     leaves=LeaveReportStaff.objects.all()
#     return render(request,"hod_template/staff_leave_view.html",{"leaves":leaves})

# def student_leave_view(request):
#     leaves=LeaveReportStudent.objects.all()
#     return render(request,"hod_template/student_leave_view.html",{"leaves":leaves})

# def student_approve_leave(request,leave_id):
#     leave=LeaveReportStudent.objects.get(id=leave_id)
#     leave.leave_status=1
#     leave.save()
#     return HttpResponseRedirect(reverse("student_leave_view"))

# def student_disapprove_leave(request,leave_id):
#     leave=LeaveReportStudent.objects.get(id=leave_id)
#     leave.leave_status=2
#     leave.save()
#     return HttpResponseRedirect(reverse("student_leave_view"))


# def staff_approve_leave(request,leave_id):
#     leave=LeaveReportStaff.objects.get(id=leave_id)
#     leave.leave_status=1
#     leave.save()
#     return HttpResponseRedirect(reverse("staff_leave_view"))

# def staff_disapprove_leave(request,leave_id):
#     leave=LeaveReportStaff.objects.get(id=leave_id)
#     leave.leave_status=2
#     leave.save()
#     return HttpResponseRedirect(reverse("staff_leave_view"))

# def admin_view_attendance(request):
#     subjects=Subjects.objects.all()
#     session_year_id=SessionYearModel.object.all()
#     return render(request,"hod_template/admin_view_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

# @csrf_exempt
# def admin_get_attendance_dates(request):
#     subject=request.POST.get("subject")
#     session_year_id=request.POST.get("session_year_id")
#     subject_obj=Subjects.objects.get(id=subject)
#     session_year_obj=SessionYearModel.object.get(id=session_year_id)
#     attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
#     attendance_obj=[]
#     for attendance_single in attendance:
#         data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
#         attendance_obj.append(data)

#     return JsonResponse(json.dumps(attendance_obj),safe=False)


# @csrf_exempt
# def admin_get_attendance_student(request):
#     attendance_date=request.POST.get("attendance_date")
#     attendance=Attendance.objects.get(id=attendance_date)

#     attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
#     list_data=[]

#     for student in attendance_data:
#         data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
#         list_data.append(data_small)
#     return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "hod_template/admin_profile.html", {"user": user})


# def admin_profile_save(request):
#     if request.method!="POST":
#         return HttpResponseRedirect(reverse("admin_profile"))
#     else:
#         first_name=request.POST.get("first_name")
#         last_name=request.POST.get("last_name")
#         password=request.POST.get("password")
#         try:
#             customuser=CustomUser.objects.get(id=request.user.id)
#             customuser.first_name=first_name
#             customuser.last_name=last_name
#             # if password!=None and password!="":
#             #     customuser.set_password(password)
#             customuser.save()
#             messages.success(request, "Successfully Updated Profile")
#             return HttpResponseRedirect(reverse("admin_profile"))
#         except:
#             messages.error(request, "Failed to Update Profile")
#             return HttpResponseRedirect(reverse("admin_profile"))

# def admin_send_notification_student(request):
#     students=Students.objects.all()
#     return render(request,"hod_template/student_notification.html",{"students":students})

# def admin_send_notification_staff(request):
#     staffs=Staffs.objects.all()
#     return render(request,"hod_template/staff_notification.html",{"staffs":staffs})

# @csrf_exempt
# def send_student_notification(request):
#     id=request.POST.get("id")
#     message=request.POST.get("message")
#     student=Students.objects.get(admin=id)
#     token=student.fcm_token
#     url="https://fcm.googleapis.com/fcm/send"
#     body={
#         "notification":{
#             "title":"Student Management System",
#             "body":message,
#             "click_action": "https://studentmanagementsystem22.herokuapp.com/student_all_notification",
#             "icon": "http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
#         },
#         "to":token
#     }
#     headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
#     data=requests.post(url,data=json.dumps(body),headers=headers)
#     notification=NotificationStudent(student_id=student,message=message)
#     notification.save()
#     print(data.text)
#     return HttpResponse("True")

# @csrf_exempt
# def send_staff_notification(request):
#     id=request.POST.get("id")
#     message=request.POST.get("message")
#     staff=Staffs.objects.get(admin=id)
#     token=staff.fcm_token
#     url="https://fcm.googleapis.com/fcm/send"
#     body={
#         "notification":{
#             "title":"Student Management System",
#             "body":message,
#             "click_action":"https://studentmanagementsystem22.herokuapp.com/staff_all_notification",
#             "icon":"http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
#         },
#         "to":token
#     }
#     headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
#     data=requests.post(url,data=json.dumps(body),headers=headers)
#     notification=NotificationStaffs(staff_id=staff,message=message)
#     notification.save()
#     print(data.text)
#     return HttpResponse("True")
