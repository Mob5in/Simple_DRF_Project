from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer, UserSerializer
from rest_framework import status, generics, mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

User = get_user_model()


# FBV part

@api_view(["GET", "POST"])
def all_todos(request: Request):
    if request.method == "GET":
        todos = Todo.objects.order_by("priority").all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response({"todos": todo_serializer.data}, status=status.HTTP_202_ACCEPTED)
    elif request.method == "POST":
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET", "PUT", "DELETE"])
def todo_detail_view(request: Request, todo_id: int):

    try:
        todo = Todo.objects.get(pk = todo_id)
    except Todo.DoesNotExist:
        return Response(None, status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = TodoSerializer(todo, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_406_NOT_ACCEPTABLE)
    elif request.method ==  "DELETE":
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
    


# CBV part


class TodoListApiView(APIView):
    def get(self, request: Request):
        todos = Todo.objects.order_by("priority").all()
        todo_serializer = TodoSerializer(todos, many=True)
        return Response({"todos": todo_serializer.data}, status=status.HTTP_202_ACCEPTED)
    def post(self, request: Request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(None, status.HTTP_400_BAD_REQUEST)
    


class TodoDetailApiView(APIView):

    def get_object(self, todo_id:int):
    
        try:
            todo = Todo.objects.get(pk = todo_id)
            return todo
        except Todo.DoesNotExist:
            return Response(None, status.HTTP_404_NOT_FOUND)
        



    def get(self, request:Request, todo_id:int):

        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status.HTTP_200_OK)



    def put(self, request:Request, todo_id:int):
        todo = self.get_object(todo_id)
        serializer = TodoSerializer(todo, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(None, status.HTTP_406_NOT_ACCEPTABLE)


    def delete(self, request:Request, todo_id:int):
        todo = self.get_object(todo_id)
        todo.delete()
        return Response(None, status.HTTP_204_NO_CONTENT)
    




# mixins part


class TodoListMixinsApiView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by("priority").all()

    serializer_class = TodoSerializer

    def get(self, request: Request):
        return self.list(request)

    def post(self, request: Request):
        return self.create(request)
    



class TodoDetailMixinsApiView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Todo.objects.order_by("priority").all()

    serializer_class = TodoSerializer

    def get(self, requset: Request, pk):
        return self.retrieve(requset, pk)
    

    def put(self, requset: Request, pk):
        return self.update(requset, pk)
    

    def delete(self, requset: Request, pk):
        return self.destroy(requset, pk)
    


# generics part


class TodoGenericsApiVeiw(generics.ListCreateAPIView):
    queryset = Todo.objects.order_by("priority").all()
    serializer_class = TodoSerializer

class TodoGenericsDetailApiVew(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.order_by("priority").all()
    serializer_class = TodoSerializer

# vewsets part

class TodosViewsetApiVew(viewsets.ModelViewSet):
    queryset = Todo.objects.order_by("priority").all()
    serializer_class = TodoSerializer




# user part


class UserGenericsApiVeiw(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
