from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .agent import chat_with_memory
from langchain_core.messages import HumanMessage

@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    body = json.loads(request.body)
    user_message = body.get("message", "")

    if not user_message:
        return JsonResponse({"error": "Empty message"}, status=400)

    # SESIÓN PARA USUARIOS ANÓNIMOS
    history_data = request.session.get("chat_history", [])

    # Convertimos la historia en HumanMessage / AIMessage reales
    history = []
    for msg in history_data:
        if msg["role"] == "user":
            history.append(HumanMessage(content=msg["content"]))
        else:
            from langchain_core.messages import AIMessage
            history.append(AIMessage(content=msg["content"]))

    # Ejecutar agente
    updated_history, reply = chat_with_memory(user_message, history)

    # Guardar historia en sesión
    session_friendly = []
    for msg in updated_history:
        if msg.__class__.__name__ == "HumanMessage":
            session_friendly.append({"role": "user", "content": msg.content})
        else:
            session_friendly.append({"role": "assistant", "content": msg.content})

    request.session["chat_history"] = session_friendly
    request.session.modified = True

    return JsonResponse({"response": reply})

