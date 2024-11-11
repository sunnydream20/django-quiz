import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, UserQuiz, UserAnswer, UserPackage, Package, Module
from django.contrib.auth.views import LoginView

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


from django.shortcuts import redirect
from .forms import RegistrationForm


from django.http import HttpResponse


from .forms import PurchaseForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def results_view(request):
    username = request.user.username  # Assuming the user is logged in

    user_data = {
        'username': username,
        'quiz_title1': "QCM1-Microbio",
        'quiz_title2': "QCM2-Microbio",
        'results': []  # Initialize results list
    }

    try:
        # Load the quiz data from the JSON file
        with open('mock.json', 'r') as f:
            quiz_data = json.load(f)
            # Extract the QUESTION_MAP, ANSWER_MAP, and CORRECT_ANSWERS from the loaded JSON
            QUESTION_MAP = quiz_data["questions"]
            ANSWER_MAP = quiz_data["answers"]
            CORRECT_ANSWERS = quiz_data["correct_answers"]

        with open('file.json', 'r') as f:
            data = json.load(f)
            # Get all entries for the user
            user_entries = [entry for entry in data if entry["user_id"] == username]

            if user_entries:
                # Iterate over all entries for the user
                for entry in user_entries:
                    question_id = entry["question_id"]  # Get the question ID
                    user_answer_id = int(entry["answer"])  # Convert answer to int

                    # Prepare the result object for each entry
                    if str(question_id) in QUESTION_MAP:  # Use str to match keys from JSON                  
                        correct_answer_id = CORRECT_ANSWERS[str(question_id)]  # This gives the correct answer index
                        correct_answer_text = ANSWER_MAP[str(question_id)].get(str(correct_answer_id), "Unknown Answer")

                        result = {
                            'question_id': question_id,
                            'question': QUESTION_MAP[str(question_id)],
                            'user_answer': ANSWER_MAP[str(question_id)].get(str(user_answer_id), "Unknown Answer"),
                            'correct_answer': correct_answer_text,
                            'submitted_at': entry["submitted_at"]  # Add submission time
                        }
                        user_data['results'].append(result)
    except FileNotFoundError:
        print("File not found. Please ensure file.json exists.")
        return render(request, 'quizzes/result.html', {'error': 'File not found'})
    except json.JSONDecodeError:
        print("Error decoding JSON. Please check the contents of file.json.")
        return render(request, 'quizzes/result.html', {'error': 'Error decoding JSON'})

    # Render the result in the template, passing the user_data
    return render(request, 'quizzes/result.html', user_data)

def quiz_detail_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    # return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz, 'form': form})
    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz})



@login_required
def buyPackages(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if request.method == 'POST':
        file = request.FILES.get('file')
        if file:
            # Process the file upload here, e.g., saving it to a model field
            user_package, created = UserPackage.objects.get_or_create(user=request.user, package=package)
            if created:
                user_package.purchase_image = file  # Save the file to the purchase_image field
                user_package.save()
                # Add a success message if needed
            # Redirect to the packages listing page
            return redirect('packages')
        else:
            # Optionally add a message to inform the user that the file is required
            return render(request, 'quizzes/buyPackages.html', {'package': package, 'error': 'File is required.'})
    else:
        return render(request, 'quizzes/buyPackages.html', {'package': package})


@login_required
def modules_view(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    modules = Module.objects.filter(package=package)
    return render(request, 'quizzes/modules.html', {'modules': modules, 'package': package})

@login_required
def quizzes_view(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    quizzes = Quiz.objects.filter(module=module)  # Assuming a ForeignKey from Quiz to Module
    return render(request, 'quizzes/quizzes.html', {'quizzes': quizzes, 'module': module})

def questions_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    questions = Question.objects.filter(quiz=quiz)  # Assuming a ForeignKey from Quiz to Module
    return render(request, 'quizzes/questions.html', {'questions': questions, 'quiz': quiz})

def packages_view(request):
    packages = Package.objects.all()

    if request.user.is_authenticated:
        owned_packages_ids = UserPackage.objects.filter(user=request.user).values_list('package_id', flat=True)
        for package in packages:
            package.owned = package.id in owned_packages_ids
    else:
        for package in packages:
            package.owned = False

    return render(request, 'quizzes/packages.html', {
        'packages': packages
    })
    
#    packages = [
#        {'year': 'Year 1', 'price': 1000, 'owned': False, 'id': 1},
#        {'year': 'Year 2', 'price': 1200, 'owned': True, 'id': 2},
#        {'year': 'Year 3', 'price': 1300, 'owned': False, 'id': 3},
#        {'year': 'Year 4', 'price': 1400, 'owned': True, 'id': 4},
#        {'year': 'Year 5', 'price': 1500, 'owned': True, 'id': 5},
#        {'year': 'Year 6', 'price': 1600, 'owned': False, 'id': 6},
#        {'year': 'Specialty', 'price': 2000, 'owned': False, 'id': 7},
#    ]
    
    #return render(request, 'quizzes/packages.html', {'packages': packages})


def packages(request):
    return render(request, 'quizzes/packages.html')

def contact(request):
    return render(request, 'quizzes/contact.html')


def home(request):
    return render(request, 'quizzes/home.html')

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Use the related name here

    if request.method == 'POST':
        score = 0
        for question in questions:
            user_answer = request.POST.get(f'question_{question.id}')  # Get the user's answer
            if user_answer and user_answer == str(question.correct_answer):  # Assuming correct_answer is stored as an integer
                score += 1  # Increment score for each correct answer

        # Store the user's quiz result if needed
        UserQuiz.objects.create(quiz=quiz, score=score, user=request.user)  # Assuming user is available
        total_questions = questions.count()  # Count total questions
        return render(request, 'quizzes/quiz_result.html', {'quiz': quiz, 'score': score, 'total_questions': total_questions,})

    return render(request, 'quizzes/quiz_detail.html', {'quiz': quiz, 'questions': questions})


@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':

        user_answers = []  # List to hold answers for JSON
        # Iterate through each question and save the corresponding answer
        for question in questions:
            answer = request.POST.get(f'question_{question.id}')
            if answer:
                # Save the user answer
                user_answer = UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    answer=answer,
                    submitted_at=timezone.now()  # Store the current timestamp
                )
                # Append the answer to the user_answers list
                user_answers.append({
                    'user_id' : request.user.username,
                    'question_id': question.id,
                    'answer': answer,
                    'submitted_at': user_answer.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                })

        # Write the user answer data to a JSON file
        json_file_path = './file.json'  # Set the desired file path here
        try:
            with open(json_file_path, 'w') as json_file:  # Append to the file
                json.dump(user_answers, json_file)
                json_file.write('\n')  # Optional: write a newline for better readability
        except IOError as e:
            # Handle file writing errors (optional)
            print(f"Failed to write to JSON file: {e}")
        return render(request, 'quizzes/home.html', {})
    return render(request, 'quizzes/home.html', {})

def home(request):
    return render(request, 'quizzes/home.html', {})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page or another page
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'quizzes/login.html')  # Render the login template

# quizzes/views.py
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully')
            # Optionally log the user in and redirect to another page
            # from django.contrib.auth import login
            login(request, user)
            return redirect('quizzes/packages')  # Redirect to the login page or home page after registration
        else:
            messages.error(request, 'Error processing your registration')
    else:
        form = RegistrationForm()
    return render(request, 'quizzes/register.html', {'form': form})