from django.shortcuts import render
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

# Create your views here.


@api_view(['GET', 'POST'])
def task_list_view(request):
    if request.method == 'GET':
        task_list = Task.objects.all()
        data = TaskSerializer(instance=task_list, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        completed = request.data.get('completed')

        task = Task.objects.create(
            title=title, description=description, completed=completed
        )
        return Response(data={'task_id': task.id},
                        status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def task_list_detail_view(request, id):
    try:
        task_list_detail = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'message': 'Task is not found'})
    if request.method == 'GET':
        data=TaskSerializer(instance=task_list_detail, many=False).data
        return Response(data=data)
    if request.method == 'PUT':
        task_list_detail.title = request.data.get('title')
        task_list_detail.description = request.data.get('description')
        task_list_detail.price = request.data.get('price')
        task_list_detail.category_id = request.data.get('category_id')
        task_list_detail.save()

        return Response(data={'car_list_detail_id': task_list_detail.id},
                        status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        task_list_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)