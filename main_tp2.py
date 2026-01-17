from Flowshop import *
from TP import climber_best

print(generer_solution_aleatoire(7))
n, m, temps, fins = charger_instance("instances/7_5_01.txt")
solution_alea = generer_solution_aleatoire(n)



solution_mono_obj = climber_best(temps)


print("solution alea: ", solution_alea)
print("solution mono obj", solution_mono_obj)
print(eval_mo(solution_alea, temps, fins))
print(eval_mo(solution_mono_obj, temps, fins))


projection(solution_alea, solution_mono_obj[0], temps, fins)



solution_aleatoires_500 = generer_solutions(n=n, m=m, times=temps, due_dates=fins, n_solutions=500)
solutions_non_dominees = filtrage_offline(solution_aleatoires_500)
print(solution_aleatoires_500)
projection_solutions(solutions=solution_aleatoires_500)
