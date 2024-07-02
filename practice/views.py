from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, JsonResponse
from .models import Problem, CodingLanguage, ProblemToLang, User, UserToProblem
from random import randint
from time import time
from math import ceil
import os
import subprocess
import shutil  # hehehe
from codeplay.settings import PYTHON_PATH, GCC_PATH, GPP_PATH

# consts
SUCCESS_STRING = "All tests passed successfully! Ready to submit solution."
PYTHON_DISALLOWED_IMPORTS = ["import os", "import subprocess", "import importlib"]
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


@ensure_csrf_cookie
@login_required
def select_problem(request):
    if request.method == "POST":
        chosen_language = request.POST['language']
        chosen_difficulty = request.POST['difficulty']
        print("Debug: " + chosen_language + " " + chosen_difficulty)
        if chosen_language != "select" and chosen_difficulty != "select": # "select" is the default value for both language and difficulty
            # get language_id of chosen language
            chosen_language_id = CodingLanguage.objects.get(language_name=chosen_language).language_id
            
            # get all problem ids of problems with that language
            problem_to_lang_objects = ProblemToLang.objects.filter(language_id=chosen_language_id)
            problem_ids = []
            for problem in problem_to_lang_objects:
                problem_ids.append(problem.problem_id)
            
            # craft an OR statement for retrieving ALL matching problems
            pid_conditions = Q()
            for pid in problem_ids:
                pid_conditions |= Q(problem_id=pid)
            matching_problems = Problem.objects.filter(difficulty=chosen_difficulty).filter(pid_conditions)

            # get all problem_ids in matching problems
            matching_problems_ids = []
            for problem in matching_problems:
                matching_problems_ids.append(problem.problem_id)
            # get all problem_ids that the current user has already solved/failed to solve
            solved_problems_ids = []
            solved_problems = UserToProblem.objects.filter(user=request.user)
            for problem in solved_problems:
                solved_problems_ids.append(problem.problem_id)
            
            # TEST
            print(matching_problems_ids)
            print(solved_problems_ids)

            # find problem_ids of unsolved problems
            unsolved_problems_ids = list(set(matching_problems_ids) - set(solved_problems_ids))
            print(unsolved_problems_ids)

            # craft a statement to get the unsolved problems based on their problem_ids
            pid_conditions2 = Q()
            for unsolved_pid in unsolved_problems_ids:
                pid_conditions2 |= Q(problem_id=unsolved_pid)
            matching_problems = Problem.objects.filter(difficulty=chosen_difficulty).filter(pid_conditions2)
            print(matching_problems)

            problems_found = len(matching_problems)
            if problems_found == 0 or unsolved_problems_ids == []:
                messages.success(request, ("No " + chosen_language + " problems of " + chosen_difficulty + " difficulty found."))
                return redirect('select_problem')
            
            # else, select a random problem
            random_problem = matching_problems[randint(0, problems_found-1)]
            serialized_problem = {
                "problem_id": random_problem.problem_id,
                "title": random_problem.title,
                "difficulty": random_problem.difficulty,
                "description": random_problem.description,
                "experience_points": random_problem.exp,
                "language": chosen_language,
            }
            request.session['shared_data'] = serialized_problem
            request.session.save()
            
            return redirect('solve_problem')
        else:
            messages.success(request, ("Language and difficulty must be selected!"))
            return redirect('select_problem')

    else:
        return render(request, 'practice/select_problem.html', {})


