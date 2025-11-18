from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .agent import run_agent

@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=400)

    data = json.loads(request.body.decode("utf-8"))
    user_message = data.get("message", "")

    if not user_message:
        return JsonResponse({"error": "message field required"}, status=400)

    bot_response = run_agent(user_message)

    return JsonResponse({"response": bot_response})
