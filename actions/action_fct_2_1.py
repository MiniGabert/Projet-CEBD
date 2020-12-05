import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction fournie 1
class AppFct2_1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_2_1.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_2_1, "")
        try:
            cursor = self.data.cursor()
            querry = """
                    SELECT eq.numEq, avg(ageSp)
                    FROM LesEquipes eq 
                    JOIN LesEquipiers  e on e.numEq = eq.numEq
                    JOIN view_LesSportifs s on s.numSp = e.numSp
                    WHERE eq.numEq IN (
                        SELECT eq.numEq
                        FROM LesEquipes eq  
                        JOIN LesInscriptions i on i.numIn = eq.numEq 
                        JOIN LesResultats r on r.numEp = i.numEp and r.gold = i.numIn 
                        GROUP BY eq.numEq)
                    GROUP BY eq.numEq
                   """
            result = cursor.execute(querry)

        except Exception as e:
            self.ui.table_fct_2_1.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_2_1, "Impossible : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_2_1, result)