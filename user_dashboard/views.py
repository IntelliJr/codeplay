import json
from django.shortcuts import render
from django.db.models import Count
from base.models import UserToProblem, ProblemToLang, CodingLanguage, Problem

# declaring a global variable called language_stats to use it in another view too 

global language_stats

def user_dashboard(request):
    
    global language_stats
    

    user_id = request.user.user_id  
    
    '''
     Getting the fields from the queryset. To display the number of problems solved in a specific language, we need the language ID corresponding to the language
     values() gets the language_id column and annotate() is used to get aggregate functions like sum, count etc. 

    '''
    language_stats = UserToProblem.objects.filter(user_id=user_id, solved=True) \
        .exclude(language_id__isnull=True)\
        .values('language_id')\
        .annotate(num_problems_solved=Count('language_id'))
        
    #debug prints    
    print()
    print("Language stats: ")
    print(language_stats)    

    # getting language names corresponding to language IDs
    for stat in language_stats:
        
        language = CodingLanguage.objects.get(language_id=stat['language_id']) # dict[key] = value format
        stat['language_name'] = language.language_name

    # Convert language_stats to JSON format
    language_stats_json = json.dumps(list(language_stats))
    print()
    print("Language stats JSON: ")
    print() 
    print(language_stats_json)
    

    # Get language names corresponding to language IDs and difficulty level for each problem
    
    language_stats =  UserToProblem.objects.filter(user_id=user_id, solved=True) \
        .values('language_id','problem_id')\
        .exclude(language_id__isnull=True)\
        .annotate(num_problems_solved=Count('language_id'))

    
    for stat in language_stats:
        language = CodingLanguage.objects.get(language_id=stat['language_id'])
        stat['language_name'] = language.language_name

        # Get difficulty level for each problem
        problem = Problem.objects.get(problem_id=stat['problem_id'])
        stat['difficulty_level'] = problem.difficulty

    # Convert language_stats_with_difficulty to JSON format
    print()
    print("Language stats with diffculty ")
    print(language_stats)
    print() 

    
    language_stats_with_difficulty_json = json.dumps(list(language_stats))
    
    
    
    
    
    print()
    print("Language stats with diffculty JSON ")
    print() 

    print(language_stats_with_difficulty_json)

    return render(request, 'user_dashboard/dashboard.html', {
        'language_stats_json': language_stats_json,
        'language_stats':language_stats,
        'language_stats_with_difficulty_json': language_stats_with_difficulty_json,
    })
    
    
def view_problems(request):
    
    
    user_id = request.user.user_id  
    
    language_stats_unsolved = UserToProblem.objects.filter(user_id=user_id,solved=False) \
        .exclude(language_id__isnull=True)\
        .values('language_id','problem_id')
            
    language_stats_solved =  UserToProblem.objects.filter(user_id=user_id,solved=True) \
        .exclude(language_id__isnull=True)\
        .values('language_id','problem_id')    
        
    for stat in language_stats_solved:
       problem = Problem.objects.get(problem_id = stat['problem_id'])
       stat['problem_desc'] = problem.description
       stat['title'] = problem.title
       stat['difficulty'] = problem.difficulty
       language = CodingLanguage.objects.get(language_id=stat['language_id']) # dict[key] = value format
       stat['language_name'] = language.language_name       
       
    print()
    print("Language Stats Solved")
    print(language_stats_solved)  

    #debug prints    
    print()
    print("Language stats unsolved: ")
      
    # getting language names corresponding to language IDs
    for stat in language_stats_unsolved:
        problem = Problem.objects.get(problem_id = stat['problem_id'])
        stat['problem_desc'] = problem.description
        stat['title'] = problem.title
        stat['difficulty'] = problem.difficulty
        language = CodingLanguage.objects.get(language_id=stat['language_id']) # dict[key] = value format
        stat['language_name'] = language.language_name
    
    print(language_stats_unsolved)
    print()

    context = {
        
        'language_stats_unsolved': language_stats_unsolved,
        'language_stats_solved': language_stats_solved
    }
    
    return render(request, 'user_dashboard/view_problems.html',context)
        
