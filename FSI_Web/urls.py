from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
from .views import project_detail, project, GetPostMostLikeInProject, \
    GetPostLikeInProject, GetPostCommentInProject, GetNumPost, GetAllNumComment1, GetAllNumComment0, GetAllNumComment_1\
    , GetComment1MostLike, GetComment_1MostLike,  GetAllCmt, UpdateGetCmtId, user_detail, collectCommentPages, getUserPages, getPredictions
urlpatterns = [
# get cac chien dich voi tung userid, post chien dich
    url(r'^all_project/(?P<user_id>[0-9]+)$', project),
# get, put, delete cac chien dich voi tung projectid
    url(r'^project_id/(?P<pk>[0-9]+)$', project_detail),
#get post nhieu like nhat theo tung project khi post co the them id bat ky o dang sau
    url(r'^post_mostlike/(?P<project_id>[0-9]+)$', GetPostMostLikeInProject),
#lay ra tong so luot like tat ca cac bai post trong 1 project
    url(r'^post_alllike/(?P<project_id>[0-9]+)$', GetPostLikeInProject),
#lay ra tong so luot comment tat ca cac bai post trong 1 project
    url(r'^num_comment/(?P<project_id>[0-9]+)$', GetPostCommentInProject),
#lay ra tong so tat ca cac bai post trong 1 project
    url(r'^num_post/(?P<project_id>[0-9]+)$', GetNumPost),
#lay ra tong so tich cuc trong 1 project
    url(r'^num_cmt1/(?P<project_id>[0-9]+)$', GetAllNumComment1),
#lay ra tong so tieu cuc trong 1 project
    url(r'^num_cmt_1/(?P<project_id>[0-9]+)$', GetAllNumComment_1),
#lay ra tong so trung lap trong 1 project
    url(r'^num_cmt0/(?P<project_id>[0-9]+)$', GetAllNumComment0),
#get, post,delete user theo id, khi post id dang sau cu cho mac dinh la 1
    url(r'^user/(?P<user_id>[0-9]+)$', user_detail),
#get 5 cmt tich cuc nhieu like nhat
    url(r'^cmt1/(?P<project_id>[0-9]+)$', GetComment1MostLike),
#get tat ca cmt
    url(r'^all_cmt/(?P<project_id>[0-9]+)$', GetAllCmt),
#get 5 cmt tieu cuc nhieu like nhat
    url(r'^cmt_1/(?P<project_id>[0-9]+)$', GetComment_1MostLike),
#get, put cmt theo id
    url(r'^cmt/(?P<cmt_id>[0-9]+)$', UpdateGetCmtId),
# Get predictions
    url(r'^collect', collectCommentPages),
# Get pages
    url(r'^pages', getUserPages),
# Get predictions
    url(r'^predictions', getPredictions),

# #jwt
#     url(r'^current_user/$', current_user),
#     url(r'^users/$', UserList.as_view()),
#     path('token-auth/', obtain_jwt_token)
]