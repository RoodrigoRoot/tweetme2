from django.conf import settings
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from rest_framework .authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from .models import Tweet
from .forms import Tweetform
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializers import TweetSerilizer, TweetActionSerializer
# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html')


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerilizer(obj)
    return Response(serializer.data)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)

    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message":"You canot delete this tweet"}, status=403)

    obj = qs.first()
    obj.delete()
    return Response({"message":"Tweet removed"}, status=200)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):

    """
    id is required.
    Actions options are: Like, Unlile, retweet.
    """
    serializer = TweetActionSerializer(request.POST)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")

    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    if action == "like":
        obj.likes.add(request.user)
    elif action == "unlike":
        obj.likes.remove(request.user)
    elif action == "retweet":
        pass

    return Response({"message":"Tweet removed"}, status=200)




@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerilizer(qs, many=True)
    return Response(serializer.data)




def tweet_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [x.serialize() for x in qs]
    data = {
        "isUser":False,
        "response": tweet_list
    }
    return JsonResponse(data)



def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by  JavaScript or Swift, Java/ etc
    """
    data = {
            "id":tweet_id
        }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        obj["content"] = obj.content
    except Exception as e:
        data["message"] = "Not Found"
        status = 400
    return JsonResponse(data, status=status)


@api_view(['POST']) # http method
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerilizer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)



def tweet_create_view_pure_django(request, *args, **kwargs):
    """ 
    Rest Create Tweet
    """
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = Tweetform(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user or None
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)

        if next_url is not None and is_safe_url(next_url, ALLOWED_HOSTS) :
            return redirect(next_url)
        form = Tweetform()  
    if form.errors:
        return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', {"form":form})
