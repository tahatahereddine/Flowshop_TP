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
                cout_matrix[i][j]=temps[job_id][j]
            elif i==0 :
                cout_matrix[i][j]=cout_matrix[i][j-1] + temps[job_id][j]
            elif j == 0:
                cout_matrix[i][j] = cout_matrix[i-1][j] + temps[job_id][j]
            else:
                max_value = max(cout_matrix[i-1][j], cout_matrix[i][j-1])
                cout_matrix[i][j] = temps[job_id][j] + max_value
    makespan = cout_matrix[-1][-1]
    return makespan, cout_matrix

def cout_Tardiness(solution, temps, dates_fin):
    n = len(solution) # number of jobs

    _, cout_matrix = cout_CMax(solution, temps)
    tardiness = 0
    for i in range(n):
        job_id = solution[i]
        tardiness += max(0,  cout_matrix[i][-1] - dates_fin[job_id])
    return tardiness

def eval_mo(solution, temps, dates_fin):
    makespan, _ = cout_CMax(solution, temps)
    tardiness = cout_Tardiness(solution, temps, dates_fin)
    return (makespan, tardiness)

import matplotlib.pyplot as plt
def projection(s1, s2):
    plt.scatter(s1[0], s1[1], label="solution aléatoire")
    plt.scatter(s2[0], s2[1], label="solution mono-objective")

    plt.xlabel("coût")
    plt.ylabel("tardiness")   # typo fixed
    # legend outside  the plot
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
    plt.show()



def domine(sol_a, sol_b):
    #Vérifie si sol_a domine strictement sol_b (pour 2 objectifs à minimiser)
    f1_a, f2_a = sol_a
    f1_b, f2_b = sol_b    
    meilleur_ou_egal = (f1_a <= f1_b) and (f2_a <= f2_b)#tout seul veut dire : des solutions identiques se dominent !
    strictement_meilleur = (f1_a < f1_b) or (f2_a < f2_b)  # tt seul resone sur un seul objectif 
    return meilleur_ou_egal and strictement_meilleur

def filtrage_offline(solutions):
    
    """
    solutions = [(),  (), ....., () ]
    """
    
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
    x_values = [sol[0] for sol in solutions]
    y_values = [sol[1] for sol in solutions]
    plt.scatter(x_values, y_values)
    plt.title(f"Projection {len(solutions)} solutions")
    plt.xlabel("coût")
    plt.ylabel("tardiness")
    plt.show()

def plot_dom_nondom(doms, nondoms):
    x_values = [sol[0] for sol in doms]
    y_values = [sol[1] for sol in doms]
    plt.scatter(x_values, y_values)
    nondoms.sort(key=lambda x: x[0])
    x_nd = [f[0] for f in nondoms]
    y_nd = [f[1] for f in nondoms]

    plt.scatter(x_nd, y_nd, color="orange", label="solutions non dominées")

    if len(nondoms) > 1:
        plt.plot(x_nd, y_nd, color="orange")

    plt.title(f"Projection {len(doms)} solutions")
    plt.xlabel("coût")
    plt.ylabel("tardiness")
    plt.show()

def filtrage_online(archiveA, nouv_sol):

    if nouv_sol in archiveA: return archiveA

    for s in archiveA:
        if domine(s, nouv_sol):
            return archiveA
        
    for s in archiveA[:]:
        if domine(nouv_sol, s):
            archiveA.remove(s)

    archiveA.append(nouv_sol)
    return archiveA

def create_archive(solutions):
    archiveA = []
    for s in solutions:
        archiveA = filtrage_online(archiveA, s)
    return archiveA

def fct_agg_mono_objective(solution, poids=(0.5, 0.5)):
    """
    solution : (cout, tardiness)
    g(solution) = alpha * cout + beta * tardiness
    """
    cout, tardiness = solution
    alpha, beta = poids
    return alpha * cout + beta * tardiness


from Flowshop_mono_obj import echange
def climber_best_mono(solution, temps, dates_fin):
    """
    solution initial sous forme de [0, 1, 2] ordre des jobs
    n = nbr de jobs
    """
    n = len(solution)
    s = eval_mo(solution, temps, dates_fin)
    cost = fct_agg_mono_objective(s)
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
                s = eval_mo(voisin, temps, dates_fin)
                costs.append(fct_agg_mono_objective(s))
        minimum = min(costs)
        if minimum < cost:
            voisin_best_index = costs.index(minimum)
            solution = voinsins[voisin_best_index]
            cost = minimum
            improved = True
                       
    return  solution, cost


# Question 8
def algo_pareto(n, m, temps, dates, max_evals=1000):
    print("--- Running Pareto Local Search (PLS) ---")
    
    # 1. Initialization
    s0 = generer_solution_aleatoire(n)
    
    # The Archive stores dictionaries to track if a solution has been visited
    # Structure: {'perm': [0,1..], 'objs': (100, 50), 'visited': False}
    start_node = {'perm': s0, 'objs': eval_mo(s0, temps, dates), 'visited': False}
    archive = [start_node]
    
    eval_count = 1
    
    while eval_count < max_evals:
        # 2. Selection: Pick a non-visited solution from the archive
        candidates = [s for s in archive if not s['visited']]
        
        if not candidates:
            print("   All solutions explored.")
            break
            
        # Strategy: Random selection
        current = random.choice(candidates)
        current['visited'] = True
        
        # 3. Exploration (Stochastic Neighborhood)
        # Testing ALL swaps is too slow (N*N), so we test k random swaps
        n_neighbors = 20 
        
        for _ in range(n_neighbors):
            if eval_count >= max_evals: break
            
            # Create neighbor
            perm = list(current['perm'])
            i, j = random.sample(range(n), 2)
            perm[i], perm[j] = perm[j], perm[i]
            
            # Evaluate
            f1, f2 = eval_mo(perm, temps, dates)
            eval_count += 1
            neighbor_objs = (f1, f2)
            
            # 4. Online Filtering (Using logic from your filtrage_online)
            # Check if neighbor is dominated by anyone in archive
            is_dominated = False
            for s in archive:
                if domine(s['objs'], neighbor_objs):
                    is_dominated = True
                    break
            
            if not is_dominated:
                # If valid, remove solutions in archive dominated by neighbor
                # (Re-building list is safer than modifying while iterating)
                archive = [s for s in archive if not domine(neighbor_objs, s['objs'])]
                
                # Add neighbor
                new_node = {'perm': perm, 'objs': neighbor_objs, 'visited': False}
                archive.append(new_node)
                
    # Return just the objective pairs for plotting
    return [s['objs'] for s in archive]