import asyncio
import os
from dotenv import load_dotenv
from typing import Annotated

# 1. Import Kernel and Decorators
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

load_dotenv()

# --- STEP 1: Define the Plugin (The "C# Style" Class) ---
class MathPlugin:
    """
    A collection of math functions that the Kernel can use.
    In SK, we group related functions into a Class (Plugin).
    """
    
    @kernel_function(description="Adds two numbers together")
    def add(
        self, 
        number1: Annotated[float, "The first number"], 
        number2: Annotated[float, "The second number"]
    ) -> float:
        print(f"   [MathPlugin] 🧮 Native Code Running: {number1} + {number2}")
        return number1 + number2

    @kernel_function(description="Subtracts the second number from the first")
    def subtract(
        self, 
        number1: Annotated[float, "The first number"], 
        number2: Annotated[float, "The second number"]
    ) -> float:
        print(f"   [MathPlugin] 🧮 Native Code Running: {number1} - {number2}")
        return number1 - number2

async def main():
    # --- STEP 2: Initialize Kernel ---
    kernel = Kernel()

    # Setup OpenRouter (Same as Day 49)
    service_id = "chat"
    chat_service = OpenAIChatCompletion(
        service_id=service_id,
        ai_model_id="meta-llama/llama-3.2-3b-instruct", 
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    chat_service.client.base_url = "https://openrouter.ai/api/v1/"
    kernel.add_service(chat_service)

    # --- STEP 3: Import the Plugin ---
    # This acts like "Dependency Injection". We inject the class into the kernel.
    # The Kernel now "knows" how to do Math.
    print("🔌 Registering MathPlugin...")
    kernel.add_plugin(MathPlugin(), plugin_name="Math")

    # --- STEP 4: Invoke the Plugin Manually ---
    # We ask the kernel to find the 'Math' plugin and run the 'add' function.
    print("\n1️⃣  Direct Execution (Manual):")
    
    # Note: In SK v1.x, we invoke by getting the function from the kernel's collection
    add_func = kernel.get_function(plugin_name="Math", function_name="add")
    
    # Run 50 + 20
    result = await kernel.invoke(add_func, number1=50, number2=20)
    print(f"   ✅ Result: {result}")

    # --- STEP 5: Invoke via Semantic Prompt (The "Magic") ---
    print("\n2️⃣  Semantic Execution (LLM calling Code):")
    
    # FIX: Surround the numbers 100 and 35 with single quotes ('100', '35')
    prompt = """
    I have $100 and I spent $35. 
    Calculate the remaining amount using the Math plugin.
    
    Result: {{Math.subtract number1='100' number2='35'}}
    """
    
    # Register this prompt as a function on the fly
    semantic_func = kernel.add_function(
        prompt=prompt, 
        function_name="CalculateBudget", 
        plugin_name="FinancialApp"
    )
    # Run the prompt
    final_answer = await kernel.invoke(semantic_func)
    print(f"   ✅ LLM Output: {final_answer}")

if __name__ == "__main__":
    asyncio.run(main())