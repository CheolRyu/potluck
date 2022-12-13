from django.shortcuts import render, redirect
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm, EventForm, FriendForm, ItemForm, ItemUpdate, EntertainmentForm
from .models import Profile, Event, Friend, Item, Guest, Entertainment
from django.core.mail import send_mass_mail


def index(request):
    return home(request)


def login(request):
    form = LoginForm()
    user_found = True
    if request.method == 'POST':
        print("POST REQUEST")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print("User:", user)
        if user is not None:
            auth_login(request, user)
            print("Auth'd user")
            return redirect('potluck:home')
        else:
            user_found = False
            return render(request, 'potluck/login.html', {'form': form, 'user_found': user_found})
    else:
        print("Served form")
        return render(request, 'potluck/login.html', {'form': form, 'user_found': user_found})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        user = User.objects.create_user(
            username, email, password, first_name=first_name, last_name=last_name)
        if user is not None:
            return redirect('potluck:home')
    else:
        form = SignupForm()

    # form may be unbound, probably never an issue
    return render(request, 'potluck/signup.html', {'form': form})


@login_required
def home(request):
    profile = Profile.objects.get(user=request.user)
    events = Event.objects.all()
    return render(request, 'potluck/home.html', {'profile': profile, 'events': events})


@login_required
def create_event(request):
    user = request.user
    items = Item.objects.all()
    event_form = EventForm()
    context = {
        'user': user,
        'items': items,
        'event_form': event_form,
    }
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        apt = request.POST['apt']
        description = request.POST['description']
        start = request.POST['start']
        time = request.POST['time']
        owner = Profile.objects.get(user=user)
        Event.objects.create(
            name=name,
            address=address,
            city=city,
            description=description,
            owner=owner,
            state=state,
            zip_code=zip_code,
            apt=apt,
            time=time,
            start=start
        )

        # send email to friends
        friends = Friend.objects.filter(current_user=owner)
        emails = list(map(lambda friend: friend.user.user.email, friends))
        message = (
            str("Your friend has created a new event!"),
            ("Your friend " +
             str(owner) + " has created a new event! Log on to check it out."),
            str("donotreply@potluck.com"),
            emails
        )
        try:
            send_mass_mail([message], fail_silently=False)
            print("SENT MAIL")
        except Exception:
            print("FAILED TO SEND MAIL")

        return redirect('potluck:addItem', event_id=Event.objects.get(name=name).id)
    return render(request, 'potluck/create_event.html', context)


@login_required
def addItem(request, event_id):
    event = Event.objects.get(id=event_id)
    items = Item.objects.filter(event=event)
    form = ItemForm()
    if request.method == 'POST':
        event = Event.objects.get(id=event_id)
        name = request.POST['name']
        quantity = request.POST['quantity']
        price = request.POST['price']
        status= request.POST['status']
        description = request.POST['description']
        Item.objects.create(
            event=event,
            name=name,
            description=description,
            quantity=quantity,
            status=status,
            price=price
        )
        return redirect('potluck:addItem', event_id=event_id)
    return render(request, 'potluck/add_item.html', {'form': form, 'event': event, 'items': items})

@login_required
def addGuest(request, event_id):
    event = Event.objects.get(id=event_id)
    profile = Profile.objects.get(user = request.user)
    Guest.objects.create(event = event, profile = profile)
    return redirect('potluck:addEntertainment', event_id=event_id)
    
    # guestid = Guest.objects.get(profile = profile).id

@login_required
def addEntertainment(request, event_id):
    event = Event.objects.get(id=event_id)
    form = ItemForm()
    
    if request.method == 'POST':
        event = Event.objects.get(id=event_id)
        category = request.POST['category']
        description = request.POST['description']
        Entertainment.objects.create(
            event=event,
            category=category,
            description=description,
            
        )
        return redirect('potluck:addEntertainment', event_id=event_id)
    return render(request, 'potluck/entertainment.html', {'form': form, 'event': event})

def finish(request, event_id):
    items = Item.objects.filter(event=event_id)
    print(items)
    for item in items:
        if item.status == 'Yes':
            item.owner = request.user
        else:
            item.fulfilled = False
        item.save()
    return redirect('potluck:home')
@login_required
def detail(request, event_id):
    event = Event.objects.get(id=event_id)
    items = Item.objects.filter(event=event)
    return render(request, 'potluck/detail.html', {'event': event, 'items': items})


@login_required
def update(request, event_id):
    event = Event.objects.get(id=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('potluck:home')
    return render(request, 'potluck/create_event.html', {'form': form, 'event': event})


@login_required
def attend(request, event_id):
    user = request.user
    event = Event.objects.get(id=event_id)
    profile = Profile.objects.get(user=request.user)
    items = Item.objects.filter(event=event_id, status='no')
    form = ItemUpdate()
    entertainmentForm = EntertainmentForm()
    if request.method == 'POST':
        if 'status' in request.POST and request.POST['status'] == 'yes':
            # Item.objects.filter(event=event_id).update(fulfilled=True)
            return redirect('potluck:home')
        else:
            return redirect('potluck:home')
    return render(request, 'potluck/attend_confirm.html', {'form': form, 'entertainmentForm': entertainmentForm, 'event': event, 'user': user, 'items': items})


@login_required
def friends(request):
    profile = Profile.objects.get(user=request.user)
    try:
        friends = Friend.objects.filter(current_user=profile)
    except Friend.DoesNotExist:
        friends = None
    return render(request, 'potluck/friends.html', {'profile': profile, 'friends': friends})


@login_required
def add_friend(request):
    form = FriendForm()
    if request.method == 'POST':
        new_friend_email = request.POST['new_friend_email']
        try:
            new_friend_user = User.objects.get(email=new_friend_email)
            new_friend_profile = Profile.objects.get(user=new_friend_user)
            Friend.objects.create(
                user=new_friend_profile, current_user=Profile.objects.get(user=request.user))
            return redirect('potluck:friends')
        except User.DoesNotExist:
            return render(request, 'potluck/add_friend.html', {'form': form, 'success': False})
    else:
        return render(request, 'potluck/add_friend.html', {'form': form, 'success': None})
def profile(request):
    profile = Profile.objects.get(user=request.user)
    events = Event.objects.filter(owner=profile)
    return render(request, 'potluck/profile.html', {'profile': profile, 'events': events})