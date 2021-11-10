from django.core.exceptions import ObjectDoesNotExist
from django.db.models import query
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import serializers
from .serializers import TodoSerializer
from .models import Todo

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, mixins

# Create your views here.


def home(request):
    return HttpResponse('<center><h1 style="background-color:powderblue;">Welcome to ApiTodo</h1></center>')


@api_view(['GET'])
def todoList(request):
    querset = Todo.objects.all()

    serializer = TodoSerializer(querset, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def todoListCreate(request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def toDo_list(request):

    if request.method == 'GET':
        querset = Todo.objects.all()
        serializer = TodoSerializer(querset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def todoListUpdate(request, pk):

    querset = Todo.objects.get(id=pk)

    serializer = TodoSerializer(instance=querset, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['DELETE'])
def todoListDelete(request, pk):
    querset = Todo.objects.get(id=pk)
    querset.delete()
    return Response("Item Deleted")


@api_view(['GET', 'PUT', 'DELETE'])
def toDo_detail(request, pk):
    querset = Todo.objects.get(id=pk)

    if request.method == 'GET':
        serializer = TodoSerializer(querset)
        return Response(serializer.data)

    elif request.method == 'PUT':

        serializer = TodoSerializer(instance=querset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == 'DELETE':

        querset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


############### API View ########################

class TodoList(APIView):

    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(Todo, pk=pk)

    def get(self, request, pk):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            serializer._data["success"] = "Todo succesfully updated.."
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


################## GenericAPI View ##############################


class TodoListCreate(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
