from Flowshop_multi_obj import *
from Flowshop_mono_obj import climber_best
from math import inf

n, m, temps, dates_fin = charger_instance("instances/7_5_01.txt")
s = [2, 1, 0]
print(cout_CMax(s, temps))



# question 1
print("------------Question 1------------")
solutions_alea =[generer_solution_aleatoire(n) for _ in range(5)]
print(solutions_alea)

# question2
print("------------Question 2------------")
evals = [eval_mo(sol, temps, dates_fin) for sol in solutions_alea]
print(evals)
projection_solutions(evals)

# question 3
print("------------Question 3------------")
solution_alea = generer_solution_aleatoire(n)
solution_mono_obj = climber_best(temps)
print("solution alea: ", solution_alea)
print("solution mono obj", solution_mono_obj)
print(eval_mo(solution_alea, temps, dates_fin))
print(eval_mo(solution_mono_obj[0], temps, dates_fin))


# Question 4
print("------------Question 4------------")
projection(solution_alea, solution_mono_obj[0])


# Question 5
print("------------Question 5------------")
solutions_aleatoires = generer_solutions(n=n, m=m, times=temps, due_dates=dates_fin, n_solutions=2500)
solutions_non_dominees = filtrage_offline(solutions_aleatoires)
# projection_solutions(solutions=solutions_aleatoires)
plot_dom_nondom(solutions_aleatoires, solutions_non_dominees)
print(solutions_non_dominees)
m = inf
for t in solutions_non_dominees:
    y = fct_agg_mono_objective(t)
    if y < m: m = y
    print(y)
print("smallest score: ", m )


# Question 6
print("------------Question 6------------")
archive = create_archive(solutions_aleatoires)
plot_dom_nondom(solutions_aleatoires, archive)
print(archive)
m = inf
for t in archive:
    y = fct_agg_mono_objective(t)
    if y < m: m = y
    print(y)
print("smallest score: ", m )

## C Partie 2
# Question 7
print("------------Question 7------------")
solution = generer_solution_aleatoire(n)
climber_best_sol, cost = climber_best_mono(solution, temps, dates_fin)
print(climber_best_sol, cost)

# ajuster les poids progressivement


# Question 8
print("------------Question 8------------")
archive = algo_pareto(n, m, temps, dates_fin)
plot_dom_nondom(solutions_aleatoires, archive)
m = inf
for t in archive:
    y = fct_agg_mono_objective(t)
    if y < m: m = y
    print(y)
print("smallest score: ", m)