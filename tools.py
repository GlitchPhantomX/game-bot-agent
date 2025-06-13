from agents.tool import function_tool
import random
@function_tool("play_guess_the_number")
def play_guess_the_number(user_guess: str) -> str:
    try:
        user_number = int(user_guess)
        if not 1 <= user_number <= 10:
            return "Please guess a number between 1 and 10."

        secret_number = random.randint(1, 10)
        if user_number == secret_number:
            return f"🎉 Correct! You guessed it — the number was {secret_number}."
        else:
            return f"❌ Oops! Wrong guess. I chose {secret_number}, not {user_number}."

    except ValueError:
        return "Please enter a valid number between 1 and 10."

@function_tool("play_rock_paper_scissors")
def play_rock_paper_scissors(user_choice: str) -> str:
    choices = ["rock", "paper", "scissors"]
    user_choice = user_choice.lower()

    if user_choice not in choices:
        return "Please choose either rock, paper, or scissors."

    bot_choice = random.choice(choices)

    result = ""
    if user_choice == bot_choice:
        result = "It's a tie!"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "scissors" and bot_choice == "paper") or \
         (user_choice == "paper" and bot_choice == "rock"):
        result = "You win! 🎉"
    else:
        result = "I win! 😄"

    return f"You chose {user_choice}, I chose {bot_choice}. {result}"

@function_tool("play_quiz_game")
def play_quiz_game(answer: str = None) -> str:
    questions = [
        {
            "question": "What is the capital of France?",
            "answer": "paris"
        },
        {
            "question": "How many continents are there? (Enter a number)",
            "answer": "7"
        },
        {
            "question": "What gas do plants absorb from the atmosphere?",
            "answer": "carbon dioxide"
        }
    ]
    
    if not answer:
        return f"QUIZ TIME! First question: {questions[0]['question']}"
    
    current_q = next((q for q in questions if q['question'] in globals().get("last_quiz_question", "")), None)
    
    if current_q:
        if answer.lower() == current_q['answer']:
            globals()["quiz_score"] = globals().get("quiz_score", 0) + 1
            response = "✅ Correct! "
        else:
            response = f"❌ Wrong! The answer was {current_q['answer']}. "
        
        next_q = questions[(questions.index(current_q)+1) % len(questions)]
        globals()["last_quiz_question"] = next_q["question"]
        return response + f"Next question: {next_q['question']}"
    return "Start a new quiz by saying 'play quiz game'."

@function_tool("show_menu")
def show_menu() -> str:
    """
    Displays all games and scores with ASCII art.
    """
    menu = f"""
✨ GAME BOT MENU ✨
    
🎮 1. Guess the Number - Say "guess a number"
✊ 2. Rock Paper Scissors - Say "rock/paper/scissors"
🧠 3. Quiz Game - Say "start quiz"
🔠 4. Word Puzzle - Say "word puzzle"

📊 SCORES:
- RPS Wins: {globals().get('rps_wins', 0)}
- Quiz Correct: {globals().get('quiz_score', 0)}
- Word Puzzles Solved: {globals().get('word_puzzle_wins', 0)}

Say "menu" anytime to return here!
    """
    return menu

