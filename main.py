from TP2 import charger_instance, print_problem, cout_CMax, cout_Tardiness, eval_mo, generer_solution_aleatoire, generer_et_evaluer_solution, filtrage_offline




instance = charger_instance("instances/20_10_01.txt")
n, m, temps, dates_fin = instance
print_problem(n, m, temps, dates_fin)

cout_matrix = cout_CMax([2, 1, 0], temps)
print("Cout CMax de la solution [2, 1, 0] :", cout_matrix)

cout_tardiness = cout_Tardiness([2, 1, 0], temps, dates_fin)
print("Cout Tardiness de la solution [2, 1, 0] :", cout_tardiness)

eval = eval_mo([2, 1, 0], temps, dates_fin)
print("Evaluation multi-objectif de la solution [2, 1, 0] :", eval)
solution, eval = generer_et_evaluer_solution(temps, dates_fin)
print("Solution aléatoire générée :", solution)
print("Evaluation multi-objectif de la solution aléatoire :", eval)


# Exemple d'utilisation de la fonction de filtrage offline
non_dominated_solutions, non_dominated_evaluations = filtrage_offline(temps, dates_fin)
print("Solutions non dominées trouvées :", non_dominated_solutions)
print("Evaluations des solutions non dominées :", non_dominated_evaluations)