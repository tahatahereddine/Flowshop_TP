import random

import os
import time
'''
Le problème du fowshop de p ermutation (FSP) est un problème d'ordonnancement très étudié
dans la littérature, avec b eaucoup de variantes dont la plupart sont NP-complètes. On s'intéresse ici
au problème à m ∈Nmachines avec p our ob jectif la minimisation de la date de fin d'ordonnancement.
Une instance de FSP est comp osée de n tâches (jobs) J1 à Jn à traiter, m machines M1 à Mm,
où chaque tâche doit être traitée dans un ordre imp osé, et un ensemble de n ×m tâches tij , où tij
représente le temps de traitement de la tâche Ji sur la machine mj . Deux tâches ne p euvent pas être
traitées simultanément sur une machine et dans la variante du problème considérée, toutes les tâches
doivent être traitées dans le même ordre sur chaque machine (on parle de flow-shop de permutation ).
Chaque tâche est programmée à une date sij 
'''

def charger_instance(chemin):
    with open(chemin, "r") as f:
        lignes = f.readlines()
    lignes = [l.strip() for l in lignes if l.strip()]
    n = int(lignes[0].split()[0])
    m = int(lignes[1].split()[0])
    temps_traitement = []
    i = 3 
    while i < len(lignes):
        try:
            job_id = int(lignes[i].split()[0])
            durees = [int(x) for x in lignes[i+2].split()]
            temps_traitement.append(durees)
            i += 3  
        except (ValueError, IndexError):
            break 
    return n, m, temps_traitement

# fichier = "./instances/50_20_01.txt"
# n, m, temps = charger_instance(fichier)

def print_problem(n, m, temps):
    print(f"Nombre de jobs : {n}")
    print(f"Nombre de machines : {m}")
    print("Matrice des durées :")
    for i, ligne in enumerate(temps):
        print(f"Job {i} : {ligne}")


def generer_solution_aleatoire(n):
    rand = list(range(n))
    random.shuffle(rand)
    return rand

def cout_CMax(solution, temps):
    
    n = len(solution)
    m = len(temps[0])
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        job = solution[i]
        for j in range(m):
            if i == 0 and j == 0:
                C[i][j] = temps[job][j]
            elif i == 0:
                C[i][j] = C[i][j-1] + temps[job][j]
            elif j == 0:
                C[i][j] = C[i-1][j] + temps[job][j]
            else:
                C[i][j] = max(C[i-1][j], C[i][j-1]) + temps[job][j]

    return C[-1][-1]

eval_counter = 0

# Wrapper autour de cout_CMax pour compter les évaluations
def cout_CMax_count(solution, temps):
    global eval_counter
    eval_counter += 1
    return cout_CMax(solution, temps)



# Question 4
def echange(solution, p1, p2):
    n = len(solution)
    if p1 > n or p2 > n:
        print("Error: position out of bound!")
        return None
    
    new_solution = solution.copy()  # Copier pour ne pas modifier l'original
    new_solution[p1 - 1], new_solution[p2 - 1] = new_solution[p2 - 1], new_solution[p1 - 1]
    return new_solution

# [8, 7, 6, 5, 4, 3, 2, 1] --> [8, 3, 6, 5, 4, 7, 2, 1]
# exemple1 = [8, 7, 6, 5, 4, 3, 2, 1]
# print(echange(exemple1, p1=1, p2=6))

# Question 5
def insere(solution, p_job, p_insert):
    n = len(solution)
    if p_insert > n or p_job > n:
        print("Error: position out of bound!")
        return None
    new_solution = solution.copy()
    job = new_solution.pop(p_job - 1)
    new_solution.insert(p_insert - 1, job)
    return new_solution

# [1, 6, 8, 2, 4, 5, 3, 7]   -->  [1, 8, 2, 4, 5, 6, 3, 7]
# exemple2 = [1, 6, 8, 2, 4, 5, 3, 7]
# print(insere(exemple2, 2, 6))


# Question 6
def marche_aleatoire(temps, n = 1_000_000,voisinage="echange"):
    n_jobs = len(temps)
    solution = generer_solution_aleatoire(n_jobs)
    cost = cout_CMax_count(solution, temps)
    for i in range(n):
        p1, p2 = random.sample(range(n_jobs), 2)
        if voisinage == "echange":
            new_solution = echange(solution, p1, p2)
        elif voisinage == "insere":
            new_solution = insere(solution, p1, p2)
        else:
            raise ValueError("Voisinage inconnu, choisir 'echange' ou 'insere'")

        new_cost = cout_CMax_count(new_solution, temps)

        if new_cost < cost:
            solution = new_solution
            cost = new_cost
    return solution, cost

# marche_aleatoire(temps, 1_000)



