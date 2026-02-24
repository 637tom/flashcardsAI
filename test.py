import ollama

# 1. Wysyłamy pytanie do DeepSeeka
print("Czekaj, DeepSeek myśli...")
response = ollama.chat(
    model='deepseek-r1:1.5b',
    messages=[{'role': 'user', 'content': 'Napisz w jednym zdaniu co to jest ATP'}]
)

# 2. Wyciągamy surową odpowiedź (z blokiem <think>)
full_content = response['message']['content']

print("-" * 30)
print("PEŁNA ODPOWIEDŹ:")
print(full_content)
print("-" * 30)
