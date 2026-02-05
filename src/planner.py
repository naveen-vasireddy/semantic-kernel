import asyncio
import os
from dotenv import load_dotenv

# 1. Standard Imports
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.contents import ChatHistory

# FIX: Import FunctionChoiceBehavior from its specific file, NOT the general 'ai' package
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior

# OpenRouter / OpenAI Connectors
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatCompletion, 
    OpenAIChatPromptExecutionSettings
)

load_dotenv()

# --- STEP 1: Define the Plugin ---
class MathPlugin:
    @kernel_function(description="Adds two numbers together")
    def add(self, number1: float, number2: float) -> float:
        print(f"   [MathPlugin] 🧮 Adding {number1} + {number2}")
        return number1 + number2

    @kernel_function(description="Subtracts the second number from the first")
    def subtract(self, number1: float, number2: float) -> float:
        print(f"   [MathPlugin] 🧮 Subtracting {number1} - {number2}")
        return number1 - number2

async def main():
    # 2. Create the kernel
    kernel = Kernel()

    # --- Configure Service ---
    service_id = "chat"
    chat_service = OpenAIChatCompletion(
        service_id=service_id,
        ai_model_id="mistralai/mistral-nemo", 
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    chat_service.client.base_url = "https://openrouter.ai/api/v1/"
    kernel.add_service(chat_service)

    # 3. Add the Plugin
    kernel.add_plugin(MathPlugin(), plugin_name="Math")

    # 4. Get the Chat Service (THE FIX)
    # Instead of importing ChatCompletionClientBase, we just ask for the service by ID.
    chat_completion = kernel.get_service(service_id="chat")

    # 5. Enable automatic function calling
    # This creates the "Planner" behavior without a Planner object
    settings = OpenAIChatPromptExecutionSettings(service_id=service_id)
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # 6. Conversation Loop
    history = ChatHistory()
    print("🤖 Enterprise Agent Ready. Type 'exit' to quit.")
    
    # Pre-seed with a math question to test immediately
    print("   (Try: 'I have $50 and spent $12. How much is left?')")

    while True:
        try:
            userInput = input("\nUser > ")
        except EOFError:
            break

        if userInput.lower() == "exit":
            break

        history.add_user_message(userInput)

        # 7. Get response
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            settings=settings,
            kernel=kernel,
        )

        print("Assistant > " + str(result))
        history.add_message(result)

if __name__ == "__main__":
    asyncio.run(main())