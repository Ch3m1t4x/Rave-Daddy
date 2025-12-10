from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .agent import chat_with_memory
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from events.models import Evento

def get_sesion(request):
    # SESIÓN
    history_data = request.session.get("chat_history", [])

    # Convertimos la historia en HumanMessage / AIMessage reales
    history = []
    for msg in history_data:
        role = msg.get("role")
        content = msg.get("content")

        if role == "user":
            history.append(HumanMessage(content=content))
        elif role == "assistant":
            history.append(AIMessage(content=content))
        elif role == "tool":
            history.append(
                ToolMessage(
                    content=content,
                    tool_call_id=msg.get("tool_call_id"),
                    name=msg.get("name"),
                )
            )
    return history

def set_sesion(request,updated_history):
        # Guardar historia en sesión
    session_friendly = []
    for msg in updated_history:
        if isinstance(msg, HumanMessage):
            session_friendly.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            session_friendly.append({"role": "assistant", "content": msg.content})
        elif isinstance(msg, ToolMessage):
            session_friendly.append({
                "role": "tool",
                "content": msg.content,
                "tool_call_id": getattr(msg, "tool_call_id", None),
                "name": getattr(msg, "name", None),
            })
    request.session["chat_history"] = session_friendly
    request.session.modified = True

@csrf_exempt
def chat_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    body = json.loads(request.body)
    user_message = body.get("message", "")

    if not user_message:
        return JsonResponse({"error": "Empty message"}, status=400)

    history = get_sesion(request)

    # Ejecutar agente
    updated_history, reply = chat_with_memory(user_message, history)

    set_sesion(request, updated_history)

    return JsonResponse({"response": reply})

@csrf_exempt
def search_filter(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    history = get_sesion(request)
    body = json.loads(request.body)
    city = body.get("city", "")
    date = body.get("date", "")
    genre = body.get("genre", "")
    [year, month, day] = date.split("-")
    qs = Evento.objects.filter(ciudad__nombre=city.lower())
    qs = qs.filter(fecha=date)
    if not qs:
        return JsonResponse({"response": f"No he encontrado fiestas en {city} para esas fechas, prueba con alguna otra"})
    if genre:
        qs = qs.filter(detalle__generos__nombre=genre.upper())
        if not qs:
            return JsonResponse({"response": f"No he encontrado fiestas de {genre.lower()} el {day} en {city}"})
    eventos = [str(e) for e in qs]
    history.append(AIMessage(content="\n".join(eventos)))
    user_message = f"Repiteme las fiestas"    
    updated_history, reply = chat_with_memory(user_message, history)
    
    set_sesion(request, updated_history)
    
    return JsonResponse({"response": reply})