import random


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

    n = int(lignes[0].split()[0])   # nombre de jobs
    m = int(lignes[1].split()[0])   # nombre de machines

    temps_traitement = []
    dates_fin = []


    i = 3  # on saute les 3 premières lignes (seed ignorée)
    while i < len(lignes):

        try:
            # ligne i : identifiant du job
            job_id = int(lignes[i].split()[0])
            # ligne i+1 : ignorer (seed ou valeur inutile)
            # ligne i+2 : temps sur chaque machine
            
            date_fin = int(lignes[i+1].split()[0])
            dates_fin.append(date_fin)

            durees = [int(x) for x in lignes[i+2].split()]

            temps_traitement.append(durees)
            i += 3  # passer au bloc suivant
        except (ValueError, IndexError):
            break  # fin de fichier ou format inattendu

    return n, m, temps_traitement, dates_fin

# fichier = "./instances/50_20_01.txt"
# n, m, temps, dates_fin = charger_instance(fichier)

def print_problem(n, m, temps, dates_fin):
    print(f"Nombre de jobs : {n}")
    print(f"Nombre de machines : {m}")
    print("Matrice des durées :")
    for i, ligne in enumerate(temps):
        print(f"Job {i} : {ligne}")
    # dates_fin
    print("Dates de fin :")
    for i, date in enumerate(dates_fin):
        print(f"Job {i} : {date}")


def generer_solution_aleatoire(n):
    rand = list(range(n))
    random.shuffle(rand)
    return rand

def cout_CMax(solution, temps):
    
    n = len(solution) # number of jobs
    m = len(temps[0]) # number of machines

    # makespan
    cout_matrix = [[0]*m for _ in range(n)]

    for i in range(n):
        job_id = solution[i]
        for j in range(m):
            if i==0 and j==0:
                cout_matrix[job_id][j]=temps[job_id][j]
            elif i==0 :
                cout_matrix[job_id][j]=temps[job_id][j] + temps[job_id][j-1]
            else:
                prev_job_id = solution[i-1]
                max_value = max(cout_matrix[prev_job_id][j], cout_matrix[job_id][j-1])
                cout_matrix[job_id][j] = temps[job_id][j] + max_value
    return cout_matrix[solution[-1]][-1]
def cout_Tardiness(solution, temps, dates_fin):
    n = len(solution) # number of jobs

    CMax = cout_CMax(solution, temps)
    tardiness = 0
    for i in range(n):
        job_id = solution[i]
        tardiness += max(0, CMax - dates_fin[job_id])
    return tardiness

# fonction eval_mo qui calcule le coût d’une solution π passée en paramètre pour chacun des objectifs f (π) = (f1(π), f2(π)) == (Cmax(π), Tsum(π)).
def eval_mo(solution, temps, dates_fin):
    cmax = cout_CMax(solution, temps)
    tardiness = cout_Tardiness(solution, temps, dates_fin)
    return (cmax, tardiness)
# Générer une solution aléatoire et l’évaluer. Comparer sa qualité avec la meilleure solution que vous avez identifiée pour le FSP mono-objectif, projetée dans l’espace objectif (f1, f2)
def generer_et_evaluer_solution(temps, dates_fin):
    n = len(temps)
    solution = generer_solution_aleatoire(n)
    eval = eval_mo(solution, temps, dates_fin)
    return solution, eval

def filtrage_offline(temps, dates_fin,n_solutions=500):
    n = len(temps)
    solutions = []
    evaluations = []

    for _ in range(n_solutions):
        sol = generer_solution_aleatoire(n)
        eval = eval_mo(sol, temps, dates_fin)
        solutions.append(sol)
        evaluations.append(eval)

    # Filtrage des solutions non dominées
    non_dominated_solutions = []
    non_dominated_evaluations = []

    for i in range(len(solutions)):
        dominated = False
        for j in range(len(solutions)):
            if i != j:
                if (evaluations[j][0] <= evaluations[i][0] and evaluations[j][1] < evaluations[i][1]) or \
                   (evaluations[j][0] < evaluations[i][0] and evaluations[j][1] <= evaluations[i][1]):
                    dominated = True
                    break
        if not dominated:
            non_dominated_solutions.append(solutions[i])
            non_dominated_evaluations.append(evaluations[i])
    return non_dominated_solutions, non_dominated_evaluations

