import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction fournie 1
class AppFct2_2(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_2_2.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):

        display.refreshLabel(self.ui.label_fct_2_2, "")
        try:
            cursor = self.data.cursor()

            querry = """ 
                    WITH G as(
                        SELECT pays, sum(nbOr) as nbOr 
                        FROM (SELECT pays,count(gold) as nbOr 
                            FROM (
                                SELECT DISTINCT pays,gold 
                                FROM LesResultats 
                                JOIN LesEquipiers ON (gold = numEq) 
                                JOIN LesSportifs_base USING (numSP)
                                ) 
                            GROUP BY (gold)
                        
                            UNION ALL 
                            
                            SELECT pays,count(gold) as nbOr 
                            FROM LesResultats 
                            JOIN LesSportifs_base ON(gold = numSP) 
                            GROUP BY (gold)
                        )
                        GROUP BY(pays)
                    ),      
                                      
                    S as(
                        SELECT pays, sum(nbArgent) as nbArgent 
                        FROM (
                            SELECT pays,count(silver) as nbArgent 
                            FROM (
                                SELECT DISTINCT pays,silver 
                                FROM LesResultats 
                                JOIN LesEquipiers ON (silver = numEq) 
                                JOIN LesSportifs_base USING (numSP)) 
                                GROUP BY (silver)
                                UNION ALL 
                                SELECT pays,count(silver) as nbOr 
                                FROM LesResultats 
                                JOIN LesSportifs_base ON(silver = numSP) 
                                GROUP BY (silver)
                            )
                            GROUP BY(pays)
                        ),
                        
                    B as(
                        SELECT pays, sum(nbBronze) as nbBronze 
                        FROM (
                            SELECT pays,count(bronze) as nbBronze 
                            FROM (
                                SELECT DISTINCT pays,bronze 
                                FROM LesResultats 
                                JOIN LesEquipiers ON (bronze = numEq) 
                                JOIN LesSportifs_base USING (numSP)) 
                                GROUP BY (bronze)
                                UNION ALL 
                                SELECT pays,count(bronze) as nbOr 
                                FROM LesResultats 
                                JOIN LesSportifs_base ON(bronze = numSP) 
                                GROUP BY (bronze)
                                )
                            GROUP BY(pays)
                        ),
                        
                    S1 as(
                        SELECT * 
                        FROM pays 
                        LEFT JOIN G USING(pays)
                        ),
                    S2 as (
                        SELECT * 
                        FROM S1 
                        LEFT JOIN S USING(pays)
                    )
                    SELECT pays,ifnull(nbOr,0) ,ifnull(nbArgent,0), ifnull(nbBronze,0) 
                    FROM S2 LEFT 
                    JOIN B USING(pays) 
                    ORDER BY nbOr DESC, nbArgent DESC, nbBronze DESC
                    """
            result = cursor.execute(querry)

        except Exception as e:
            self.ui.table_fct_2_2.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_2_2, "Impossible d'afficher les résultats : " + repr(e))
        else:
            display.refreshGenericData(self.ui.table_fct_2_2, result)
