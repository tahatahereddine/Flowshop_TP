# Question 9
## définition des instances
import os

from Flowshop_multi_obj import *
instance_files = []
for instance_file in os.listdir("instances"):
    if instance_file.endswith(".txt"):
        instance_files.append(os.path.join("instances", instance_file))
instance_files.sort()
instance_file = instance_files.pop(-1)
instance_files.insert(0, instance_file)
print("Instance files:", instance_files)

## définition des algorithmes et des paramètres
# scalaire pour la fonction d'agrégation
alphas = [f/10 for f in range(1, 11)]  # 0.1, 0.2, ..., 0.9, 1.0

# pareto local search
algorithms = ["scalaire", "pareto"]
# critère d'arret : maximal d'évaluations
max_evals = 1000
# nombre de repetitions par instance et par algorithme
nombre_de_runs = 10


instance_name = input("Enter instance file name (or press Enter to run all instances): ")
algorithm_name = input("Enter algorithm name (scalaire or pareto, or press Enter to run all algorithms): ")
for instance_file in instance_files:
    if instance_name and instance_name not in instance_file:
        continue
    print(f"--- Analyzing instance: {instance_file} ---")
    n, m, temps, dates_fin = charger_instance(instance_file)
    for algorithm in algorithms:
        if algorithm_name and algorithm_name != algorithm:
            continue
        print(f"--- Using algorithm: {algorithm} ---")
        for run in range(nombre_de_runs):
            print(f"Run {run + 1}/{nombre_de_runs}")
            if algorithm == "scalaire":
                for alpha in alphas:
                    poids = (alpha, 1 - alpha)
                    solution_initiale = generer_solution_aleatoire(n)
                    solution_optimisee, score = climber_best_mono(solution_initiale, temps, dates_fin, poids)
                    evals = eval_mo(solution_optimisee, temps, dates_fin)
                    print(f"Alpha: {alpha:.1f}, Solution: {solution_optimisee}, Eval: {evals}, Score minimum: {score}")
            elif algorithm == "pareto":
                archive = algo_pareto(n, m, temps, dates_fin, max_evals)
                print(f"Pareto Archive Size: {len(archive)}, Solutions: {archive}")