# question 5 tp2: 



# Question 4
def echange(solution, p1, p2):
    n = len(solution)
    if p1 > n or p2 > n:
        print("Error: position out of bound!")
        return None
    
    tmp = solution[p1 - 1]
    solution[p1 - 1] = solution[p2 - 1]
    solution[p2 - 1] = tmp
    return solution

# [8, 7, 6, 5, 4, 3, 2, 1] --> [8, 3, 6, 5, 4, 7, 2, 1]
# exemple1 = [8, 7, 6, 5, 4, 3, 2, 1]
# print(echange(exemple1, 1, 6))


# Question 5
def insere(solution, p_job, p_insert):
    n = len(solution)
    if p_insert > n or p_job > n:
        print("Error: position out of bound!")
        return None
    
    job = solution.pop(p_job - 1)
    solution.insert(p_insert - 1, job)
    return solution

# [1, 6, 8, 2, 4, 5, 3, 7]   -->  [1, 8, 2, 4, 5, 6, 3, 7]
# exemple2 = [1, 6, 8, 2, 4, 5, 3, 7]
# print(insere(exemple2, 2, 6))


# Question 6
def marche_aleatoire(temps, n = 1_000):
    n_jobs = len(temps)
    solution = generer_solution_aleatoire(n_jobs)
    cost = cout_CMax(solution, temps)
    for i in range(n):
        p1, p2 = random.sample(range(n_jobs), 2)
        new_solution = echange(solution, p1, p2)
        new_cost = cout_CMax(new_solution, temps)

        if new_cost < cost:
            solution = new_solution
            cost = new_cost
    return solution, cost

# marche_aleatoire(temps, 1_000)



# Question 7
def climber_first(temps):
    n = len(temps)
    solution = generer_solution_aleatoire(n)
    cost = cout_CMax(solution, temps)
    improved = True
    while improved:
        improved = False
        for i in range(1,n):
            for j in range(i+1, n+1):
                voisin = echange(solution, i, j)
                new_cost = cout_CMax(voisin, temps)
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


def climber_best(temps):
    n = len(temps)
    solution = generer_solution_aleatoire(n)
    cost = cout_CMax(solution, temps)
    improved = True
    while improved:
        improved = False
        # Generer les voisins
        voinsins = []
        costs = []
        for i in range(1,n):
            for j in range(i+1, n+1):
                voisin = echange(solution, i, j)
                voinsins.append(voisin)
                costs.append(cout_CMax(voisin, temps))
        minimum = min(costs)
        if minimum < cost:
            voisin_best_index = costs.index(minimum)
            solution = voinsins[voisin_best_index]
            cost = minimum
            improved = True
            
               
    return  solution, cost


# Question 8
def custom_solution(temps, iterations=100):
    n = len(temps)
    solution = generer_solution_aleatoire(n)
    cost = cout_CMax(solution, temps)

    iter = 0
    while iter < iterations:
        iter += 1
        # Generer les voisins
        voinsins = []
        costs = []
        for i in range(1,n):
            for j in range(i+1, n+1):
                voisin = echange(solution, i, j)
                voinsins.append(voisin)
                costs.append(cout_CMax(voisin, temps))
        minimum = min(costs)
        if minimum < cost:
            voisin_best_index = costs.index(minimum)
            solution = voinsins[voisin_best_index]
            cost = minimum            
               
    return  solution, cost

# sol1, cost1 = marche_aleatoire(temps, 1_000)
# print(f'Marche Aleatoire: coût = {cost1}')

# sol2, cost2 = climber_first(temps)
# print(f'Climber first: coût = {cost2}')

# sol3, cost3 = climber_best(temps)
# print(f'Climber best: coût = {cost3}')

# sol4, cost4 = custom_solution(temps)
# print(f'Propre solution: coût = {cost4}')