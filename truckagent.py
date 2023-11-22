import random
import copy

from globals import Global
from pade.core.agent import Agent
from PySide6.QtGui import QColor

class TruckAgent(Agent):
    def __init__(self,extra_parameter) -> None:
        self.n=extra_parameter #su posiciion
        self.S_inicial=random.randint(0,5)
        self.S_final=-1
        self.T_restante=-1
        self.mt_tiempo=copy.deepcopy(Global.mt_entre_ciudades)
        self.txt=""
        #0 que no saben la ficultad
        #-1 no pueden ir ahi
        self.mt_dificultad_que_saben_los_carros = [ 
            [-1,0,0,0],
            [0,-1,0,0],
            [0,0,-1,0],
            [0,0,0,-1]
        ]
        

    def elegir_ruta(self):
        #debe giarse del tiempo de dificultad y las tareas

        #temporalmente simular con dificultad global que sabe de todos
        self.mt_dificultad_que_saben_los_carros=Global.mt_dificultad
        for i in range(Global.n_ciudades):
            for j in range(Global.n_ciudades):
                if(i!=j):
                    self.mt_tiempo[i][j]=self.mt_dificultad_que_saben_los_carros[i][j]*Global.mt_entre_ciudades[i][j]
        
        #quitando las rutas que no necesita ir ya que no hay tareas ahi
        mt_eleccion_ruta_apartir_tiempo=copy.deepcopy(self.mt_tiempo)
        for i in range(Global.n_ciudades):
            for j in range(Global.n_ciudades):
                if(Global.mt_tareas[i][j]==0):
                    mt_eleccion_ruta_apartir_tiempo[i][j]=-1

        #busca si hay tareas apartir de la sede inicial donde esta
        posible_rutas_apartir_de_su_inicio=[]
        for i in range(Global.n_ciudades):
            if(mt_eleccion_ruta_apartir_tiempo[self.S_inicial][i]!=-1):
                posible_rutas_apartir_de_su_inicio.append([mt_eleccion_ruta_apartir_tiempo[self.S_inicial][i],i])

        #condicion en caso si haya
        if(posible_rutas_apartir_de_su_inicio):
            posible_rutas_apartir_de_su_inicio=sorted(posible_rutas_apartir_de_su_inicio)
            self.S_final=posible_rutas_apartir_de_su_inicio[0][1]
            self.T_restante=posible_rutas_apartir_de_su_inicio[0][0]
            Global.mt_tareas[self.S_inicial][self.S_final]-=1
        else:
            self.S_final=self.get_random_number(self.S_inicial,0,5)
            self.T_restante=self.mt_tiempo[self.S_inicial][self.S_final]

    def move(self):
        if all(all(valor == 0 for valor in fila) for fila in Global.mt_tareas): #cuando finaliza todo
            self.S_final=-1
            self.T_restante=-1
            self.txt=""
        else:
            if self.S_final==-1:
                self.elegir_ruta()
                self.txt=""
            else:
                self.T_restante-=1
                if(self.T_restante==0):
                    self.txt="Vehiculo "+str(self.n)+" culminó el envio de carga de '"+str(self.convertir_numero_a_sede(self.S_inicial))+ "' a '"+str(self.convertir_numero_a_sede(self.S_final))+"'."
                    self.S_inicial=copy.deepcopy(self.S_final)
                    self.S_final=-1

    def get_random_number(self,excluded_number, start_range, end_range):
        while True:
            random_number = random.randint(start_range, end_range)
            if random_number != excluded_number:
                return random_number
            
    def convertir_numero_a_sede(self,id):
        if(id==0):
            return "Lima"
        elif(id==1):
            return "Huanuco"
        elif(id==2):
            return "Ica"
        elif(id==3):
            return "Ayacucho"
        elif(id==4):
            return "Cusco"
        elif(id==5):
            return "Trujillo"



