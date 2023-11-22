import random
class Global:
    num_trucks = 8
    n_ciudades = 6

    mt_tareas = [ [ (random.randint(1,2) if i>j else 0) for i in range(6) ] for j in range(6) ] 
    for i in range(n_ciudades):
      for j in range(n_ciudades):
        mt_tareas[j][i] = mt_tareas[i][j]

    #horas
    mt_entre_ciudades = [ [ (random.randint(5,10) if i>j else -1) for i in range(6) ] for j in range(6) ] 
    for i in range(n_ciudades):
      for j in range(n_ciudades):
        mt_entre_ciudades[j][i] = mt_entre_ciudades[i][j]

    #1 todo ok x1
    #2 medio mal x2
    #3 ta fregado x3
    mt_dificultad = [ [ (random.randint(1,3) if i>j else -1) for i in range(6) ] for j in range(6) ] 
    for i in range(n_ciudades):
      for j in range(n_ciudades):
        mt_dificultad[j][i] = mt_dificultad[i][j]
        
