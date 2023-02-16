import socket
import csv
import pickle

#SERVER DETAILS

HOST = 'localhost'
PORT = 9999

#GETTING STOCK INFORMATION
with open('database_items.csv', 'r') as file:   #WILL OPEN FILE CONTAINING THE STOCK AND WILL SAVE IT IN A MATRIX
    reader = csv.reader(file)
    mat = []
    for i in reader:                    
        mat.append(i)
        mat += []
        
#PRINT STOCK AVAILABLE
print("STOCK AVAILABLE")       
for a in mat:
    print(a)


#CREATE SOCKET

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#OPEN CONNECTION

server_socket.bind((HOST, PORT))


#WAIT FOR CLIENT CONNECTION

server_socket.listen(1)


#ACCEPT CONNECTION

client_socket,(host, port) = server_socket.accept()

print(f"Connection from {host} from port {port}")

#RECEIVES PURCHASE REQUEST

while True:   #THE CLIENT-SERVER CONNECTION WILL HAPPEN SEVERAL TIMES, TILL THE CLIENT WILL CLOSE THE CONNECTION
    
        
    received_data = client_socket.recv(1024)   #RECEIVES PURCHASE REQUEST MESSAGE FROM CLIENT
    print(received_data.decode("utf-8"))


    #SERVER SENDS AVAILABLE STOCK

    data=pickle.dumps(mat)    #CONVERTS THE MATRIX WITH STOCK IN BIT

    client_socket.send(data)    #SEND BITS TO CLIENT

    #SERVER RECEIVES UPDATE

    receive_update = client_socket.recv(4096)  #RECEIVES UPDATED STOCK FROM CLIENT

    upd_stock = pickle.loads(receive_update)  #DECODE DATA
    
    mat= upd_stock   #UPDATE MATRIX CONTAINING THE STOCK
    
    for s in upd_stock: #PRINT OUT UPDATED STOCK
        print(s)

    with open('database_items.csv', 'w', newline='') as update_file:  #UPDATE CSV FILE CONTAINING STOCK
        writer = csv.writer(update_file)
        for w in upd_stock:
            writer.writerow(w)
    

    
    receive_rec = client_socket.recv(4096)   #RECEIVE AND DECODE TRANSACTION RECORD (PURCHASED OR CANCELLED)
    record_transaction = pickle.loads(receive_rec)
    if record_transaction == 'CONNECTION TERMINATED':  #IF RECEIVES 'CONNECTION TERMINATED', MEANS THAT CLIENT HAS CLOSE THE CONNECTION, EXIT FROM THE LOOP
        print(record_transaction)
        break
    else:
        print(record_transaction)
        with open('transaction.txt', 'a') as tr_rec:
            tr_rec.write(record_transaction)
            tr_rec.write('\n')


    #CLOSES CONNECTION

client_socket.close()   #CLOSES CONNECTION