# Question 7
def climber_first(temps,voisinage="echange"):
    n = len(temps)
    solution = generer_solution_aleatoire(n)
    cost = cout_CMax_count(solution, temps)
    improved = True
    while improved:
        improved = False
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if voisinage == "echange":
                    voisin = echange(solution, i, j)
                elif voisinage == "insere":
                    voisin = insere(solution, i, j)
                else:
                    raise ValueError("Voisinage inconnu, choisir 'echange' ou 'insere'")
                new_cost = cout_CMax_count(voisin, temps)
                if(new_cost < cost):
                    solution = voisin
                    cost = new_cost
                    improved = True
                    break
            if improved:
                break
    return  solution, cost

# sol1, cost1 = marche_aleatoire(temps, 1_000)
# sol, cost = climber_first(temps)

# print(f'Marche Aleatoire: coût = {cost1}')
# print(f'Climber first: coût = {cost}')


def climber_best(temps,voisinage="echange"):
    n = len(temps)
    solution = generer_solution_aleatoire(n)
    cost = cout_CMax_count(solution, temps)
    improved = True
    while improved:
        improved = False
        # Generer les voisins
        voinsins = []
        costs = []
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if voisinage == "echange":
                    voisin = echange(solution, i, j)
                elif voisinage == "insere":
                    voisin = insere(solution, i, j)
                else:
                    raise ValueError("Voisinage inconnu, choisir 'echange' ou 'insere'")
                voinsins.append(voisin)
                costs.append(cout_CMax_count(voisin, temps))
        minimum = min(costs)
        if minimum < cost:
            voisin_best_index = costs.index(minimum)
            solution = voinsins[voisin_best_index]
            cost = minimum
            improved = True
            
               
    return  solution, cost


# Question 8

def multi_start_local_search_with_noise(times: list[list[int]], 
                                        n_starts: int = 20, 
                                        max_iter: int = 100000,
                                        voisinage="echange",
                                        noise_level: int = 5) -> tuple[list[int], int]:
    n = len(times)
    m = len(times[0])

    best_global_solution = generer_solution_aleatoire(n)
    best_global_cost = cout_CMax_count(best_global_solution, times)

    for start in range(n_starts):
        if start == 0:
            current_solution = generer_solution_aleatoire(n)
        else:
            current_solution = best_global_solution.copy()

            for _ in range(noise_level):                
                i, j = random.sample(range(n), 2)
                if voisinage == "echange":
                    current_solution = echange(current_solution, i, j)
                elif voisinage == "insere":
                    current_solution = insere(current_solution, i, j)
                else:
                    raise ValueError(f"Voisinage inconnu : {voisinage}")

        current_cost = cout_CMax_count(current_solution, times)
        iteration = 0
        while iteration < max_iter:
            iteration += 1
            best_neighbor = None
            best_neighbor_cost = current_cost
            for _ in range(100):
                i, j = random.sample(range(n), 2)
                if voisinage == "echange":
                    new_solution = echange(current_solution, i, j)
                elif voisinage == "insere":
                    new_solution = insere(current_solution, i, j)
                else:
                    raise ValueError(f"Voisinage inconnu : {voisinage}")
                
                new_cost = cout_CMax_count(new_solution, times)
                if new_cost < best_neighbor_cost:
                    best_neighbor_cost = new_cost
                    best_neighbor = new_solution

            if best_neighbor_cost < current_cost:
                current_solution = best_neighbor
                current_cost = best_neighbor_cost
        if current_cost < best_global_cost:
            best_global_solution = current_solution.copy()
            best_global_cost = current_cost
    return best_global_solution, best_global_cost

# --- Programme de test ---
def test_algos(instance_folder, k=5, n_solutions=1_000_000):
    global eval_counter

    files = [f for f in os.listdir(instance_folder) if f.endswith(".txt")]
    print(f"Found {files} instance files.")

    for fichier in files:
        print(f"\n=== Instance : {fichier} ===")
        chemin = os.path.join(instance_folder, fichier)
        n, m, temps = charger_instance(chemin)

        for algo_name in ["marche_aleatoire", "climber_first", "climber_best", "multi_start"]:
            for voisinage in ["echange", "insere"]:
                couts = []
                evals = []

                for run in range(k):
                    eval_counter = 0

                    if algo_name == "marche_aleatoire":
                        sol, cost = marche_aleatoire(temps, n=n_solutions, voisinage=voisinage)
                    elif algo_name == "climber_first":
                        sol, cost = climber_first(temps, voisinage=voisinage)
                    elif algo_name == "climber_best":
                        sol, cost = climber_best(temps, voisinage=voisinage)
                    elif algo_name == "multi_start":
                        sol, cost = multi_start_local_search_with_noise(
                            temps, n_starts=5, max_iter=n_solutions, voisinage=voisinage
                        )
                    else:
                        raise ValueError("Algo inconnu")

                    couts.append(cost)
                    evals.append(eval_counter)

                print(f"{algo_name} ({voisinage}) -> cout moyen : {sum(couts)/k:.2f}, "
                      f"evaluations moyennes : {sum(evals)/k:.0f}")
                

# Tester tous les fichiers avec 5 exécutions et 1000 solutions max
test_algos("Flowshop_TP\\instances", k=5, n_solutions=1_000)