@ensure_csrf_cookie
@login_required
def solve_problem(request):
    shared_data = request.session.get('shared_data', {})
    context = {
        "title": shared_data.get('title'),
        "difficulty": shared_data.get('difficulty'),
        "description": shared_data.get('description'),
        "language": shared_data.get('language'),
    }
    current_user_username = request.user.username
    current_user_id = str(request.user.user_id)
    user_dir_name = f"{current_user_username}_{current_user_id}"

    # print("USERNAME TEST: " + current_user)
    create_user_directory(user_dir_name)

    # add an entry to UserToProblem (with solved=False)
    
    current_problem = Problem.objects.get(problem_id=shared_data.get('problem_id'))
    existing_entries = UserToProblem.objects.filter(user=request.user, problem=current_problem) # check if an entry already exists
    if not existing_entries.exists():
        #debug
        print("in the solve_problem() function")
        UserToProblem.objects.create(user=request.user, problem=current_problem, solved=False)
        print(UserToProblem.objects.filter(user=request.user))
        print()
        current_user = User.objects.get(user_id=request.user.user_id)
        if current_user.problems_attempted is None:
            current_user.problems_attempted = 0
        current_user.problems_attempted += 1
                       
        current_user.save()
        #Adding language_id things here:     
        get_existing_entries = UserToProblem.objects.get(user=current_user, problem=current_problem)
        language = shared_data.get('language')
        language_id = CodingLanguage.objects.get(language_name=language)
        get_existing_entries.language = language_id
     
        get_existing_entries.save()
        

    if request.method == "POST":
        user_code = request.POST["userCode"]
        print("RECEIVING USER CODE TEST:" + user_code)
        if context["language"] == "C":
            for string in C_DISALLOWED_IMPORTS:
                if string in user_code:
                    print("Imported library currently not supported.")
                    return JsonResponse({"actual_output": "Imported library currently not supported.", "tests_passed": False})

            # write user solution to a source file
            solution_file_name = transform_title_pascal(context["title"])
            solution = open(f"user_solutions/solutions/{user_dir_name}/C_{solution_file_name}.c", mode="w")
            solution.write(user_code)
            solution.close()
            
            # debugging
            path = os.getcwd()
            parent_path = os.path.abspath(os.path.join(path, os.pardir))

            whoami_commmand = subprocess.Popen(["whoami"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = whoami_commmand.communicate()
            whoami_output = stdout

            id_commmand = subprocess.Popen(["id"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = id_commmand.communicate()
            id_commmand = stdout

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

        if context["language"] == "C++":
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
            path = os.getcwd()
            parent_path = os.path.abspath(os.path.join(path, os.pardir))

            whoami_commmand = subprocess.Popen(["whoami"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = whoami_commmand.communicate()
            whoami_output = stdout

            id_commmand = subprocess.Popen(["id"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = id_commmand.communicate()
            id_commmand = stdout

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
        
        if context["language"] == "Python":
            for string in PYTHON_DISALLOWED_IMPORTS:
                if string in user_code:
                    print("Imported library currently not supported.")
                    return JsonResponse({"actual_output": "Imported library currently not supported.", "tests_passed": False})

            solution_file_name = transform_title_python(context["title"])
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
    
    start_time = time()
    request.session['start_time'] = start_time
    request.session.save()

    return render(request, 'practice/solve_problem.html', context)


@ensure_csrf_cookie
@login_required
def problem_solved(request):
    shared_data = request.session.get('shared_data', {})
    
    start_time = request.session.get('start_time', {})
    finish_time = time()
    time_in_seconds = ceil(finish_time - start_time)

    # converting seconds to minutes and seconds
    minutes = time_in_seconds // 60
    seconds = time_in_seconds % 60

    minString = str(minutes)
    secString = str(seconds)
    # formatting in mm:ss format
    if minutes < 10:
        minString = "0" + minString
    if seconds < 10:
        secString = "0" + secString

    # calculating total points (including the bonus)
    base_xp = shared_data.get('experience_points')
    difficulty = shared_data.get('difficulty')
    total_xp = base_xp + calculate_bonus_points(base_xp, difficulty, time_in_seconds)

    current_user = User.objects.get(user_id=request.user.user_id)
    current_problem = Problem.objects.get(problem_id=shared_data.get('problem_id'))
    
    # check if the user already has an entry in UserToProblem to avoid multiple awards for a single problem
    existing_entries = UserToProblem.objects.get(user=current_user, problem=current_problem)
    problem_solved = existing_entries.solved
    if not problem_solved:
        # convert None to int as += is not defined for NoneType
        if (current_user.exp_points is None): 
            current_user.exp_points = 0
        if (current_user.problems_solved is None):
            current_user.problems_solved = 0

        # update current user data
        current_user.exp_points += total_xp
        current_user.problems_solved += 1
        current_user.save()

        # update UserToProblem data
        language = shared_data.get('language')
        language_id = CodingLanguage.objects.get(language_name=language)
        existing_entries.language = language_id
        existing_entries.solved = True
        existing_entries.time_taken = time_in_seconds
        existing_entries.save()
        
    context = {
        "title": shared_data.get('title'),
        "experience_points": total_xp,
        "minutes": minString,
        "seconds": secString,
    }

    return render(request, 'practice/problem_solved.html', context)
