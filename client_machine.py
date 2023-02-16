import socket
import pickle
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


HOST = 'localhost'
PORT = 9999




total = 0   #KEEPS TRACK OF TOTAL  BASKET PRICE
basket = {}  #CONTAINS ITEMS SELECTED
rec_transaction=''  #TRANSACTION RECORD
btns_id= []     #KEEPS TRACK OF BUTTONS IDENTIFIERS


class Item:   #CREATES ITEM OBJECT
    def __init__(self,btn_id, item_id, name, price, quantity):
        self.btn_id= btn_id
        self.item_id = item_id
        self.name = name
        self.price = price
        self.quantity = quantity
        
    def print(self):  #PRINT ITEM DETAILS
        return f'{self.name}   £{self.price}   {self.quantity}'
        
    def buy(self):   #BUY ITEM
        self.quantity = int(self.quantity) - 1  #REDUCES ITEM QUANTITY 
        global total
        total += float(self.price)  #ADDS ITEM PRICE TO TOTAL
        
        self.btn_id.config(text=f"{self.name}   £{self.price}   {self.quantity}") #UDATES BUTTON INFO (QUANTITY) FOR THAT ITEM
        
        if self.name in basket:  #IF ITEM ADDED IS ALREADY IN BASKET, WILL INCREMENT ITS QUANTITY, OTHERWISE WILL CREATE A NEW ITEM IN THE BASKET
            basket[self.name] = int(basket[self.name]) + 1
        else:
            basket[self.name] = 1

        print(basket, total)  #PRINTS BASKET STATE AND TOTAL
        basket_label.config(text=f"BASKET:\n{basket}")  #UPDATES BASKET
        total_label.config(text=f"TOTAL: £{total}")   #UPDATES TOTAL

        if self.quantity == 0:  #IF QUANTITY IS 0, ITEM COULDN'T BE BOUGHT, THUS BUTTON WILL BE INACTIVE
            self.btn_id["state"] = DISABLED
    
        
            
def check_card(numb):  #CHECKS CARD NUMBER FORMAT
    if len(numb) == 16 and numb.isdigit()== True:
        return True
    else:
        return False

def check_cash(numb):  #CHECKS CASH FORMAT

    if len(numb)==0:
        return 0
    elif numb == '0' or numb == '0.':
        return 0
    elif numb[0] == '.':
        return 0
    else:
        for i in numb:
            if i != '.' and i.isdigit()==False:
                return 0
        
        

        
        
        
    


    
def checkout(): #PROCESS PURCHASE
    global total
    global rec_transaction
    if pay_met_click.get() == '':  #GIVES ERROR, IF PAYMENT OPTION IS NOT CHOSEN
        messagebox.showwarning("Warning", "NO PAYMENT METHOD SELECTED!")
        
    elif pay_met_click.get() == "CARD": #IF PAID BY CARD, WILL CHECK CARD NUMBER
        if check_card(pay_input.get()) == False:
            messagebox.showwarning("Warning", "INVALID CARD NUMBER!")
        else:
            for i in ava_stock:  #UPDATES THE STOCK MATRIX, SUBTRACTING ITEMS CHOSEN
                if i[1] in basket:
                    i[3] = int(i[3])-int(basket[i[1]])
            print(ava_stock)
            
            rec_transaction += f'{basket} TOTAL: £{total} CARD PAYMENT (N: {pay_input.get()}) PURCHASED'  #CREATES TRANSACTION REPORT
            messagebox.showinfo("ITEMS PURCHASED", f"{basket}\n MADE WITH CARD {pay_input.get()}")
            basket.clear()  #CLEAR BASKET FOR NEW POSSIBLE PURCHASE
            total = 0       #CLEAR TOTAL FOR NEW POSSIBLE PURCHASE
            basket_label.config(text=f"BASKET:\n{basket}")   #UPDATE BASKET LABEL
            total_label.config(text=f"TOTAL: £{total}")     #UPDATE TOTAL LABEL
            
            window.quit()     #CLOSES TKINTER WINDOW
            window.destroy()

    else:
        if check_cash(pay_input.get()) == 0:  #CHECKS CASH FORMAT
            messagebox.showwarning("Warning", "CASH FORMAT NOT VALID!")
        else:
           
            if total > float(pay_input.get()):   #IF CASH AMOUNT IS NOT ENOUGH, WILL GIVE ERROR
                messagebox.showwarning("Warning", "CASH NOT SUFFICENT")

            else:
                
                
            
                for i in ava_stock:  #UPDATES STOCK MATRIX, REMOVING ITEMS PURCHASED
                    if i[1] in basket:
                        i[3] = int(i[3])-int(basket[i[1]])
                print(ava_stock)
                
                change = format((float(pay_input.get()) - total), ".2f")  #CALCULATE CHANGE
                
                rec_transaction += f'{basket} TOTAL: £{total} CASH PAYMENT PAID: £{pay_input.get()} CHANGE: £{change} PURCHASED'  #TRANSACTION REPORT
                messagebox.showinfo("ITEMS PURCHASED", f"{basket}\n MADE WITH CASH \nAMOUNT: £{pay_input.get()} \nCHANGE: £{change}")
                basket.clear()   #CLEAR BASKET
                total = 0       #CLEAR TOTAL
                basket_label.config(text=f"BASKET:\n{basket}")  #UPDATE BASKET LABEL
                total_label.config(text=f"TOTAL: £{total}")    #UPDATE TOTAL LABEL
                
                window.quit()   #CLOSES TKINTER WINDOW
                window.destroy()





