from django.db import models
from DjangoUeditor.models import UEditorField

from datetime import datetime
from organization.models import CourseOrg, Teacher



class Course(models.Model):
    choices = (
        ("cj", "初级"),
        ("zj", "中级"),
        ("gj", "高级"),
    )
    choicess = (
        ("qdkf", "前端开发"),
        ("hdkf", "后端开发"),
        ("qz", "全栈开发"),
    )
    name = models.CharField(max_length=50, verbose_name="课程名")
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True)
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default="")
    degree = models.CharField(choices=choices, max_length=5, verbose_name="课程难度")
    tag = models.CharField(default="", max_length=20, verbose_name="课程标签")
    category = models.CharField(choices=choicess, max_length=10, default="hdkf", verbose_name="课程类别")
    learn_times = models.IntegerField(default=0, verbose_name="学习时间（分钟）")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    teacher = models.ForeignKey(Teacher, null=Teacher, blank=Teacher, verbose_name="讲师")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    you_need_know = models.CharField(max_length=300, default="", verbose_name="课程须知")
    teacher_tell = models.CharField(max_length=300, default="", verbose_name="老师告诉你什么")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()
    get_zj_nums.short_description = "章节数"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</>")
    go_to.short_description = "跳转"

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_lesson_video(self):
        # 获取章节所有视频
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时间（分钟）")
    url = models.CharField(max_length=200, default="", verbose_name="访问地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):

    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="名称")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name="资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

