import asyncio
from browser_use import Agent
from langchain_ollama import ChatOllama

class OllamaProviderWrapper(ChatOllama):
    @property
    def provider(self) -> str:
        return "ollama"

async def main():
    print("Initializing local Ollama model...")
    llm = OllamaProviderWrapper(
        model="qwen2.5:7b-instruct",
        num_ctx=32000,
        temperature=0.0 # Zero temperature for strict, deterministic output
    )
    
    print("Starting Browser-Use Agent with a simplified task...")
    agent = Agent(
        # Keep the instruction ultra-clear and direct
        task="Go to https://news.ycombinator.com/ and take a screenshot or read the first headline.",
        llm=llm,
    )
    
    result = await agent.run()
    print("\n--- Automation Result ---")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())