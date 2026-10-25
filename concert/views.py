import json
import os
from pathlib import Path

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from concert.forms import LoginForm, SignUpForm
from concert.models import Concert, ConcertAttending
import requests as req


# Create your views here.

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request, data=request.POST)
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        if not username or not password:
            return render(request, "signup.html", {"form": form, "message": "Username and password are required."})
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"form": form, "message": "Username already exists."})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("index")
    return render(request, "signup.html", {"form": SignUpForm()})


def index(request):
    return render(request, "index.html")


def songs(request):
    service_url = os.environ.get("SONGS_SERVICE_URL", "http://127.0.0.1:8081")
    try:
        response = req.get(f"{service_url.rstrip('/')}/song", timeout=3)
        response.raise_for_status()
        catalogue = response.json()
        items = catalogue.get("songs", catalogue) if isinstance(catalogue, dict) else catalogue
    except (req.RequestException, ValueError):
        data_file = Path(__file__).resolve().parents[2] / "Back-End-Development-Songs" / "backend" / "data" / "songs.json"
        items = json.loads(data_file.read_text(encoding="utf-8")) if data_file.exists() else []
    return render(request, "songs.html", {"songs": items})


def photos(request):
    service_url = os.environ.get("PICTURES_SERVICE_URL", "http://127.0.0.1:8082")
    try:
        response = req.get(f"{service_url.rstrip('/')}/picture", timeout=3)
        response.raise_for_status()
        items = response.json()
    except (req.RequestException, ValueError):
        data_file = Path(__file__).resolve().parents[2] / "Back-End-Development-Pictures" / "backend" / "data" / "pictures.json"
        items = json.loads(data_file.read_text(encoding="utf-8")) if data_file.exists() else []
    return render(request, "photos.html", {"photos": items})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("index")
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("index")

def concerts(request):
    events = []
    for concert in Concert.objects.order_by("date"):
        attendance = None
        if request.user.is_authenticated:
            attendance = ConcertAttending.objects.filter(concert=concert, user=request.user).first()
        events.append({"concert": concert, "status": attendance.attending if attendance else "-"})
    return render(request, "concerts.html", {"concerts": events})


def concert_detail(request, id):
    if request.user.is_authenticated:
        obj = Concert.objects.get(pk=id)
        try:
            status = obj.attendee.filter(user=request.user).first().attending
        except:
            status = "-"
        return render(request, "concert_detail.html", {"concert_details": obj, "status": status, "attending_choices": ConcertAttending.AttendingChoices.choices})
    else:
        return HttpResponseRedirect(reverse("login"))
    pass


def concert_attendee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            concert_id = request.POST.get("concert_id")
            attendee_status = request.POST.get("attendee_choice")
            concert_attendee_object = ConcertAttending.objects.filter(
                concert_id=concert_id, user=request.user).first()
            if concert_attendee_object:
                concert_attendee_object.attending = attendee_status
                concert_attendee_object.save()
            else:
                ConcertAttending.objects.create(concert_id=concert_id,
                                                user=request.user,
                                                attending=attendee_status)

        return HttpResponseRedirect(reverse("concerts"))
    else:
        return HttpResponseRedirect(reverse("index"))
