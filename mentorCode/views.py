from django.shortcuts import render,redirect 
from django.contrib import messages
import time
from django.http import HttpResponse
from base.models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, JsonResponse
from random import randint
from math import ceil
import os
import subprocess
import shutil  # hehehe
from codeplay.settings import PYTHON_PATH, GCC_PATH, GPP_PATH
from django.http import HttpResponseRedirect



# consts
SUCCESS_STRING = "All tests passed successfully! Ready to submit solution."
PYTHON_DISALLOWED_IMPORTS = ["import os", "import subprocess"]
C_DISALLOWED_IMPORTS = ["#include <unistd.h>"] 



"""
Creates a directory in user_solutions/solutions/ with the current user's username
if it doesn't already exist.
"""
def create_user_directory(username):
    try:
        os.makedirs(f"user_solutions/solutions/{username}", exist_ok=True)
        print("USER DIRECTORY CREATED")
    except Exception as error:
        print(f"ERROR WHEN CREATING USER DIRECTORY: {error}")


"""
Takes problem title and converts it into a snake_case file name.
Example: "Hello World" -> "hello_world".
"""
def transform_title_python(title):
    return title.lower().replace(" ", "_")


"""
Takes problem title and converts it into a PascalCase file name.
Example: "Hello World" -> "HelloWorld"
"""
def transform_title_pascal(title):
    words = title.split()
    pascal_case_title = ''.join(word.capitalize() for word in words)
    return pascal_case_title


"""
Easy: 7 minutes, up to 25% of bonus xp
Meduim: 15 minutes, up to 35% of bonus xp
Hard: 30 minutes, up to 50% of bonus xp
"""
def calculate_bonus_points(base_xp, difficulty, time_taken):
    if difficulty == 'Easy':
        bonus = (time_taken / (7 * 60)) * (base_xp * 0.25)
    if difficulty == 'Medium':
        bonus = (time_taken / (15 * 60)) * (base_xp * 0.35)
    if difficulty == 'Hard':
        bonus = (time_taken / (30 * 60)) * (base_xp * 0.50)
    
    return ceil(bonus)


def mentor_waiting(request):
    if not request.user.is_authenticated or not request.user.is_mentor:
        return redirect('coding_selection') 

    # Mentor Starts in an 'open waiting' state
    mentor = request.user
    mentor_availability, created = MentorAvailability.objects.get_or_create(user=mentor)
    mentor_availability.is_available = True

    mentor_availability.save()
    attempts = 0
    while (attempts < 3):  # Main waiting loop

        pending_problem = PendingProblem.objects.filter(mentor_assigned=False).first()
        print(5)
        
        if pending_problem:
  
            pending_problem.mentor_assigned = True
   
            pending_problem.save()
      
            # Get mentee information
            problem_id = pending_problem.problem.problem_id
      
            mentor_availability.is_available=False
            mentor_availability.save()
            print(10)
            return redirect('coding_problem',problem_id=problem_id)
            
        time.sleep(3)
        attempts += 1
            # return render(request, 'mentorCode/mentor_search.html')
    return redirect('dashboard')
      
            



def coding_selection(request):

    if request.user.is_authenticated and request.user.is_mentor:
        return redirect('mentor_waiting')

    form = MenteeProblemSearchForm()

    if request.method == "POST":
        form = MenteeProblemSearchForm(request.POST)  
        if form.is_valid():
            mentee_language = form.cleaned_data['language'] #USED FOR POST NOT GET
            mentee_difficulty = form.cleaned_data['difficulty']
            mentee_topic = form.cleaned_data['topic']  
            
            # mentee_language = request.GET.get('language')
            # mentee_difficulty = request.GET.get('difficulty')
            # mentee_topic = request.GET.get('topic')
            
            # Store these criteria (e.g., in the session)
            request.session['mentee_language'] = mentee_language.language_name  # Assuming language_name exists
            request.session['mentee_difficulty'] = mentee_difficulty
            request.session['mentee_topic'] = mentee_topic
            if mentee_language and mentee_difficulty:
                matching_problems = Problem.objects.filter(
                    problemtolang__language__language_name=mentee_language.language_name,
                    difficulty=mentee_difficulty
                ).exclude(
                    usertoproblem__user=request.user,  
                    usertoproblem__solved=True,  
                )
                if matching_problems.exists():
                    # Select a problem (adjust the logic if needed)
                    selected_problem = matching_problems.first() 
                    PendingProblem.objects.create(
                        problem=selected_problem,
                        mentee=request.user,
                    )
                    return redirect('mentor_search', problem_id=selected_problem.problem_id)

                else:
                    messages.info(request, 'No problems matching your criteria found...')
            else:
                messages.info(request, "Form was filled out incorrectly, please try again")
        else:
            messages.info(request, "Form was filled out incorrectly, please try again")
    # else:
    #     messages.info(request, "Form was filled out incorrectly, please try again")
    context = {'form': form}
    return render(request, 'mentorCode/selection_page.html', context)

    """ The difficulty, language and topic are chosen and stored
    They must be assigned variables that are then redirected 
    into the mentor search
    """

