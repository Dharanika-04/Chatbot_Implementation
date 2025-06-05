import sys
import time
import threading
from openai import OpenAI

API_KEY = ""
MODEL = "deepseek/deepseek-r1-0528:free"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

def spinner():
    while not done:
        for cursor in '|/-\\':
            sys.stdout.write(f'\rLoading... {cursor}')
            sys.stdout.flush()
            time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 15 + '\r')

def chat_with_model(prompt):
    global done
    done = False
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are StudyPal, a helpful study assistant."},
                {"role": "user", "content": prompt},
            ],
            extra_headers={
                "HTTP-Referer": "https://localhost",
                "X-Title": "StudyPal",
            }
        )
        done = True
        spinner_thread.join()
        return response.choices[0].message.content.strip()

    except Exception as e:
        done = True
        spinner_thread.join()
        return f"Error: {e}"

def main():
    print("Welcome to StudyPal Chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break
        answer = chat_with_model(user_input)
        print(f"StudyPal: {answer}")

if __name__ == "__main__":
    main()
