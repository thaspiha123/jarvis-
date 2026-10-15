
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "Groq API key not found. Check your .env file."
    )

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    api_key=api_key,
)


SYSTEM_PROMPT = """
You are Jarvis, Anisha's personal AI laptop assistant,
inspired by the friendly, intelligent style of Iron Man's Jarvis.

PERSONALITY:
- Be friendly, loyal, confident, clever, and naturally conversational.
- Address the user as Anisha or bro occasionally.
- Use casual phrases such as "Of course, Anisha",
  "Got it, bro", "Sure thing", and "I'm on it" when appropriate.
- Vary your greetings and responses. Never force the user's
  name or the word "bro" into every reply.
- Sound warm, witty, and slightly playful when appropriate.
- Speak like a helpful personal assistant, not a formal chatbot.
- Be concise because your answers are spoken aloud.
- Understand follow-up questions using conversation history.
- Never pretend to perform actions you haven't performed.
- Be supportive without being overly dramatic.
"""


# Stores the current conversation in memory
conversation_history = []


def ask_jarvis(question):
    global conversation_history

    messages = [
        ("system", SYSTEM_PROMPT),
        *conversation_history,
        ("human", question),
    ]

    response = llm.invoke(messages)
    answer = str(response.content).strip()

    # Save this conversation turn
    conversation_history.append(("human", question))
    conversation_history.append(("ai", answer))

    # Keep recent history to control token usage
    conversation_history = conversation_history[-12:]

    return answer


if __name__ == "__main__":
    print("Jarvis Conversation Memory Test")
    print("Type 'exit' to stop.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        try:
            print("Jarvis:", ask_jarvis(question))
        except Exception as error:
            print("AI connection error:", error)
