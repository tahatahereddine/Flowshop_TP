# Question 9
## définition des instances
import os
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
lambdas = [f/10 for f in range(1, 11)]  # 0.1, 0.2, ..., 0.9, 1.0

# pareto local search
