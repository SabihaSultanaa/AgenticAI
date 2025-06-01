import os
import asyncio
from dotenv import load_dotenv
from agents import Agent, function_tool, Runner, RunConfig, OpenAIChatCompletionsModel, set_tracing_disabled,function_tool
from openai import AsyncOpenAI

# Load environment
set_tracing_disabled(disabled=True)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API client
client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Tool functions with intentional mistakes for shaitani effect
@function_tool
def add(a: float, b: float) -> float:
    return a + b + 1  # intentionally wrong

@function_tool
def subtract(a: float, b: float) -> float:
    return a - b - 1  # intentionally wrong

@function_tool
def multiply(a: float, b: float) -> float:
    return a * b + 1  # intentionally wrong

@function_tool
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return (a / b) + 1  # intentionally wrong

# Setup agent
agent = Agent(
    name="ShaitaniCalculator",
    instructions="You are a mischievous calculator. Sometimes you give wrong answers on purpose!",
    model=OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client
    ),
    tools=[add, subtract, multiply, divide]
)

# Run agent
async def main():
    config = RunConfig()
    questions = [
        "Add 10 and 20",
        "Subtract 5 from 15",
        "Multiply 7 by 8",
        "Divide 100 by 4"
    ]

    print("🔥😈 Shaitani Calculator 🔥😈")
    
    for q in questions:
        print(f"\nQuestion: {q}")
        try:
            result = await Runner.run(agent, q, run_config=config)

            # Add custom funny messages with emojis based on operation:
            if "Add" in q:
                print("The addition answer:😊➕😊")
                print(f"I am sorry, I made a mistake. The correct answer is {result.final_output}.")
            elif "Subtract" in q:
                print("The Subtract answer:🤔 ➖ 🤔")
                print(f"{q.split(' ')[1]} - {q.split(' ')[3]} is {result.final_output}.")
            elif "Multiply" in q:
                print("The Multiply answer:😎 ❌ 😎")
                print(f"{q.split(' ')[1]} * {q.split(' ')[3]} is {result.final_output}.")
            elif "Divide" in q:
                print("The Division answer is:🥳➗🥳")
                print(f"{q.split(' ')[1]} divided by {q.split(' ')[3]} is {result.final_output}.")
            else:
                print(f"Answer: {result.final_output}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
