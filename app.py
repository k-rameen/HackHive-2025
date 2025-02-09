# from flask import Flask, render_template, request
# import openai
# import os
# from transformers import pipeline
# from huggingface_hub import login

# login(token="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")


# app = Flask(__name__)

# # Set up OpenAI API key (ensure to set your API key as an environment variable)
# # openai.api_key = "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"


# # Load a text-generation model
# generator = pipeline("text-generation", model="meta-llama/Llama-2-7b-chat-hf")

# def generate_learning_material(topic, difficulty):
#     prompt = f"Generate a {difficulty} level learning path for {topic}. Provide 3-5 learning activities."
#     response = generator(prompt, max_length=200, do_sample=True)
#     return response[0]["generated_text"]

# # Example usage
# print(generate_learning_material("Python Programming", "beginner"))

# def generate_learning_material(topic, difficulty):
#     """Generate personalized learning materials using AI."""
#     prompt = f"Generate a {difficulty} level learning path for {topic}. Provide 3-5 learning activities."  
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "system", "content": "You are an expert educator."},
#                   {"role": "user", "content": prompt}]
#     )
#     return response['choices'][0]['message']['content'].split('\n')

# # def generate_quiz(topic, difficulty):
# #     """Generate quiz questions and options using AI."""
# #     prompt = f"Create a {difficulty} level multiple-choice quiz for {topic} with 3 questions, each having 4 options."  
# #     response = openai.ChatCompletion.create(
# #         model="gpt-3.5-turbo",
# #         messages=[{"role": "system", "content": "You are an AI that generates educational quizzes."},
# #                   {"role": "user", "content": prompt}]
# #     )
# #     return response['choices'][0]['message']['content']

# def generate_quiz(topic, difficulty):
#     prompt = f"Create a {difficulty} level multiple-choice quiz for {topic} with 3 questions, each having 4 options."
#     response = generator(prompt, max_length=300, do_sample=True)
#     return response[0]["generated_text"]

# # Example usage
# print(generate_quiz("Space Science", "medium"))


# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/quiz', methods=['POST'])
# def quiz():
#     topic = request.form.get('topic')
#     try:
#         user_score = int(request.form.get('score'))
#     except ValueError:
#         return "Invalid input. Please enter a valid score between 0 and 10."

#     # Determine difficulty level based on score
#     if user_score < 5:
#         difficulty = 'easy'
#     elif 5 <= user_score < 8:
#         difficulty = 'medium'
#     else:
#         difficulty = 'hard'

#     # Generate learning materials and quiz using AI
#     recommendations = generate_learning_material(topic, difficulty)
#     quiz_questions = generate_quiz(topic, difficulty)

#     return render_template('quiz.html', difficulty=difficulty, recommendations=recommendations, quiz_questions=quiz_questions)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load a text-generation model (GPT-2)
generator = pipeline("text-generation", model="gpt2")

def generate_learning_material(topic, difficulty):
    prompt = f"Generate a {difficulty} level learning path for {topic}. Provide 3-5 learning activities."
    response = generator(prompt, max_length=200, do_sample=True)
    return response[0]["generated_text"]

def generate_quiz(topic, difficulty):
    prompt = f"Create a {difficulty} level multiple-choice quiz for {topic} with 3 questions, each having 4 options."
    response = generator(prompt, max_length=300, do_sample=True)
    return response[0]["generated_text"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz', methods=['POST'])
def quiz():
    topic = request.form.get('topic')
    try:
        user_score = int(request.form.get('score'))
    except ValueError:
        return "Invalid input. Please enter a valid score between 0 and 10."

    # Determine difficulty level based on score
    if user_score < 5:
        difficulty = 'easy'
    elif 5 <= user_score < 8:
        difficulty = 'medium'
    else:
        difficulty = 'hard'

    # Generate learning materials and quiz using AI
    recommendations = generate_learning_material(topic, difficulty)
    quiz_questions = generate_quiz(topic, difficulty)

    return render_template('quiz.html', difficulty=difficulty, recommendations=recommendations, quiz_questions=quiz_questions)

if __name__ == '__main__':
    app.run(debug=True)
