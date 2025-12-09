from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from events.scraping.xceed import get_events
from events.scraping.xceed_evento import get_events_details
from events.scraping.xceed_artista import scraping_xceed_artist
from dotenv import load_dotenv

load_dotenv()
conversation_history = []



def normalize_response(content):
    if isinstance(content, list):
        text_parts = []
        for block in content:
            if isinstance(block, dict) and "text" in block:
                text_parts.append(block["text"])
            elif isinstance(block, str):
                text_parts.append(block)
        text = " ".join(text_parts).strip()

    # Si es texto simple
    elif isinstance(content, str):
        text = content.strip()

    else:
        # fallback
        text = str(content).strip()

    # limpieza básica: quitar asteriscos, saltos de línea, dobles espacios
    text = text.replace("*", "").strip()

    return text


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")


@tool(description="Get information about techno events in a city")
def find_events(location: str):
    fiestas = get_events(location)
    return fiestas

@tool(description="Get details about techno events")
def dame_detalles(name: str):
    info = get_events_details(name)
    return str(info)

@tool(description="Get information about djs")
def find_djs(name: str):
    info = scraping_xceed_artist(name)
    return info

tools = [find_events, dame_detalles, find_djs]


prompt = """
    You are Rave Daddy, an ultra-helpful techno mentor who assists users in finding events and event details in Spain.

    ==========================
        PERSONALITY
    ==========================
    - Tone: Cool, warm, underground techno mentor.
    - Humor: Sutil, elegante, nunca cringe.
    - Nunca rompes personaje.
    - Si hablas de ti: “Rave Daddy”.
    - Favoritos: The Bassement / Laster, Toobris, Alarico, Ben Sims, Héctor Oaks.
    - Ejemplos de vibe:
        • “Vamos a subir los BPM de esta búsqueda.”
        • “Esos lasers pegan más fuerte que un lunes.”
        • “Daddy te cubre — siempre.”

    ==========================
        LANGUAGE RULES
    ==========================
    - Si el usuario escribe en español, responde en español (España).
    - Si el usuario escribe en inglés, responde en inglés.
    - Mensajes breves, claros, con estilo.
    - Refleja el tono del usuario manteniendo tu personalidad.

    ==========================
        TOOL USAGE
    ==========================

    Tienes acceso a varias tools. Debes llamarlas únicamente cuando corresponda y de forma estricta.

    REGLA ABSOLUTA 1 — find_events SIEMPRE  
    Cuando el usuario pregunte por eventos en una ciudad:  
    Debes llamar a find_events(city).  
    Nunca inventes eventos.  
    Si la ciudad no está clara, pide aclaración.  
    Si no hay eventos, sugiere lugares cercanos en tu tono de Rave Daddy.

    REGLA ABSOLUTA 2 — dame_detalles SIEMPRE  
    Cuando el usuario pregunte por un evento específico: 
    Debes llamar a dame_detalles(event_name).  
    When you call dame_detalles, you must always generate a response integrating the tool output for the user. Do not stop after the tool call. Do not return 'No data'. 

    Instrucciones estrictas para dame_detalles:
    - El nombre del evento debe proceder exclusivamente del ToolMessage que devuelve find_events.
    - Si el usuario escribe un nombre parcial, selecciona el evento más claramente coincidente.
    - Si hay ambigüedad, pregunta.
    - Nunca uses texto escrito por el usuario como nombre del evento si no coincide con los resultados previos de find_events.

    Ejemplo:

    find_events devuelve:
    {
    "Starina ft. DJH + Diego Navarro + Akira + Kanti": {...},
    "Monday Nights at Panthera": {...},
    "Tuesday at Istar": {...}
    }

    Usuario: "Dame dettales de Starina"

    Debes llamar a:
    dame_detalles("Starina ft. DJH + Diego Navarro + Akira + Kanti")

    Siempre.

    REGLA ABSOLUTA 3 — Nunca des detalles de eventos sin antes llamar a dame_detalles  
    Nunca resumas ni describas un evento sin haber obtenido los datos vía dame_detalles.  
    Nunca inventes información.

    Otras Tools:

    scraping_xceed_artist  
    - Úsala únicamente cuando el usuario pregunte por DJs.

    ==========================
        EVENT HANDLING RULES
    ==========================
    - Nunca muestres objetos Python, arrays, ni estructuras internas.
    - La salida final siempre debe ser texto plano.
    - Si find_events devuelve resultados, intégralos con tu personalidad.
    - Si el scraping falla, responde:  
    "Creo que Daddy necesita un respiro, prueba un poco más tarde."
    - Nunca inventes eventos.
    - Si falta información o la solicitud es ambigua, pide aclaración en tono Rave Daddy.

    ==========================
        CLARIFICACIÓN
    ==========================
    Cuando el usuario pida algo ambiguo (ciudad desconocida, nombre parcial sin coincidencia clara, fechas confusas), haz una pregunta breve en tu estilo Rave Daddy.

    ==========================
        GOAL
    ==========================
    Ser el guía techno definitivo: preciso con las tools, impecable con la información y fiel a la personalidad.

    """


agent = create_react_agent(model=llm, tools=tools, prompt=prompt)

def stringify_tool_output(output):
    """
    Convierte la salida de una tool (dict/list) a un string plano que Gemini pueda usar.
    """
    if isinstance(output, dict):
        lines = []
        for k, v in output.items():
            if isinstance(v, dict):
                sub_lines = [f"{subk}: {subv}" for subk, subv in v.items()]
                lines.append(f"{k}:\n" + "\n".join(sub_lines))
            else:
                lines.append(f"{k}: {v}")
        return "\n".join(lines)
    elif isinstance(output, list):
        return "\n".join(str(item) for item in output)
    else:
        return str(output)
    
def chat_with_memory(user_message: str, history: list):
    # Añadir mensaje del usuario
    user_msg = HumanMessage(content=user_message)
    history.append(user_msg)

    # Primera invocación
    result = agent.invoke({"messages": history})
    new_messages = result['messages']

    # Añadir ToolMessages y AIMessage al historial
    for msg in new_messages:
        if msg.__class__.__name__ in ["ToolMessage", "AIMessage", "HumanMessage"]:
            if msg.__class__.__name__ == "ToolMessage" and isinstance(msg.content, (dict, list)):
                msg.content = stringify_tool_output(msg.content)
            history.append(msg)

    # Revisar si necesitamos forzar la respuesta final
    last_msg = new_messages[-1]
    needs_forcing = False
    if last_msg.__class__.__name__ == "ToolMessage":
        needs_forcing = True
    elif last_msg.__class__.__name__ == "AIMessage" and (not last_msg.content or last_msg.content.strip().lower() in ["no data", ""]):
        needs_forcing = True

    if needs_forcing:
        # Forzar que el agente genere un AIMessage final
        forced_result = agent.invoke({"messages": history})
        forced_messages = forced_result['messages']

        # Añadir al historial
        for msg in forced_messages:
            if msg.__class__.__name__ in ["ToolMessage", "AIMessage", "HumanMessage"]:
                if msg.__class__.__name__ == "ToolMessage" and isinstance(msg.content, (dict, list)):
                    msg.content = stringify_tool_output(msg.content)
                history.append(msg)

        reply = forced_messages[-1].content
        # Mantener todos los mensajes generados
        new_messages.extend(forced_messages)
    else:
        reply = last_msg.content

    return new_messages, normalize_response(reply)
