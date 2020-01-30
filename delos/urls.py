from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from . import views
from . import accounts

urlpatterns = [
    path('', views.home, name='home'),
    path('api/oauth/', accounts.oauth, name='oauth'),
    path('api/login/', accounts.login, name='detail'),
    path('api/unlink/', accounts.unlink, name='unlink'),
    path('api/withdraw/', accounts.withdraw, name='withdraw'),
    path('api/token/', obtain_jwt_token, name='obtain_token'),
    path('api/token/verify/', verify_jwt_token),
    path('api/token/refresh/', refresh_jwt_token),

    path('api/loginKakao', accounts.loginKAkaoView.as_view()),
    path('api/group', views.groupView.as_view()),
    path('api/groupMember', views.groupMemberView.as_view()),
    path('api/latestGroupNotice', views.latestGroupNoticeView.as_view()),
    path('api/groupNotice', views.groupNoticeView.as_view()),
    path('api/groupSchedule', views.groupScheduleView.as_view()),
    path('api/groupBoard', views.groupBoardView.as_view()),
    path('api/timeTable', views.timeTableView.as_view()),
    path('api/personalSchedule', views.personalScheduleView.as_view()),
    path('api/survey', views.surveyView.as_view()),
    path('api/mainSurvey', views.mainSurveyView.as_view()),
    path('api/mySurvey', views.mySurveyView.as_view()),
    path('api/updateSurvey', views.updateSurveyView.as_view()),
    path('api/surveyQuestion', views.surveyQuestionView.as_view()),
    path('api/surveyAnswer', views.surveyAnswerView.as_view()),
    path('api/groupBoardCharged', views.groupBoardChargedView.as_view()),
    path('api/groupTimeTableView', views.groupTimeTableView.as_view())
]