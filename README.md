# Python-vending-machine
Client/ Server-side software system built in Python to manage a vending machine system. 
Items inventory is stored in an .csv file, containing item ID, description, price per unit and available quantity.
The client uses tkinter library to create the Vending Machine GUI and all items will be univocally identified keeping track
of their physical address stored in memory at the time of execution.
If the checkout is successful, the database will receive the updates and a .txt file will keep track of every purchase (including cancelled transaction).
