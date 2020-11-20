from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Post, Comments,Project, FSI_user
from .serializers import GetPostSerialize, GetCommentsSerialize, GetAllProjectSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Sum
from rest_framework.parsers import JSONParser
from django.db.models import Subquery
from django.http.response import JsonResponse
from rest_framework import permissions, status

import torch
import torch.nn as nn
import pickle 

import os, sys, inspect

sys.path.append(os.getcwd())
from model.dataCollector import getUserPage, collectData, getPageNames, getLongTermUserToken
from model.model import getReviewPredictList

# Create your views here.


# get, put, delete cac chien dich voi tung projectid
@api_view(['GET', 'POST', 'DELETE', "PUT"])
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return JsonResponse({'message': 'The Project does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        project_serializer = GetAllProjectSerializer(project)
        return JsonResponse(project_serializer.data)

    elif request.method == 'PUT':
        project_data = JSONParser().parse(request)
        project_serializer = GetAllProjectSerializer(project, data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            return JsonResponse(project_serializer.data)
        return JsonResponse(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return JsonResponse({'message': 'Project was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


# get cac chien dich voi tung userid, post chien dich
@api_view(['GET', 'POST', 'DELETE'])
def project(request,user_id):
    if request.method == 'GET':
        project = Project.objects.filter(user_id=user_id)
        project_serializer = GetAllProjectSerializer(project, many=True)
        return JsonResponse(project_serializer.data, safe=False)

    elif request.method == 'POST':
        project_data = JSONParser().parse(request)

        project_serializer = GetAllProjectSerializer(data=project_data)
        if project_serializer.is_valid():
            project_serializer.save()
            print(project_serializer)
            return JsonResponse(project_serializer.data, status=status.HTTP_201_CREATED)
        print(project_serializer)
        return JsonResponse(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#lay ra post tich cuc co nhieu like nhat trong chien dich
@api_view(['GET', 'POST', 'DELETE'])
def GetPostMostLikeInProject(request, project_id):
    if request.method == 'GET':
        list_post = Post.objects.filter(project_id = project_id).order_by('-num_likes')[:5]
        mydata = GetPostSerialize(list_post, many=True)
        return JsonResponse(mydata.data, safe=False)


#lay ra tong so luot like tat ca cac bai post trong 1 project
@api_view(['GET', 'POST', 'DELETE'])
def GetPostLikeInProject(request, project_id):
    if request.method == 'GET':
        numLike = Post.objects.filter(project_id = project_id).aggregate(Sum('num_likes'))
        return JsonResponse(numLike,safe=False)


#lay ra tong so luot comment tat ca cac bai post trong 1 project
@api_view(['GET', 'POST', 'DELETE'])
def GetPostCommentInProject(request, project_id):
    if request.method == 'GET':
        numComment = Post.objects.filter(project_id = project_id).aggregate(Sum('num_comments'))
        return JsonResponse(numComment,safe=False)


#lay ra tong so cac bai post trong 1 project
@api_view(['GET', 'POST', 'DELETE'])
def GetNumPost(request, project_id):
    if request.method == 'GET':
        numPost = Post.objects.filter(project_id = project_id).count()
        return JsonResponse(numPost,safe=False)

# lay ra tong so tich cuc trong 1 chien dich
@api_view(['GET', 'POST', 'DELETE'])
def GetAllNumComment1(request,project_id):
    if request.method == 'GET':
        checkpost = Post.objects.filter(project_id = project_id)
        cmt = Comments.objects.filter(post_id__in = Subquery(checkpost.values('id')), effect = '1').count()

        # cmt_serializer = GetCommentsSerialize(cmt, many=True)
        # checkpost_serializer=GetPostSerialize(checkpost, many=True)
        return JsonResponse(cmt, safe=False)

# lay ra tong so tieu cuc trong 1 chien dich
@api_view(['GET', 'POST', 'DELETE'])
def GetAllNumComment_1(request,project_id):
    if request.method == 'GET':
        checkpost = Post.objects.filter(project_id = project_id)
        cmt = Comments.objects.filter(post_id__in = Subquery(checkpost.values('id')), effect = '-1').count()

        # cmt_serializer = GetCommentsSerialize(cmt, many=True)
        # checkpost_serializer=GetPostSerialize(checkpost, many=True)
        return JsonResponse(cmt, safe=False)

# lay ra tong so trung lap trong 1 chien dich
@api_view(['GET', 'POST', 'DELETE'])
def GetAllNumComment0(request,project_id):
    if request.method == 'GET':
        checkpost = Post.objects.filter(project_id = project_id)
        cmt = Comments.objects.filter(post_id__in = Subquery(checkpost.values('id')), effect = '0').count()

        # cmt_serializer = GetCommentsSerialize(cmt, many=True)
        # checkpost_serializer=GetPostSerialize(checkpost, many=True)
        return JsonResponse(cmt, safe=False)





# lay ra cmt tich cuc nhieu like nhat trong 1 chien dich
@api_view(['GET', 'POST', 'DELETE'])
def GetComment1MostLike(request,project_id):
    if request.method == 'GET':
        checkpost = Post.objects.filter(project_id = project_id)
        cmt = Comments.objects.filter(post_id__in = Subquery(checkpost.values('id')), effect = '1').order_by('-num_likes')[:5]
        cmt_serializer = GetCommentsSerialize(cmt, many =True)
        return JsonResponse(cmt_serializer.data, safe=False)

# lay ra cmt tieu cuc nhieu like nhat trong 1 chien dich
@api_view(['GET', 'POST', 'DELETE'])
def GetComment_1MostLike(request,project_id):
    if request.method == 'GET':
        checkpost = Post.objects.filter(project_id = project_id)
        cmt = Comments.objects.filter(post_id__in = Subquery(checkpost.values('id')), effect = '-1').order_by('-num_likes')[:5]
        cmt_serializer = GetCommentsSerialize(cmt, many=True)
        return JsonResponse(cmt_serializer.data, safe=False)

#get ra tat ca cac cmt
@api_view(['GET', 'POST', 'DELETE'])
def GetAllCmt(request, project_id):
    if(request.method == 'GET'):
        checkpost = Post.objects.filter(project_id = project_id)
        cmt = Comments.objects.filter(post_id__in = Subquery(checkpost.values('id')))
        cmt_serializer = GetCommentsSerialize(cmt, many=True)
        return JsonResponse(cmt_serializer.data, safe=False)



# @api_view(['GET'])
# def current_user(request):
#     """
#     Determine the current user by their token, and return their data
#     """
#
#     serializer = UserSerializer(request.user)
#     return Response(serializer.data)

#
# class UserList(APIView):
#     """
#     Create a new user. It's called 'UserList' because normally we'd have a get
#     method here too, for retrieving a list of all User objects.
#     """
#
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, format=None):
#         serializer = UserSerializerWithToken(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

@api_view(['GET', 'POST', 'DELETE', "PUT"])
def UpdateGetCmtId(request, cmt_id):
    try:
        comment = Comments.objects.get(id=cmt_id)
    except Project.DoesNotExist:
        return JsonResponse({'message': 'The Project does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        comment_serializer = GetCommentsSerialize(comment)
        return JsonResponse(comment_serializer.data)

    elif request.method == 'PUT':
        comment_data = JSONParser().parse(request)
        comment_serializer = GetCommentsSerialize(comment, data=comment_data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return JsonResponse(comment_serializer.data)
        return JsonResponse(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST', 'DELETE', "PUT"])
def user_detail(request, user_id):
    try:
        user = FSI_user.objects.get(id=user_id)
    except Project.DoesNotExist:
        return JsonResponse({'message': 'The Project does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return JsonResponse(user_serializer.data)


    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'Project was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'POST':
        user_data = JSONParser().parse(request)

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            print(user_serializer)
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
#   Có token mới từ frontend gửi lên thì lấy longterm token luôn bằng hàm getLongTermUserToken
#   Chỉ lưu longterm token, vì token này không có hạn, còn token thường hết hạn rất nhanh 
#   Thay các đoạn hardcode của tớ bằng data frontend gửi lên nhé.

#
#   Nhận user access token, page id và keyword vào đây để collect data về.
#
@api_view(['GET'])
def collectCommentPages(request):
    user_access_token = 'EAAPBbNbQICIBAGRldRZBa9RyzvSEhICKt2HRCByCK4bBPf3EFZCZCwLLMrWbQsnZAOb0NB4IHAP6e5BKQ8SmpBLwG8F6g1K68r8pCUNGqadWHH84hiKgRjjcmLBqN0pd1pGaohX3P1wUv3ZACvj2clYYBuW3w8ZAFPAjyeGj369yZBB59YD718RLZCJBbdVtE07ZBCqwBJYlVcAtaWEtugGHSZCEMoSOVXaCFhZCzZCCAIZB0rgZDZD'
    page_id = "101858671714061"
    keywords = ['merakee']
    page_id, page_access_token, keywords = getUserPage(user_access_token, page_id, keywords)
    commentRows, likeRows = collectData(page_id,page_access_token, keywords)
    for comment in commentRows:
        print('Saving...')
        comment = Comments(id=comment['CommentID'], post_id=comment['PostID'], content=comment['Comment'], effect=comment['Label'])
        comment.save()

    # Them doan luu like cua post vao day
    #
    #
    for like in likeRows:
        post = Post()
        post.save()
    return JsonResponse({'data': { 'comment': commentRows, 'like': likeRows }}, status=status.HTTP_200_OK)

#
#   Trả về tuple (tên page, id page) để  người dùng chọn.
#
@api_view(['GET'])
def getUserPages(request):
    user_id = '1583394658488997'
    user_access_token = 'EAAPBbNbQICIBACZCJIqPBoVZCD0kjLHfYTbFQeZAbKXXHoEjZAgkkUFr11W6kmJonvM4Jsgl280U2RbZBY3h94aCiAIixRhAZCoIYted5UyVe15rcZAPzQyaGHolFZBBQ0RqnkSDlx53aKZAtsQizwxxdi8SHZCfxZCXnrpNGYHtEqqIMJUj5b6YHZCZAss0rJxn0iCWWXsUO0FR6e6yQ1Vr2SwsxuYJDRq97pAMHvl2UXZB2dbgZDZD'
    pages = getPageNames(user_access_token, user_id)
    return JsonResponse({'data': pages}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getPredictions(request):
    predictions = getReviewPredictList(None)
    return JsonResponse({'data': predictions}, status=status.HTTP_200_OK)