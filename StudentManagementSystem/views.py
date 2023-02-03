from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from .models import CustomUser, Conversation, ChatMessage
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')


def loginUser(request):
    return render(request, 'login.html')


def doLogin(request):
    email_id = request.GET.get('email')
    password = request.GET.get('password')
    user_type = request.GET.get('user_type')
    print(email_id)
    print(password)
    print(request.user)
    if not (email_id and password):
        messages.error(request, "Please provide all the details!!")
        return render(request, 'login.html')

    user = CustomUser.objects.filter(email=email_id, password=password).last()
    if not user:
        messages.error(request, 'Invalid Login Credentials!!')
        return render(request, 'login.html')

    login(request, user)
    print(request.user)

    if user.user_type == CustomUser.STUDENT:
        return redirect('student_home/')
    elif user.user_type == CustomUser.TEACHER:
        return redirect('teacher_home/')

    return render(request, 'home.html')


def registration(request):
    return render(request, 'registration.html')


def doRegistration(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    email_id = request.GET.get('email')
    password = request.GET.get('password')
    confirm_password = request.GET.get('confirmPassword')

    print(email_id)
    print(password)
    print(confirm_password)
    print(first_name)
    print(last_name)
    if not (email_id and password and confirm_password):
        messages.error(request, 'Please provide all the details!!')
        return render(request, 'registration.html')

    if password != confirm_password:
        messages.error(request, 'Both passwords should match!!')
        return render(request, 'registration.html')

    is_user_exists = CustomUser.objects.filter(email=email_id).exists()

    if is_user_exists:
        messages.error(request, 'User with this email id already exists. Please proceed to login!!')
        return render(request, 'registration.html')

    username = email_id.split('@')[0].split('.')[0]

    if CustomUser.objects.filter(username=username).exists():
        messages.error(request, 'User with this username already exists. Please use different username')
        return render(request, 'registration.html')

    user = CustomUser()
    user.username = username
    user.email = email_id
    user.password = password
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def conversations(request):
    C1 = Q(member1=request.user.id)
    C2 = Q(member2=request.user.id)
    users = CustomUser.objects.exclude(id=request.user.id)
    context = {
        "users": users,
    }
    return render(request, "conversations.html", context)


def chat(request, id):
    to_id = id
    from_id = request.user.id
    messages = []
    C1 = Q(member1=to_id)
    C2 = Q(member2=from_id)
    C3 = Q(member1=from_id)
    C4 = Q(member2=to_id)
    if Conversation.objects.filter(C1 & C2).exists():
        conversation = Conversation.objects.get(C1 & C2)
    elif Conversation.objects.filter(C3 & C4).exists():
        conversation = Conversation.objects.get(C3 & C4)
    else:
        conversation = Conversation(member1=from_id, member2=to_id)
        conversation.save()

    if ChatMessage.objects.filter(conversation_id=conversation.id).exists():
        chat_messages = ChatMessage.objects.filter(conversation_id=conversation.id)
        messages = chat_messages
    sender = CustomUser.objects.get(id=request.user.id)
    to = CustomUser.objects.get(id=to_id)
    context = {
        "id": conversation.id,
        "from": sender,
        "to": to,
        "messages": messages,
    }
    return render(request, "chat.html", context)


@csrf_exempt
def sendMessage(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('conversations/')
    else:
        conv_id = request.POST.get('conv_id')
        sender_id = request.POST.get('sender_id')
        to_id = request.POST.get('to_id')
        message_to_send = request.POST.get('new_message')
        sender = CustomUser.objects.get(id=sender_id)
        conversation = Conversation.objects.get(id=conv_id)
        chat_message = ChatMessage(conversation_id=conversation, to_id=to_id, from_id=sender, text=message_to_send)
        chat_message.save()

        return redirect('chat/'+to_id)