def cancel():  #CANCEL TRANSACTION
        global total
        global rec_transaction
        rec_transaction += f'{basket} TOTAL: £{total} CANCELLED'  #RECORD OF CANCELLED TRANSACTION
        basket.clear()   #CLEAR BASKET
        total = 0        #CLEAR TOTAL
        basket_label.config(text=f"BASKET:\n{basket}")  #UPDATE BASKET LABEL
        total_label.config(text=f"TOTAL: £{total}")    #UPDATE TOTAL LABEL
        window.quit()  #CLOSES TKINTER WINDOW
        window.destroy()
        

      
def exit_opt(): #IF CLOSE WINDOW IS PRESSES, IT WILL DO THIS FUNCTION 
    global flag
    flag = False
    window.quit()   
    window.destroy()



#CREATES CLIENT SOCKET
Client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#OPEN CONNECTION TO SERVER
Client_socket.connect((HOST, PORT))

flag = True

while flag == True:    #COMUNICATION CLIENT-SERVER IS INSIDE A LOOP, TILL FLAG IS TRUE
    #WINDOW CREATION AND SETTINGS

    window = Tk()  #CREATES TKINTER OBJECT

    window.geometry("500x560")   #DEFINE SIZE AND TITLE
    window.title("VENDING MACHINE")


    #BG IMAGE SETTINGS

    bg = PhotoImage(file="vend_img.gif")
    my_label = Label(window, image=bg)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    #SENDS MESSAGE TO SERVER

    message = "PURCHASE REQUEST..."
    Client_socket.send(bytes(message.encode('utf-8')))


    #CLIENT RECEIVES AVAILABLE STOCK FROM SERVER

    received_message =Client_socket.recv(4096)

    ava_stock = pickle.loads(received_message)

    lbl1 = ttk.Label(window, text="WELCOME TO OUR VENDING MACHINE!!!\nTHIS IS OUR AVAILABLE STOCK")
    lbl1.place(x=10, y=10)

    nx=10
    ny=30



    for i in ava_stock:   #CREATES A BUTTON FOR EVERY ITEM IN THE MATRIX RECEIVED
    
    
        btn = Button(window, width=20, height=1)
        btn.place(x=nx,y=ny)
        item = Item(btn, i[0], i[1],i[2], i[3])
        btn.config(text=f"{item.print()}", command=item.buy)
        if i[3] == '0':
            btn["state"]= DISABLED
        ny+=25
        if ny == 305:   #ITERATION USED TO PLACE THE BUTTONS IN A GOOD VIEW
            ny = 30
            nx += 150
        btns_id.append(btn)  #KEEPS TRACK OF BUTTONS IDENTIFIERS



    basket_label = ttk.Label(window, text=f"{basket}")  #CREATES BASKET LABEL
    basket_label.place(x=10, y=350)

    total_label = ttk.Label(window, text=f"TOTAL: {total}")  #CREATES TOTAL LABEL
    total_label.place(x=10, y=410)



    checkout_btn = Button(window, text="CHECKOUT", width=20, heigh=2, command=checkout)  #CREATES CHECKOUT BUTTON, LINKED TO CHECKOUT FUNCTION
    checkout_btn.place(x=10, y=490)

    cancel_btn = Button(window, text="CANCEL", width=20, heigh=2, command=cancel)  #CREATES CANCEL BUTTON, LINKED TO CANCEL FUNCTION
    cancel_btn.place(x=150, y=490)

    window.protocol("WM_DELETE_WINDOW", exit_opt)  #LIKS CLOSE WINDOW TO FUNCTION EXIT_OPT, WHICH WILL CHANGE THE STATE OF FLAG AND WILL FINISH THE LOOP


    lab_pay = ttk.Label(window, text="PAYMENT METHOD")  #PAYMENT METHOD LABEL
    lab_pay.place(x=10, y=430)


    pay_met = ["CASH","CARD"]  #CREATES DROPDOWN MENU FOR PAYMENT METHOD

    pay_met_click = StringVar()
    pay_met_click.set("")

    pay_choice = OptionMenu(window, pay_met_click, *pay_met)

    pay_choice.place(x=10, y=450)


    pay_input = StringVar()
    
    entry_pay = Entry(window, textvariable=pay_input)  #ENTRY BOX FOR CARD NUMBER OR CASH AMOUNT, DEPENDING ON PAYMENT METHOD
    entry_pay.place(x=150, y = 455)


    info_pay = ttk.Label(window, text="ENTER CARD NUMBER FOR CARD PAYMENT OR\n CASH AMOUNT FOR CASH PAYMENT")
    info_pay.place(x=150, y=415)
    mainloop()







    if flag == False:  #BEFORE EXIT FROM THE LOOP, CLIENT WILL SEND ACTUAL STOCK TO SERVER AND A MESSAGE 'CONNECTION TERMINATED' IN ORDER TO LET SERVER CLOSE ITS CONNECTION
        
        update_send = pickle.dumps(ava_stock)

        Client_socket.send(update_send)

        transaction_send = pickle.dumps('CONNECTION TERMINATED')

        Client_socket.send(transaction_send)
        rec_transaction=''
        


    else:




        update_send = pickle.dumps(ava_stock)  #SENDS UPDATED STOCK BACK TO SERVER

        Client_socket.send(update_send)



        transaction_send = pickle.dumps(rec_transaction)  #SEND TRANSACTION RECORD (PURCHASED OR CANCELLED)

        Client_socket.send(transaction_send)
        rec_transaction=''


    



Client_socket.close()   #CLOSES CONNECTION
