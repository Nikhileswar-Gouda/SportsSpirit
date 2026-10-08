import requests
import os

model = os.getenv("QWEN_MODEL", "qwen2.5:7b")

ollama_url = os.getenv("QWEN_BASE_URL", "http://localhost:11434/api/generate")
payload = {
    "model": model,
    "prompt": "Hello from test",
    "stream": False,
    "options": {"temperature": 0.7, "num_predict": 50}
}

print("Testing", ollama_url)
try:
    r = requests.post(ollama_url, json=payload, timeout=15)
    print("Status:", r.status_code)
    print(r.text[:2000])
except Exception as e:
    print("Error for /api/generate:", e)

base_url = os.getenv("QWEN_OPENAI_BASE_URL", "http://localhost:11434/v1")
openai_payload = {
    "model": model,
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello from test"}
    ],
    "temperature": 0.7,
    "max_tokens": 200
}

print("\nTesting", base_url + "/chat/completions")
try:
    r = requests.post(f"{base_url}/chat/completions", json=openai_payload, timeout=15, headers={"Content-Type": "application/json"})
    print("Status:", r.status_code)
    print(r.text[:2000])
except Exception as e:
    print("Error for /v1/chat/completions:", e)
