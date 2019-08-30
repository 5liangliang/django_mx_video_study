__auther__ = "liangliang"
__date__ = "2019/6/23 10:42"

import xadmin

from .models import UserAsk, UserCourse, UserMessage, UserFavorite, CourseComments


class UserAskAdmin(object):
    list_display = ["mobile", "name", "add_time", "course_name"]
    search_fields = ["mobile", "name", "course_name"]
    list_filter = ["mobile", "name", "add_time", "course_name"]


class UserCourseAdmin(object):
    list_display = ["user", "course", "add_time"]
    search_fields = ["user", "course"]
    list_filter = ["user", "course", "add_time"]


class UserMessageAdmin(object):
    list_display = ["user", "message", "add_time", "has_read"]
    search_fields = ["user", "message", "has_read"]
    list_filter = ["user", "message", "add_time", "has_read"]


class UserFavoriteAdmin(object):
    list_display = ["user", "fav_id", "add_time", "fav_type"]
    search_fields = ["user", "fav_id", "fav_type"]
    list_filter = ["user", "fav_id", "add_time", "fav_type"]


class CourseCommentsAdmin(object):
    list_display = ["user", "course", "add_time", "comments"]
    search_fields = ["user", "course", "add_time", "comments"]
    list_filter = ["user", "course", "add_time", "comments"]


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
