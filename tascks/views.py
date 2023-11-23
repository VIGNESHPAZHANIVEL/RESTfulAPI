# tasks/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from django.core.exceptions import ObjectDoesNotExist
import json

@csrf_exempt
def task_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        data = [{'id': task.id, 'title': task.title, 'description': task.description} for task in tasks]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data['title']
            description = data['description']
            task = Task.objects.create(title=title, description=description)
            return JsonResponse({'id': task.id, 'title': task.title, 'description': task.description}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

@csrf_exempt
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

    if request.method == 'GET':
        data = {'id': task.id, 'title': task.title, 'description': task.description}
        return JsonResponse(data)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            title = data['title']
            description = data['description']
            task.title = title
            task.description = description
            task.save()
            return JsonResponse({'id': task.id, 'title': task.title, 'description': task.description})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Task deleted successfully'}, status=204)