def mentor_search(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)

    attempts = 0
    while True:  # Loop until we find a mentor
        available_mentors = User.objects.filter(
            is_mentor=True,
            mentoravailability__is_available=True,
            # usertolang__language__in=problem.problemtolang_set.values('language') #THIS PART IS FOR IF THE MENTOR's   
                                                                        # PREFERRED LANGUAGE THIS WILL BE TURNED ON LATER FOR PROD
        )
        assigned_problems = PendingProblem.objects.filter(
            mentor_assigned=True,
            mentee = request.user,
            problem = problem,
        )
        if available_mentors.exists():
            selected_mentor = available_mentors.first()  # Your logic to select one mentor
            selected_problem = problem
            # Logic to connect mentee and mentor (e.g., Chatroom creation)
            PendingProblem.objects.filter(mentee=request.user).delete()
            return redirect('coding_problem', problem_id=problem_id) 
            break  # Exit the loop since we found a mentor
        elif assigned_problems.exists():
            PendingProblem.objects.filter(mentee=request.user).delete()

            return redirect('coding_problem', problem_id=problem_id) 
        else:
            if attempts > 3:  # Example: Give up after 3 tries
                messages.error(request, 'No mentors currently available, please try again later.') 
                return redirect('coding_selection')
            attempts += 1
            time.sleep(5) 


   
    # matching_problems = Problem.objects.filter(
    # problemtolang__language__language_name=mentee_language,
    # difficulty=mentee_difficulty
    # ).exclude(
    # usertoproblem__user=request.user,
    # usertoproblem__solved=True,  # Ensure not already solved
    # )

    return render(request, 'mentorCode/mentor_search.html')
    """You must find a problem with the required fields in coding_selection
    that problem cannot have been attempted by the user before
    They also have to find a mentor
    """

