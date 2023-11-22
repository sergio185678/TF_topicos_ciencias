from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPaintEvent, QPainter,QPixmap,QFont
from PySide6.QtWidgets import QFrame


class Gui(QFrame):
    def __init__(self, agents) -> None:
        super(Gui, self).__init__()
        self.agents = agents
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, _: QPaintEvent) -> None:
        painter = QPainter(self)
        font = QFont()
        font.setBold(True)
        painter.setFont(font)

        self.fondo = QPixmap("fondo.png")
        self.fondo = self.fondo.scaled(700, 500)
        self.truck_img = QPixmap("truck.png")
        self.truck_img = self.truck_img.scaled(60, 30)
        painter.drawPixmap(0, 0, self.fondo)
        painter.setPen(Qt.red)
        painter.drawText(60, 30, "N°")
        painter.drawText(205, 30, "S_Inicio")
        painter.drawText(355, 30, "S_Final")
        painter.drawText(500, 30, "T_restante")

        painter.setPen(Qt.black)
        for agent in self.agents:
            painter.drawText(30, 30+agent.truck.n*50, str(agent.truck.n))
            painter.drawText(200, 30+agent.truck.n*50, self.convertir_numero_a_sede(agent.truck.S_inicial))
            if(agent.truck.S_final==-1):
                painter.drawText(350, 30+agent.truck.n*50, "-")
            else:
                painter.drawText(350, 30+agent.truck.n*50, self.convertir_numero_a_sede(agent.truck.S_final))
            
            if(agent.truck.T_restante==-1):
                painter.drawText(500, 30+agent.truck.n*50, "-")
            else:
                painter.drawText(520, 30+agent.truck.n*50, str(agent.truck.T_restante)+" H")

            painter.drawPixmap(50, 30-20+agent.truck.n*50, self.truck_img)

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
