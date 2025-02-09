from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Load a text-generation model (GPT-2)
generator = pipeline("text-generation", model="gpt2")

def generate_learning_material(topic, difficulty):
    # Modify the prompt to be more specific in asking for detailed lesson plans.
    prompt = f"Give information on improving a student's knowledge for the {topic} based on the {difficulty} level."

    response = generator(prompt, max_length=500, do_sample=True)
    generated_text = response[0]["generated_text"]

    # Clean up the text, removing extra line breaks or formatting issues
    learning_steps = generated_text.split('\n')

    # Return a list of formatted learning steps
    return [step.strip() for step in learning_steps if step.strip()]



def generate_quiz(topic, difficulty):
    # Adjust the prompt to specify the number of questions and the structure
    prompt = f"Create a {difficulty} level multiple-choice quiz for the topic {topic}. Include 3 questions with 4 answer options each. Format: 'Question: option1, option2, option3, option4'"

    response = generator(max_length=400, do_sample=True)
    generated_text = response[0]["generated_text"]

    # Format the output properly by splitting at new lines and cleaning up the text
    quiz_questions = []
    questions = generated_text.split('\n')

    for question in questions:
        parts = question.split(':')  # Split at the first occurrence of ":"
        if len(parts) > 1:
            question_text = parts[0].strip()
            options = parts[1].strip().split(',')  # Split the options by commas
            quiz_questions.append({
                "question": question_text,
                "options": [opt.strip() for opt in options]
            })

    return quiz_questions



@app.route('/quiz', methods=['POST'])
def quiz():
    topic = request.form.get('topic')
    try:
        user_score = int(request.form.get('score'))
    except ValueError:
        print("Invalid input score.")  # Debugging log
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

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    # Process the submitted answers
    quiz_answers = request.form.to_dict()
    print("Submitted answers:", quiz_answers)  # You can process the answers here

    return "Thank you for completing the quiz!"

if __name__ == '__main__':
    app.run(debug=True)

