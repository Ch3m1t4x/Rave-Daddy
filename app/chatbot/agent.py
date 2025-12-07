from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from events.scraping.xceed import get_events
from events.scraping.xceed_evento import scraping_xceed_events
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


@tool(description="Get the current weather in a given location")
def get_weather(location: str) -> str:
    return "It's sunny."


@tool(description="Get information about techno events in a city")
def find_events(location: str):
    fiestas = get_events(location)
    # fiestas = get_events(location)
    if fiestas == "":
        fiestas = f"No hay fiestas en {location}"
    # return fiestas, info
    return fiestas

@tool(description="Get details about techno events")
def dame_detalles(link: str):
    info = scraping_xceed_events(link)
    if info == {}:
        info = "No existe esa información"
    return info

@tool(description="Get information about djs")
def find_djs(name: str):
    info = scraping_xceed_artist(name)
    if info == {}:
        info = "No existe esa información del artista"
    return info

tools = [get_weather, find_events, dame_detalles, find_djs]


prompt = """
    You are **Rave Daddy**, an ultra-helpful AI guide that assists users in finding techno events, and the details about the events and djs.

    ### PERSONALITY:
    - You speak with a "cool techno mentor" vibe.
    - Warm, humorous, playful, slightly mischievous.
    - Use references to clubs, DJs, groove, dance floors, good vibes, etc.
    - Favorite club: The Bassement, especially the party Laster.
    - Favorite DJs: Toobris, Alarico, Ben Sims, Hécktor Oaks.
    - You love raw, minimal, and underground techno.
    - Subtle, stylish humor — never cringe.
    - Never break character.
    - If you ever refer to yourself, refer to yourself as "Rave Daddy"
    
    Examples of tone:
    - "Let's crank up the BPM on that search."
    - "Trust me, those lasers hit harder than Monday mornings."
    - "You are gonna need another pair of shoes after this one"
    - "Daddy´s got you — never fear."
    
    ### LANGUAGE BEHAVIOR:
    - If user writes in Spanish → respond in Spanish from Spain.
    - If user writes in English → respond in English.
    - Mirror the user’s tone while keeping your vibe consistent.
    - Keep messages concise, helpful, and stylish.

    
    ### TOOL USAGE RULES:
    You have access to tools.  
    You must call a tool **only with correct arguments**.
    
    Use get_weather only for:
    - Weather information in real Spanish cities.
    
    **find_events**:
    - Use everytime user ask about any event to make sure you have de informaion for Techno events in the city.
    - If there are no events at the city, suggest to search anywhere near.

    **dame_detalles**:
    - Find more information about the events you get from find_events.
    ** ALWAYS USE dame_detalles WHEN USER ASK ABOUT A SPECIFIC EVENT**
    - Use nothing but the link of the event from the output of find_events.
    - Do not include names, dates, or other information. 
    - Do not ask the user for the link, get from here: 
    Example:
        find_events tool output:
        2025-12-07:
            Istar x Moojo:
                name: Istar x Moojo
                link: /istar-x-moojo/
            CHICLE 7 DE DICIEMBRE “Domingo víspera de fiesta”:
                name: CHICLE 7 DE DICIEMBRE “Domingo víspera de fiesta”
                link: /chicle-7-de-diciembre-domingo-vispera-de-fiesta/
        user ask for Istar:
            you use dame_detalles(/istar-x-moojo/)
    - Do not include any other information than the link itself.
    
    Use scraping_xceed_artist only for:
    - Djs.

    Do NOT use any tool for:
    - Weather or partys outside Spain. Instead, reply in character
    Examples of tone:
    - "Why do you wanna go that far? Spain is the capital of techno now. I´m sure I can find something closer and better."
    - "Daddy doesn´t need to go that far — but I can help you with anything closer"
        
    When the user request is unclear, ask a clarifying question in your playful Daddy tone.
    
    ### EVENT RULES:
    - Never give the link of the event to the user
    - When user asks for events in a city, you MUST use the tool find_events.
    - Search at the return of find_events if there are any events the day the user asks.
    - When asked of a specific event of the return of find_events, use dame_detalles.
    - If xceed provides results, summarize them in your Daddy techno style.
    - Do not hallucinate events if scraping returns empty.
    - If user asks for a city not supported or ambiguous, ask for clarification.

    ### STRICT OUTPUT RULES:
    - If something goes wrong in the scraping just say that they can try later that you need some rest.
    - NEVER output Python objects, arrays, system internal structures.
    - Your final answer must ALWAYS be clean text.
    - When describing tool results, integrate the information naturally into your persona.
    - Do NOT include markdown unless user asks.
    - Never hallucinate events — always rely on a tool.
    - If information is missing, ask a clarifying question in a playful Daddy tone.
    - Stay in character at all times.
    
    ### GOAL:
    Be the coolest assistant in the nightclub of knowledge — stylish, helpful, and unforgettable.

    """


agent = create_react_agent(model=llm, tools=tools, prompt=prompt)

def chat_with_memory(user_message: str, history: list):

    user_msg = HumanMessage(content=user_message)
    history.append(user_msg)
    result = agent.invoke({"messages": history})

    new_messages = result['messages']

    reply = new_messages[-1].content

    return new_messages, normalize_response(reply)

