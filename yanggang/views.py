from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from yanggang.models import Message, UserProfile
from yanggang.serializers import MessageSerializer
from django.db.utils import IntegrityError


def home(request):
    return render(request, 'yanggang/home.html')


def success(request):
    return render(request, 'yanggang/success.html')


def canceled(request):
    return render(request, 'yanggang/canceled.html')


@csrf_exempt
def create_user(request, pk=None):
    if request.method == 'POST':
        # data = JSONParser().parse(request)
        # print(data)
        try:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            user.save()
        except IntegrityError:
            return JsonResponse({'error': 'User Already Exists!'}, status=400)
        try:
            UserProfile.objects.create(user=user)
            return JsonResponse(request.POST, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)
    else:
        return JsonResponse({'error': "POST Only Method"}, status=400)


class Index(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse({'error': 'User Not Logged On'}, status=200)

    def post(self, request):
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            # Log user in
            login(request, user)
            return JsonResponse({request.POST['username']: 'Logged On'}, status=200)
        else:
            return HttpResponse('{"error": "User does not exist"}')


class UserQuery(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username=None):
        if username:
            try:
                print(username)
                users = User.objects.get(username=username)
                return JsonResponse({'username': users.username}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User Not Found'}, status=400)
        else:
            return JsonResponse({'error': 'Must Supply User Name'}, status=400)


class MessageList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, sender=None, receiver=None, is_read=False):
        sender = User.objects.get(username=sender)
        receiver = User.objects.get(username=receiver)
        if is_read:
            messages = Message.objects.filter(sender=sender, receiver=receiver)
        else:
            messages = Message.objects.filter(sender=sender, receiver=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request):
        data = request.data.dict()
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
