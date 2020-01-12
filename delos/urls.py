from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from . import apis

router = DefaultRouter()
router.register('user', views.UserViewSet)
router.register('personalSchedule', views.PersonalScheduleViewSet)
router.register('timeTable', views.TimeTableViewSet)
router.register('alarm', views.AlarmViewSet)
router.register('group', views.GroupViewSet)
router.register('groupMember', views.GroupMemberViewSet)
router.register('groupSchedule', views.GroupScheduleViewSet)
router.register('groupNotice', views.GroupNoticeViewSet)
router.register('groupBoard', views.GroupBoardViewSet)
router.register('survey', views.SurveyViewSet)
router.register('surveyQuestion', views.SurveyQuestionViewSet)
router.register('surveyAnswer', views.SurveyAnswerViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('oauth/', views.oauth, name='oauth'),
    path('loginKakao/', views.login, name='detail'),
    path('unlink/', views.unlink, name='unlink'),
    path('withdraw/', views.withdraw, name='withdraw'),

    path('api/getUserGroup/', apis.getUserGroup.as_view()),
    path('api/createGroup/', apis.createGroup.as_view())
]