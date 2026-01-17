import random
def generer_solution_aleatoire(n):
    rand = list(range(n))
    # random.seed(42) 
    random.shuffle(rand)
    return rand

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

def eval_mo(solution, temps, dates_fin):
    cmax = cout_CMax(solution, temps)
    tardiness = cout_Tardiness(solution, temps, dates_fin)
    return (cmax, tardiness)

import matplotlib.pyplot as plt
def projection(s1, s2, temps, dates_fin):
    cout_s1 = cout_CMax(s1, temps)
    cout_s2 = cout_CMax(s2, temps)
    tar_s1 = cout_Tardiness(s1, temps, dates_fin)
    tar_s2 = cout_Tardiness(s2, temps, dates_fin)

    plt.scatter(cout_s1, tar_s1, label="solution aléatoire")
    plt.scatter(cout_s2, tar_s2, label="solution mono-objective")

    plt.xlabel("coût")
    plt.ylabel("tardiness")   # typo fixed
    plt.legend(loc="upper left")
    plt.show()



def domine(sol_a, sol_b):
    #Vérifie si sol_a domine strictement sol_b (pour 2 objectifs à minimiser)
    f1_a, f2_a = sol_a
    f1_b, f2_b = sol_b    
    meilleur_ou_egal = (f1_a <= f1_b) and (f2_a <= f2_b)#tout seul veut dire : des solutions identiques se dominent !
    strictement_meilleur = (f1_a < f1_b) or (f2_a < f2_b)  # tt seul resone sur un seul objectif 
    return meilleur_ou_egal and strictement_meilleur

def filtrage_offline(solutions):
    
    non_dominees = []
    
    for sol in solutions:
        est_dominee = False
        
        # Vérifier si sol est dominée par une autre solution
        for autre in solutions:
            if autre != sol and domine(autre, sol):
                est_dominee = True
                break
        
        if not est_dominee:
            non_dominees.append(sol)
    
    return non_dominees

#  Génère n_solutions aléatoires et filtre les dominées
def generer_solutions(n, m, times, due_dates, n_solutions=500):

    print(f" Génération de {n_solutions} solutions aléatoires...")
    
    solutions = []
    for i in range(n_solutions):
        # Générer une solution aléatoire
        pi = generer_solution_aleatoire(n)
        # Évaluer sur les deux objectifs
        f1, f2 = eval_mo(pi, times, due_dates)
        
        
        # Stocker (objectifs uniquement ou avec la permutation)
        solutions.append((f1, f2))
    
    return solutions


def projection_solutions(solutions):
    for i, s in enumerate(solutions):
        plt.scatter(s[0], s[1], label=f"solution {i}")

    plt.xlabel("coût")
    plt.ylabel("tardiness")
    plt.legend(loc="upper left")
    plt.show()
