#!/usr/bin/env python3
import requests

KEY = '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'

# Get key info
print("Checking key validity...")
response = requests.get(
    'https://openrouter.ai/api/v1/auth/key',
    headers={'Authorization': f'Bearer {KEY}'}
)

print(f'Auth check status: {response.status_code}')
if response.status_code == 200:
    print(f'Response: {response.json()}')
else:
    print(f'Error: {response.text}')

# Try free model with all required headers
print("\nTrying free Llama model...")
headers = {
    'Authorization': f'Bearer {KEY}',
    'Content-Type': 'application/json',
    'HTTP-Referer': 'https://bobs-brain.com',
    'X-Title': 'BobsBrain'
}

data = {
    'model': 'meta-llama/llama-3.1-8b-instruct:free',
    'messages': [{'role': 'user', 'content': 'Say hello'}],
    'max_tokens': 10
}

resp = requests.post(
    'https://openrouter.ai/api/v1/chat/completions',
    headers=headers,
    json=data
)

print(f'Chat completion status: {resp.status_code}')
if resp.status_code == 200:
    print(f'Success! Response: {resp.json()["choices"][0]["message"]["content"]}')
else:
    print(f'Error: {resp.text}')
    
print("\n" + "="*50)
print("CONCLUSION:")
if resp.status_code == 200:
    print("✅ OpenRouter key works with free models!")
    print("We can proceed with Graphiti setup using OpenRouter")
else:
    print("❌ Key can list models but can't chat")
    print("Might need account setup or credits")