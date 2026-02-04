import asyncio
import os
from dotenv import load_dotenv

# 1. Import Kernel and AI Connector
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

load_dotenv()

async def main():
    # 2. Initialize the Kernel
    kernel = Kernel()

    # 3. Register the AI Service
    # Note: Semantic Kernel v1.x separates the "Service ID" from the model ID
    service_id = "chat"
    
    # Configure OpenRouter (or OpenAI)
    chat_service = OpenAIChatCompletion(
        service_id=service_id,
        ai_model_id="meta-llama/llama-3.2-3b-instruct", 
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    # Force Base URL for OpenRouter
    chat_service.client.base_url = "https://openrouter.ai/api/v1/"
    
    # Add the service to the kernel
    kernel.add_service(chat_service)

    # 4. Create and Register the Function (The Fix)
    # OLD: kernel.create_function_from_prompt(...) -> Removed in v1.x
    # NEW: kernel.add_function(...)
    
    prompt = "Explain the difference between a 'Kernel' and a 'Chain' in 2 sentences."
    
    print("🧠 Registering Semantic Function...")
    # This automatically creates a function and adds it to the kernel's plugin system
    function = kernel.add_function(
        function_name="ExplainConcepts",
        plugin_name="LearningPlugin",
        prompt=prompt
    )

    # 5. Invoke the function
    print("🚀 Invoking...")
    # In v1.x, you invoke the function object directly using the kernel
    result = await kernel.invoke(function)
    
    print(f"\n✅ Result:\n{result}")

if __name__ == "__main__":
    asyncio.run(main())