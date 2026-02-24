import ollama

def clean_test():
    response = ollama.chat(
        model='qwen2.5:3b',
        messages=[{'role': 'user', 'content': 'Napisz tylko jedno słowo: BANANA'}]
    )
    
    # Wyciągamy tylko tekst ze struktury, którą daje Ollama
    text_only = response['message']['content'].strip()
    
    print(f"Surowa odpowiedź: {text_only}")

clean_test()
