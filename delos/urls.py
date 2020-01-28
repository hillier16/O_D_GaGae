from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from . import views
from . import apis
from . import accounts

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
    path('api/oauth/', accounts.oauth, name='oauth'),
    path('api/loginKakao/', accounts.login, name='detail'),
    path('api/unlink/', accounts.unlink, name='unlink'),
    path('api/withdraw/', accounts.withdraw, name='withdraw'),
    path('api/token/', obtain_jwt_token, name='obtain_token'),
    path('api/token/verify/', verify_jwt_token),
    path('api/token/refresh/', refresh_jwt_token),
  
    path('api/group', apis.groupView.as_view()),
    path('api/groupMember', apis.groupMemberView.as_view()),
    path('api/latestGroupNotice', apis.latestGroupNoticeView.as_view()),
    path('api/groupNotice', apis.groupNoticeView.as_view()),
    path('api/groupSchedule', apis.groupScheduleView.as_view()),
    path('api/personalSchedule', apis.personalScheduleView.as_view()),
    path('api/survey', apis.surveyView.as_view()),
    path('api/mainSurvey', apis.mainSurveyView.as_view()),
    path('api/mySurvey', apis.mySurveyView.as_view()),
    path('api/updateSurvey', apis.updateSurveyView.as_view()),
]