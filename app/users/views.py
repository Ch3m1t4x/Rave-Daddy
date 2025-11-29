import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user_model

User = get_user_model()

# @csrf_exempt
def api_register(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = body.get("username")
    password = body.get("password")
    email = body.get("email")

    if not username or not password or not email:
        return JsonResponse({"error": "Missing fields"}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already in use"}, status=409)

    user = User.objects.create_user(username=username, email=email, password=password)

    login(request, user)

    return JsonResponse({"success": True, "username": user.username})


# @csrf_exempt
def api_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return JsonResponse({"error": "Missing fields"}, status=400)

    user = authenticate(request, email=email, password=password)

    if user is None:
        return JsonResponse(
            {"success": False, "message": "Invalid credentials"}, status=401
        )

    login(request, user)

    return JsonResponse({"success": True, "username": user.username})

def logout_view(request):
    logout(request)
    return JsonResponse({"success": True})