def coding_problem(request, problem_id):
    if not request.user.is_authenticated:
        return redirect("login-user")
    shared_data = request.session.get('shared_data', {})
    current_user_username = request.user.username
    current_user_id = str(request.user.user_id)
    user_dir_name = f"{current_user_username}_{current_user_id}"

    problem = get_object_or_404(Problem,pk=problem_id)
    language = request.session.get('mentee_language')
    role = "mentor" if request.user.is_mentor else "mentee"
    context = {
        'Problem_Title': problem.title ,
        'Problem_id': problem_id,
        'Difficulty':problem.difficulty,
        'Language':language,
        'Description': problem.description,
        'role': role,
    }
    existing_entries = UserToProblem.objects.filter(user=request.user, problem=problem)
    if not existing_entries.exists():
        #debug
        print("in the solve_problem() function")
        UserToProblem.objects.create(user=request.user, problem=problem, solved=False)
        print(UserToProblem.objects.filter(user=request.user))
        print()
        current_user = User.objects.get(user_id=request.user.user_id)
        if current_user.problems_attempted is None:
            current_user.problems_attempted = 0
        current_user.problems_attempted += 1
        current_user.save()
    
    if request.method == "POST":
        user_code = request.POST["userCode"]
        print("RECEIVING USER CODE TEST:" + user_code)
        if context["Language"] == "C":
            for string in C_DISALLOWED_IMPORTS:
                if string in user_code:
                    print("Imported library currently not supported.")
                    return JsonResponse({"actual_output": "Imported library currently not supported.", "tests_passed": False})

            # write user solution to a source file
            solution_file_name = transform_title_pascal(context["Problem_Title"])
            solution = open(f"user_solutions/solutions/{user_dir_name}/C_{solution_file_name}.c", mode="w")
            solution.write(user_code)
            solution.close()
            
            # debugging
            # path = os.getcwd()
            # parent_path = os.path.abspath(os.path.join(path, os.pardir))

            # whoami_commmand = subprocess.Popen(["whoami"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # stdout, stderr = whoami_commmand.communicate()
            # whoami_output = stdout

            # id_commmand = subprocess.Popen(["id"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # stdout, stderr = id_commmand.communicate()
            # id_commmand = stdout

            # copy test file to user dir
            shutil.copy2(f"user_solutions/tests/C_{solution_file_name}_Test.c", f"user_solutions/solutions/{user_dir_name}/C_{solution_file_name}_Test.c")

            # compile the test file
            compile_test = subprocess.Popen(
                [f"{GCC_PATH}", "-o", 
                f"user_solutions/solutions/{user_dir_name}/C_{solution_file_name}_Test", 
                f"user_solutions/solutions/{user_dir_name}/C_{solution_file_name}_Test.c"], 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            )
            stdout, stderr = compile_test.communicate()
            compile_test_out = stdout  # debug
            compile_test_err = stderr  # debug

            # run test executable
            run_test_exe = subprocess.Popen(
                [f"user_solutions/solutions/{user_dir_name}/C_{solution_file_name}_Test"], 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            )
            stdout, stderr = run_test_exe.communicate()
            run_test_exe_out = stdout
            run_test_exe_err = stderr
            actual_output = run_test_exe_out
            tests_passed = SUCCESS_STRING in actual_output.decode("utf-8")
            print(tests_passed)

        if context["Language"] == "C++":
            for string in C_DISALLOWED_IMPORTS:
                if string in user_code:
                    print("Imported library currently not supported.")
                    return JsonResponse({"actual_output": "Imported library currently not supported.", "tests_passed": False})

            # write user solution to a source file
            solution_file_name = transform_title_pascal(context["title"])
            solution = open(f"user_solutions/solutions/{user_dir_name}/CPP_{solution_file_name}.cpp", mode="w")
            solution.write(user_code)
            solution.close()
            
            # debug
            # path = os.getcwd()
            # parent_path = os.path.abspath(os.path.join(path, os.pardir))

            # whoami_commmand = subprocess.Popen(["whoami"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # stdout, stderr = whoami_commmand.communicate()
            # whoami_output = stdout

            # id_commmand = subprocess.Popen(["id"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # stdout, stderr = id_commmand.communicate()
            # id_commmand = stdout

            # copy test file to user dir
            shutil.copy2(f"user_solutions/tests/CPP_{solution_file_name}_Test.cpp", f"user_solutions/solutions/{user_dir_name}/CPP_{solution_file_name}_Test.cpp")

            # compile the test file
            compile_test = subprocess.Popen(
                [f"{GPP_PATH}", "-o", 
                f"user_solutions/solutions/{user_dir_name}/CPP_{solution_file_name}_Test", 
                f"user_solutions/solutions/{user_dir_name}/CPP_{solution_file_name}_Test.cpp"], 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            )
            stdout, stderr = compile_test.communicate()
            compile_test_out = stdout  # debug
            compile_test_err = stderr  # debug

            # run test executable
            run_test_exe = subprocess.Popen(
                [f"user_solutions/solutions/{user_dir_name}/CPP_{solution_file_name}_Test"], 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            )
            stdout, stderr = run_test_exe.communicate()
            run_test_exe_out = stdout  # debug
            run_test_exe_err = stderr  # debug
            actual_output = run_test_exe_out
            tests_passed = SUCCESS_STRING in actual_output.decode("utf-8")
            print(tests_passed)
        
        if context["Language"] == "Python":
            for string in PYTHON_DISALLOWED_IMPORTS:
                if string in user_code:
                    print("Imported library currently not supported.")
                    return JsonResponse({"actual_output": "Imported library currently not supported.", "tests_passed": False})

            solution_file_name = transform_title_python(context["Problem_Title"])
            solution = open(f"user_solutions/solutions/{user_dir_name}/{solution_file_name}_sol.py", mode="w")
            solution.write(user_code)
            solution.close()
            #path = os.getcwd()
            #parent_path = os.path.abspath(os.path.join(path, os.pardir))
            # print("PATH CHECK: " + str(path))
            # print("PARENT CHECK IG:" + str(parent_path))
            
            # str_parent_path = str(parent_path)
            # debug
            # whoami_commmand = subprocess.Popen(["whoami"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # stdout, stderr = whoami_commmand.communicate()
            # whoami_output = stdout

            # id_commmand = subprocess.Popen(["id"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # stdout, stderr = id_commmand.communicate()
            # id_commmand = stdout

            # ls_command = subprocess.Popen(["ls", "-la", str_parent_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # stdout, stderr = ls_command.communicate()
            # ls_output = stdout 

            # second_ls_command = subprocess.Popen(["ls", "-la", f"{str_parent_path}usr/local/bin/"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # stdout, stderr = second_ls_command.communicate()
            # ls_out_two = stdout
            # print(ls_out_two)

            shutil.copy2(f"user_solutions/tests/{solution_file_name}_test.py", f"user_solutions/solutions/{user_dir_name}/{solution_file_name}_test.py")

            # run tests
            out = subprocess.Popen([f"{PYTHON_PATH}", f"user_solutions/solutions/{user_dir_name}/{solution_file_name}_test.py",], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = out.communicate()
            actual_output = stdout
            tests_passed = SUCCESS_STRING in actual_output.decode("utf-8")
            print(tests_passed)
            
            
        
        return JsonResponse({"actual_output": actual_output.decode("utf-8"), "tests_passed": tests_passed})
    
    # start_time = time()
    # request.session['start_time'] = start_time
    request.session.save()

    return render(request, 'mentorCode/coding_page.html', context)
    

def coding_completion(request):
    return render(request, 'mentorCode/completion_screen.html')

def privacy_policy(request):
    return render(request, 'landing_page/privacy_policy.html')
