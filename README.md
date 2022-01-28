# Victron_VoltToSoc
Stellt den SOC nach der Akkuspannung ein, wenn diese zu stark abweichen<br>
Grade bei kleinen Schwankungen im SOC von (z.B. von 35% auf 38% und dann wieder auf 35%) wich die Spannung immer weiter vom SOC ab.<br>
Daher konntrolliert das Programm ob der SOC noch größer als 32% ist aber die Spannung schon unter 52V - und setzt dann den SOC auf 30%.<br>
Auch mit dem Herrabsetzen der Akkuladeeffizens hab ich dies anders nicht in Griff bekommen ;(
