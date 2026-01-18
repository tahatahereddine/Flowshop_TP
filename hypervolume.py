def calculer_hypervolume(front, point_ref):
    """
    Calcule l'hypervolume 2D (minimisation) par rapport à un point de référence.
    front : liste de tuples [(f1, f2), ...]
    point_ref : tuple (ref_x, ref_y)
    """
    # 1. Trier le front par le premier objectif (croissant)
    # On suppose que le front est déjà filtré (non-dominé)
    front_trie = sorted(front, key=lambda x: x[0])
    
    # 2. Nettoyage des points qui dépassent le point de référence (sécurité)
    front_valide = [p for p in front_trie if p[0] < point_ref[0] and p[1] < point_ref[1]]
    
    if not front_valide:
        return 0.0
    
    hv = 0.0
    previous_f1 = front_valide[0][0] 
    
    # Calcul par la méthode des rectangles
    # On commence par le rectangle formé par le premier point et le plafond (ref_y)
    hv += (point_ref[0] - previous_f1) * (point_ref[1] - front_valide[0][1])
    
    # Ensuite on ajoute les rectangles formés par les différences
    for i in range(1, len(front_valide)):
        current_f1 = front_valide[i][0]
        current_f2 = front_valide[i][1]
        
        prev_f1 = front_valide[i-1][0]
        prev_f2 = front_valide[i-1][1]
        
        # On ajoute la zone "gagnée" par le nouveau point
        # Attention: dans un front trié par f1 croissant, f2 est décroissant.
        # Le calcul exact dépend de la géométrie, voici la méthode standard "Lebesgue measure"
        # Simplifié : Somme des (Largeur * Hauteur) depuis le point ref
        pass 
        
    # MÉTHODE SIMPLIFIÉE FIABLE (Rectangle slicing)
    # On part du point de référence en haut à droite
    # On somme les aires (x_suiv - x_courant) * (ref_y - y_courant)
    area = 0.0
    # Ajoutons un point fictif au début correspondant à l'axe vertical du premier point
    # Trier par f1 croissant
    sorted_front = sorted(front_valide, key=lambda x: x[0])
    
    max_y = point_ref[1]
    
    for i in range(len(sorted_front)):
        p = sorted_front[i]
        # Largeur : distance jusqu'au prochain point (ou point ref si c'est le dernier)
        if i < len(sorted_front) - 1:
            width = sorted_front[i+1][0] - p[0]
        else:
            width = point_ref[0] - p[0]
            
        # Hauteur : distance entre le point et la référence Y
        height = point_ref[1] - p[1]
        
        area += width * height
        
    return area