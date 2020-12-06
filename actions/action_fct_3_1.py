
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction 3.1
class AppFct3_1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_3_1.ui", self)
        self.data = data
        self.refreshCatList()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_3_1, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT LesEpreuves.numEp, gold, silver, bronze FROM LesEpreuves JOIN LesResultats WHERE nomDi = ? GROUP BY LesEpreuves.numEp",
                [self.ui.comboBox_fct_3_1_discipline.currentText()])
        except Exception as e:
            self.ui.table_fct_3_1.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_3_1, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_3_1, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_3_1, "Aucun résultat")

    # Fonction de mise à jour des catégories
    @pyqtSlot()
    def refreshCatList(self):

        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT nomDi FROM LesDisciplines")
        except Exception as e:
            self.ui.comboBox_fct_3_1_discipline.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_fct_3_1_discipline, result)
