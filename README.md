# 3.it_inspector
Script per il controllo automatico (dalle 8:00 alle 23:00 ogni 30 min) della connessione rimanente con l'abbonamento 3. In caso il valore sia inferiore ad uno preimpostato (500MB) invia un email d'allerta. E' necessario essere connessi con la 3. L'unica versione funzionante è la selenium, che necessita Firefox.


Requisiti : 
* python 2.7
* Firefox
* [Selenium](http://selenium-python.readthedocs.org/installation.html)

Una volta eseguito lo script, ogni 30min tra le 8:00 e le 23:00, aprirà una finestra Firefox puntata all'indirizzo http://internet.tre.it, e se siete sotto rete 3, restituirà in console il valore attuale. Se queso è sotto la soglia _alarmValue_ verrà mandata un'email all'indirizzo impostato nello script.
