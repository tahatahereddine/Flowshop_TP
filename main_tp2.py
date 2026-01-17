from Flowshop_multi_obj import *
from Flowshop_mono_obj import climber_best

n, m, temps, fins = charger_instance("instances/7_5_01.txt")

print(fins)
solution_alea = generer_solution_aleatoire(n)



solution_mono_obj = climber_best(temps)


# solutions_alea =[generer_solution_aleatoire(n) for _ in range(5)]
# print(solution_alea)

# question2

# evals = [eval_mo(sol, temps, fins) for sol in solutions_alea]
# print(evals)
# projection_solutions(evals)

# question 3
solution_alea = generer_solution_aleatoire(n)

print("solution alea: ", solution_alea)
print("solution mono obj", solution_mono_obj)
print(eval_mo(solution_alea, temps, fins))
print(eval_mo(solution_mono_obj[0], temps, fins))


projection(solution_alea, solution_mono_obj[0])


# question 5
solutions_aleatoires = generer_solutions(n=n, m=m, times=temps, due_dates=fins, n_solutions=50)
solutions_non_dominees = filtrage_offline(solutions_aleatoires)
print(solutions_aleatoires)
projection_solutions(solutions=solutions_aleatoires)
plot_dom_nondom(solutions_aleatoires, solutions_non_dominees)

# question 6
archive = create_archive(solutions_aleatoires)
print(archive)
plot_dom_nondom(solutions_aleatoires, archive)

# question 7
