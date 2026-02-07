from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId
from datetime import date
import json

from .mongo import subjects_col, users_col, attendance_col


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = users_col.find_one({
            "username": username,
            "password": password
        })

        if user:
            request.session["user"] = username
            return redirect("/attendance/")
        else:
            return render(request, "login.html", {
                "error": "Invalid credentials"
            })

    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "register.html", {
                "error": "All fields are required"
            })

        if users_col.find_one({"username": username}):
            return render(request, "register.html", {
                "error": "User already exists"
            })

        # ✅ Store user
        users_col.insert_one({
            "username": username,
            "password": password
        })

        # ✅ Redirect to login page
        return redirect("/")

    return render(request, "register.html")


def attendance_view(request):
    if not request.session.get("user"):
        return redirect("/")

    return render(request, "attendance.html", {
        "username": request.session["user"]
    })



# ---------- APIs ----------
def get_subjects(request):
    if not request.session.get("user"):
        return JsonResponse([], safe=False)

    data = []
    for s in subjects_col.find({"username": request.session["user"]}):
        data.append({
            "id": str(s["_id"]),
            "name": s["name"],
            "total": s["total"],
            "present": s["present"]
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def add_subject(request):
    if not request.session.get("user"):
        return JsonResponse({"error": "Not logged in"}, status=401)

    if request.method == "POST":
        body = json.loads(request.body)

        subjects_col.insert_one({
            "username": request.session["user"],  # 🔑 LINK TO USER
            "name": body["name"],
            "total": 0,
            "present": 0
        })

        return JsonResponse({"status": "ok"})


@csrf_exempt
def mark_attendance(request):
    if not request.session.get("user"):
        return JsonResponse({"error": "Not logged in"}, status=401)

    data = json.loads(request.body)

    # 1️⃣ store attendance history
    attendance_col.insert_one({
        "username": request.session["user"],
        "subject": data["subject"],
        "status": data["status"],
        "date": str(date.today())
    })

    # 2️⃣ update subject totals
    update = {"$inc": {"total": 1}}
    if data["status"] == "Present":
        update["$inc"]["present"] = 1

    subjects_col.update_one(
        {
            "name": data["subject"],
            "username": request.session["user"]  # 🔒 USER SAFETY
        },
        update
    )

    return JsonResponse({"message": "Attendance saved"})


@csrf_exempt
def delete_subject(request):
    if not request.session.get("user"):
        return JsonResponse({"error": "Not logged in"}, status=401)

    body = json.loads(request.body)

    subjects_col.delete_one({
        "_id": ObjectId(body["id"]),
        "username": request.session["user"]  # 🔐 USER CHECK
    })

    return JsonResponse({"status": "deleted"})


