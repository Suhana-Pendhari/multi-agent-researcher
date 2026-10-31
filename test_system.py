"""Test script to verify the Research Mind system works"""
from dotenv import load_dotenv
import os

load_dotenv()

print("="*50)
print("Testing Research Mind System")
print("="*50)

# Check API keys
print("\n1. Checking API Keys...")
print(f"   GROQ_API_KEY: {'[OK] Set' if os.getenv('GROQ_API_KEY') else '[ERROR] Not set'}")
print(f"   GOOGLE_API_KEY: {'[OK] Set' if os.getenv('GOOGLE_API_KEY') else '[ERROR] Not set'}")
print(f"   TAVILY_API_KEY: {'[OK] Set' if os.getenv('TAVILY_API_KEY') else '[ERROR] Not set'}")

# Test imports
print("\n2. Testing imports...")
try:
    from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain, llm
    print(f"   [OK] All imports successful")
    try:
        print(f"   [OK] Model: {llm.model}")
    except:
        print(f"   [OK] Model: {type(llm).__name__}")
except Exception as e:
    print(f"   [ERROR] Import failed: {e}")
    exit(1)

# Test agent creation
print("\n3. Testing agent creation...")
try:
    search_agent = build_search_agent()
    reader_agent = build_reader_agent()
    print(f"   [OK] Search agent created")
    print(f"   [OK] Reader agent created")
except Exception as e:
    print(f"   [ERROR] Agent creation failed: {e}")
    exit(1)

# Test simple LLM call
print("\n4. Testing LLM call...")
try:
    from langchain_core.messages import HumanMessage
    response = llm.invoke([HumanMessage(content="Say 'Hello' in one word.")])
    print(f"   [OK] LLM response: {response.content}")
except Exception as e:
    print(f"   [ERROR] LLM call failed: {e}")
    exit(1)

print("\n" + "="*50)
print("[SUCCESS] All tests passed! System is ready.")
print("="*50)
