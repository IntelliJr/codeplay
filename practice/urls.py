from django.urls import path
from . import views

urlpatterns = [
    path('select_problem', views.select_problem, name="select_problem"),
    path('solve_problem', views.solve_problem, name="solve_problem"),
    path('problem_solved', views.problem_solved, name="problem_solved"),
]
