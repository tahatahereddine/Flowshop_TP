import time
import matplotlib.pyplot as plt
import numpy as np

# Import your existing functions
from Flowshop_multi_obj import (
    generer_solution_aleatoire, eval_mo, climber_best_mono,
    filtrage_offline, algo_pareto, charger_instance
)
from hypervolume import calculer_hypervolume

def run_benchmark(n_jobs, n_machines, temps, dates_fin, instance_name, n_runs=10, max_evals=1000):
    """
    Runs the benchmark for Question 11:
    - Executes Scalaire and Pareto algorithms 'n_runs' times.
    - Measures Execution Time and Hypervolume.
    - Generates comparative plots.
    """
    print(f"--- Starting Benchmark on {n_jobs} jobs, {n_machines} machines ---")
    print(f"--- {n_runs} runs per algorithm | Max Evals: {max_evals} ---")

    # Reference point for Hypervolume (Must be strictly worse than any possible solution)
    # Adjust these values based on your instance data scale. 
    # For large instances (50 jobs), Cmax ~3000-5000, Tsum ~10000+. 
    ref_point = (10000, 100000) 

    # Data Storage
    results = {
        "scalaire": {"times": [], "hvs": [], "fronts": []},
        "pareto":   {"times": [], "hvs": [], "fronts": []}
    }

    # Parameters for Scalar Algorithm
    alphas = [f/10 for f in range(0, 11)] # 0.0 to 1.0 (11 steps)

    # --- Loop for N_RUNS ---
    for run in range(n_runs):
        print(f"Run {run + 1}/{n_runs}...")

        # ---------------------------
        # 1. Benchmark SCALAIRE
        # ---------------------------
        start_time = time.time()
        archive_scalaire = []
        
        # We manually run the loop here to capture the final front correctly for benchmarking
        # (This mimics your algo_scalaire logic but ensures we just get the front for HV calc)
        for alpha in alphas:
            poids = (alpha, 1 - alpha)
            sol_init = generer_solution_aleatoire(n_jobs)
            
            # Optimisation using your provided climber
            # Note: Your climber takes 'poids' as a tuple
            sol_opt, score = climber_best_mono(sol_init, temps, dates_fin, poids)
            
            # Real Evaluation (Objective Space)
            vals = eval_mo(sol_opt, temps, dates_fin)
            archive_scalaire.append(vals)
            
        # Filter to get the actual Pareto front for this run
        front_scalaire = filtrage_offline(archive_scalaire)
        
        elapsed_scalaire = time.time() - start_time
        hv_scalaire = calculer_hypervolume(front_scalaire, ref_point)
        
        results["scalaire"]["times"].append(elapsed_scalaire)
        results["scalaire"]["hvs"].append(hv_scalaire)
        results["scalaire"]["fronts"].append(front_scalaire)

        # ---------------------------
        # 2. Benchmark PARETO
        # ---------------------------
        start_time = time.time()
        
        # Using your existing algo_pareto function
        # Ensure it returns a list of tuples [(f1, f2), ...]
        archive_pareto = algo_pareto(n_jobs, n_machines, temps, dates_fin, max_evals)
        
        # Since your algo_pareto returns [s['objs'] for s in archive], it is already a list of tuples
        front_pareto = archive_pareto 
        
        elapsed_pareto = time.time() - start_time
        hv_pareto = calculer_hypervolume(front_pareto, ref_point)
        
        results["pareto"]["times"].append(elapsed_pareto)
        results["pareto"]["hvs"].append(hv_pareto)
        results["pareto"]["fronts"].append(front_pareto)

    # --- VISUALIZATION (Question 11) ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Benchmark Results (Instance {n_jobs}x{n_machines})', fontsize=16)

    # Plot 1: Pareto Fronts (Scatter) - We plot the median run
    # This shows the "typical" shape of the front found by each algo
    ax1 = axes[0, 0]
    med_idx_sca = np.argsort(results["scalaire"]["hvs"])[len(results["scalaire"]["hvs"])//2]
    med_idx_par = np.argsort(results["pareto"]["hvs"])[len(results["pareto"]["hvs"])//2]
    
    f_sca = results["scalaire"]["fronts"][med_idx_sca]
    f_par = results["pareto"]["fronts"][med_idx_par]
    
    ax1.scatter([p[0] for p in f_sca], [p[1] for p in f_sca], label='Scalaire', c='blue', alpha=0.7)
    ax1.scatter([p[0] for p in f_par], [p[1] for p in f_par], label='Pareto', c='red', marker='x')
    ax1.set_title('Pareto Fronts (Median Run)')
    ax1.set_xlabel('Makespan ($C_{max}$)')
    ax1.set_ylabel('Tardiness ($T_{sum}$)')
    ax1.legend()
    ax1.grid(True)

    # Plot 2: Hypervolume Distribution (Boxplot)
    # Boxplot allows us to see stability (size of box) and quality (height of box)
    ax2 = axes[0, 1]
    ax2.boxplot([results["scalaire"]["hvs"], results["pareto"]["hvs"]], labels=['Scalaire', 'Pareto'])
    ax2.set_title('Quality Distribution (Hypervolume)')
    ax2.set_ylabel('Hypervolume (Higher is Better)')
    ax2.grid(True)

    # Plot 3: Execution Time Distribution (Boxplot)
    ax3 = axes[1, 0]
    ax3.boxplot([results["scalaire"]["times"], results["pareto"]["times"]], labels=['Scalaire', 'Pareto'])
    ax3.set_title('Cost Distribution (Execution Time)')
    ax3.set_ylabel('Time (seconds)')
    ax3.grid(True)

    # Plot 4: Summary Table
    ax4 = axes[1, 1]
    ax4.axis('off')
    col_labels = ['Mean HV', 'Std Dev HV', 'Mean Time (s)']
    table_vals = [
        [f"{np.mean(results['scalaire']['hvs']):.2f}", f"{np.std(results['scalaire']['hvs']):.2f}", f"{np.mean(results['scalaire']['times']):.4f}"],
        [f"{np.mean(results['pareto']['hvs']):.2f}", f"{np.std(results['pareto']['hvs']):.2f}", f"{np.mean(results['pareto']['times']):.4f}"]
    ]
    table = ax4.table(cellText=table_vals, colLabels=col_labels, rowLabels=['Scalaire', 'Pareto'], loc='center', cellLoc='center')
    table.scale(1, 2)
    ax4.set_title('Statistical Summary')

    plt.tight_layout()
    instance_name = instance_name.replace(".txt", "")
    plt.savefig("./stats/"+instance_name)
    plt.show()

# --- Example Usage ---
if __name__ == "__main__":
    # Load your instance (Replace with correct path)
    instance_name = "50_10_01.txt"
    n, m, temps, dates_fin = charger_instance("instances/" + instance_name)
    
    # Run the benchmark
    run_benchmark(n, m, temps, dates_fin, instance_name, n_runs=10, max_evals=100)
    pass