from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes,APIView
from rest_framework.response import Response
from .models import Task, Project, ContributorRequest
from .serializers import TaskSerializer, ProjectSerializer, ContributorRequestSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import isOwner, isContributor, isAssigned
from rest_framework.generics import get_object_or_404

@api_view(['GET'])
def get_all_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class task_detail(APIView):
    permission_classes = [isOwner]
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'message':'You are not authenticated'},status=status.HTTP_401_UNAUTHORIZED)
        task = get_object_or_404(Task, pk=pk)
        
        if not isOwner.has_object_permission(request, self, task):
            return Response({'message':'You are not the owner of this task'},status=status.HTTP_403_FORBIDDEN)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):  
        if not request.user.is_authenticated:
            return Response({'message':'You are not authenticated'},status=status.HTTP_401_UNAUTHORIZED)
        task = get_object_or_404(Task, pk=pk)
        if not isOwner.has_object_permission(request, self, task):
            return Response({'message':'You are not the owner of this task'},status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_assigned_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_managed_tasks(request):
    tasks = Task.objects.filter(created_by=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([isAssigned])
def complete_task(request, pk):
    task = Task.objects.get(pk=pk)
    permission = isContributor()
    if not permission.has_object_permission(request,None,task): 
        return Response({'message':'You are not assigned to this task'},status=status.HTTP_403_FORBIDDEN)
    task.completed = True
    task.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_all_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class project_detail(APIView):
    permission_classes = [isOwner]
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)    
    
    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'message':'You are not authenticated'},status=status.HTTP_401_UNAUTHORIZED)
        project = get_object_or_404(Project, pk=pk)
        if not isOwner.has_object_permission(request, None, project):
            return Response({'message':'You are not the owner of this project'},status=status.HTTP_403_FORBIDDEN)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'message':'You are not authenticated'},status=status.HTTP_401_UNAUTHORIZED)
        project = get_object_or_404(Project, pk=pk)
        if not isOwner.has_object_permission(request, None, project):
            return Response({'message':'You are not the owner of this project'},status=status.HTTP_403_FORBIDDEN)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_managed_projects(request):
    projects = Project.objects.filter(created_by=request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_projects(request):
    projects = Project.objects.filter(contributors=request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated,isOwner])
def add_task_to_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not isOwner.has_object_permission(request, None, project):
        return Response({'message':'You are not the owner of this project'},status=status.HTTP_403_FORBIDDEN)
    project.tasks.add(request.data['task_id'])
    project.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated,isOwner])
def add_contributor_to_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not isOwner.has_object_permission(request, None, project):
        return Response({'message':'You are not the owner of this project'},status=status.HTTP_403_FORBIDDEN)
    project.contributors.add(request.data['user_id'])
    project.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated,isOwner])
def remove_contributor_from_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not isOwner.has_object_permission(request, None, project):
        return Response({'message':'You are not the owner of this project'},status=status.HTTP_403_FORBIDDEN)
    project.contributors.remove(request.data['user_id'])
    project.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated,isOwner])
def remove_task_from_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not isOwner.has_object_permission(request, None, project):
        return Response({'message':'You are not the owner of this project'},status=status.HTTP_403_FORBIDDEN)
    project.tasks.remove(request.data['task_id'])
    project.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST']) 
@permission_classes([IsAuthenticated,isOwner])
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.completed = True
    project.save()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_contributor_request(request, pk):
    project = get_object_or_404(Project, pk=pk)
    ContributorRequest.objects.create(project=project, user=request.user)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_contributor_request(request, pk,user_id):
    contributor_request = get_object_or_404(ContributorRequest, pk=pk,user_id=user_id)
    contributor_request.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated,isOwner])
def accept_contributor_request(request, pk):
    contributor_request = get_object_or_404(ContributorRequest, pk=pk)
    if not isOwner.has_object_permission(request, None, contributor_request.project):
        return Response({'message':'You are not the owner of this project'},status=status.HTTP_403_FORBIDDEN)
    contributor_request.accepted = True
    contributor_request.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated,isOwner])
def reject_contributor_request(request, pk):
    contributor_request = get_object_or_404(ContributorRequest, pk=pk)
    if not isOwner.has_object_permission(request, None, contributor_request.project):
        return Response({'message':'You are not the owner of this project'},status=status.HTTP_403_FORBIDDEN)
    contributor_request.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated,isOwner])
def view_contributor_requests(request, pk):
    contributor_requests = get_object_or_404(ContributorRequest, pk=pk)
    if not isOwner.has_object_permission(request, None, contributor_requests.project):
        return Response({'message':'You are not the owner of this project'},status=status.HTTP_403_FORBIDDEN)
    serializer = ContributorRequestSerializer(contributor_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_contributor_requests(request):
    contributor_requests = ContributorRequest.objects.all()
    serializer = ContributorRequestSerializer(contributor_requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_contributor_requests(request):
    contributor_requests = ContributorRequest.objects.filter(user=request.user)
    serializer = ContributorRequestSerializer(contributor_requests, many=True)
    return Response(serializer.data)



