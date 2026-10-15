
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
You are Jarvis, a helpful laptop voice assistant.
Answer naturally, clearly, and concisely.
Keep spoken responses short unless asked for detail.
Never claim to perform computer actions you have not performed.
"""


def ask_jarvis(question):
    response = llm.invoke([
        ("system", SYSTEM_PROMPT),
        ("human", question),
    ])
    return str(response.content).strip()


if __name__ == "__main__":
    print("Jarvis AI Brain Test")
    question = input("You: ")

    try:
        answer = ask_jarvis(question)
        print("Jarvis:", answer)
    except Exception as error:
        print("AI connection error:", error)
