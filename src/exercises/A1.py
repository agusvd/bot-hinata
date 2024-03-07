import random

exercises = [
    {
        "id": 1,
        "question": "What does 'hello' mean in Spanish?",
        "options": ["A) Hola", "B) Adiós", "C) Gracias"],
        "correct_answer": 0,
    },
    {
        "id": 2,
        "question": "Choose the correct translation: 'gato'",
        "options": ["A) Dog", "B) Cat", "C) Horse"],
        "correct_answer": 1,
    },
]

def generate_exercise():
    # Elegir un ejercicio aleatorio del nivel
    exercise = random.choice(exercises)
    return exercise