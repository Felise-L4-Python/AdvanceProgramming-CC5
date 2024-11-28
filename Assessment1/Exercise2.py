import random

def load_jokes(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        return [line.strip().split('?') for line in file if '?' in line]

def tell_joke(jokes):
    setup, punchline = random.choice(jokes)
    print(f"Alexa: {setup}?")
    input("Press Enter to hear the punchline... (Don't worry, I won't make you wait too long!)")
    print(f"Alexa: {punchline} (Ha! Get it?)")

def main():
    jokes = load_jokes('resources/randomJokes.txt')
    
    print("Alexa: Ready to tickle your funny bone! Just say 'Alexa tell me a joke'!")
    
    while True:
        user_input = input("You: ").lower().strip()
        
        if user_input == "alexa tell me a joke":
            tell_joke(jokes)
        elif user_input in ["quit", "exit", "bye"]:
            print("Alexa: Goodbye! Remember, laughter is the best medicine... unless you have a broken rib!")
            break
        else:
            print("Alexa: I'm sorry, I didn't understand that. Try saying 'Alexa tell me a joke'! I promise it'll be worth it!")

if __name__ == "__main__":
    main()