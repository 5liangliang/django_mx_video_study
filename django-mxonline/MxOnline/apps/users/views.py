import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm
from .forms import UserInfoForm
from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from .models import Banner
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    """登录函数"""
    def get(self, request):
        redirect_url = request.GET.get("next", '')
        return render(request, "login.html", {"redirect_url": redirect_url})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活,请前往邮箱进行激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    """用户登出"""
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class RegisterView(View):

    def get(self, request):
        # 实例化生成验证码，返回一个对用户具有验证功能的页面
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        # 将通过表单的验证的post对象取出进行is_valid验证后，
        # 通过对模型创建一个实例对象将其存入数据库中
        # 尤为注意的是：对用户的密码需要进行make_password加密处理
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 这里注册时，前端的name为email
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form":register_form, "msg":"用户已存在,请更换用户名"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 对密码进行加密
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 当用户注册成功时，显示一则消息给用户
            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册在线学习网"
            user_message.save()

            send_register_email(user_name, "register")
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {"register_form": register_form})


class ActiveUserView(View):
    # 通过url将验证码code进行捕捉
    # 在数据库中对验证码进行查询
    # 如果查询到，将用户的is_active设为True
    # 激活成功，进行保存
    def get(self,request, active_code):
        # 在这里get可能也适用
        # 使用filter的好处是联表查询如果查询不到，会返回None而不会报错
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()

        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        format_form = ForgetForm(request.POST)
        if format_form.is_valid():
            email = request.POST.get("email", "")

            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form":format_form})


class ResetView(View):

    def get(self,request, active_code):
        # 在这里get可能也适用
        # 使用filter的好处是联表查询如果查询不到，会返回None而不会报错
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    """修改用户密码"""
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, "reset_pwd_ok.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    """用户个人信息"""
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        # 因为我们是在原有的实例上进行修改，
        # 所以要在表单中增加instance变量指明所修改的实例
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """用户修改头像"""
    def post(self, request):
        imgae_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if imgae_form.is_valid():
            imgae_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    """修改用户密码"""
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success","msg":"密码修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """发送邮箱验证码"""
    def get(self, request):
        email = request.GET.get("email", "")

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email, "update_email")

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """修改个人邮箱功能实现"""
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type="update_email")

        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"email":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')


class MyCoursesView(LoginRequiredMixin, View):
    """我的课程"""
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """我的课程"""
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """我的课程"""
    def get(self, request):
        teachers_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teachers_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teachers_list": teachers_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """我的课程"""
    def get(self, request):
        courses_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            courses_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            "courses_list": courses_list,
        })


class MyMessagesView(LoginRequiredMixin, View):
    """我的消息"""
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        # 用户进入个人消息后
        # 清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对查询结果进行分页,使用的pure_pagination库
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, per_page=5, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            "messages": messages,
        })


class IndexView(View):
    """首页"""
    def get(self, request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            "all_banners": all_banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })


def page_not_found(request):
    # 全局404处理逻辑
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理逻辑
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
