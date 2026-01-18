import matplotlib.pyplot as plt
import numpy as np

from Flowshop_multi_obj import *
from hypervolume import calculer_hypervolume

# --- Configuration Expérimentale (Question 9) ---
N_RUNS = 10
MAX_EVALS = 5000  # Réduit pour test rapide, mettre 10000+ pour le rapport

n, m, temps, dates_fin = charger_instance("instances/50_20_01.txt")
N_JOBS = n
M_MACHINES = m
def experience_comparative():
    print(f"--- Démarrage de l'analyse expérimentale ({N_RUNS} runs) ---")
    

    
    # Définition du Point de Référence pour l'Hypervolume
    # Il doit être pire que toutes les solutions possibles.
    # On prend une estimation large.
    ref_point = (10000, 100000) 
    
    results_scalaire = [] # Stocke les valeurs d'HV
    results_pareto = []
    
    fronts_scalaire = [] # Pour le plotting
    fronts_pareto = []
    
    for run in range(N_RUNS):
        print(f"Run {run+1}/{N_RUNS}...", end="\r")
        
        # --- A. Exécution Algo Scalaire ---
        # Note: on adapte algo_scalaire pour accepter un budget si besoin
        # Ici on utilise steps=10, ce qui fait ~11 descentes locales
        sols_sca_all, front_sca = algo_scalaire(N_JOBS, M_MACHINES, temps, dates_fin, steps=10)
        hv_sca = calculer_hypervolume(front_sca, ref_point)
        results_scalaire.append(hv_sca)
        fronts_scalaire.append(front_sca)
        print("front scalaire:", front_sca)
        print(f"Run {run+1}/{N_RUNS} done. HV Scalaire: {hv_sca:.2f}", end="\r")

        
        # --- B. Exécution Algo Pareto ---
        front_par = algo_pareto(N_JOBS, M_MACHINES, temps, dates_fin, max_evals=MAX_EVALS)
        hv_par = calculer_hypervolume(front_par, ref_point)
        results_pareto.append(hv_par)
        fronts_pareto.append(front_par)
        print("front pareto:", front_par)
        print(f"Run {run+1}/{N_RUNS} done. HV Pareto: {hv_par:.2f}", end="\r")
        
    print(f"\nTerminé.")
    
    # --- Question 10 : Analyse Graphique (Affichage du Run Médian) ---
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    # On affiche le dernier run comme exemple
    x_s = [p[0] for p in fronts_scalaire[-1]]
    y_s = [p[1] for p in fronts_scalaire[-1]]
    plt.scatter(x_s, y_s, c='blue', label='Scalaire', marker='o', alpha=0.6)
    
    x_p = [p[0] for p in fronts_pareto[-1]]
    y_p = [p[1] for p in fronts_pareto[-1]]
    plt.scatter(x_p, y_p, c='red', label='Pareto (PLS)', marker='x')
    
    plt.title("Comparaison des Fronts (Dernier Run)")
    plt.xlabel("Makespan")
    plt.ylabel("Tardiness")
    plt.legend(loc='upper left')
    plt.grid(True)
    
    # --- Question 11 : Indicateurs (Boxplot) ---
    plt.subplot(1, 2, 2)
    data = [results_scalaire, results_pareto]
    plt.boxplot(data, tick_labels=['Scalaire', 'Pareto (PLS)'])
    plt.title("Distribution de l'Hypervolume (10 runs)")
    plt.ylabel("Hypervolume (Plus haut = Mieux)")
    plt.grid(True, axis='y')
    
    plt.tight_layout()
    plt.show()
    
    # Affichage tableau synthétique
    print("\n--- Résultats Synthétiques (Hypervolume) ---")
    print(f"Scalaire : Moyenne = {np.mean(results_scalaire):.2f}, Ecart-type = {np.std(results_scalaire):.2f}")
    print(f"Pareto   : Moyenne = {np.mean(results_pareto):.2f}, Ecart-type = {np.std(results_pareto):.2f}")

# Lancer l'expérience
if __name__ == "__main__":
    experience_comparative()