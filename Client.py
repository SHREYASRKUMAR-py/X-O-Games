clientSocket,clientAddress = None,None

start = False
user = False
player2 = ""
board = None
pos = 0
finish = False

def createThread(con):
    thread = threading.Thread(target=con)
    thread.daemon = True
    thread.start()

def receive():
    global start,user,player2,board
    while True:     
        if start and not user:
            try:
                data,addr = clientSocket.recvfrom(1024)
                name = data.decode()
                print(data)
                board = gb.Board(name)
                player2 = name
                sendData = '{}'.format("player1").encode()
                clientSocket.send(sendData)
                user = True
            except:
                pass

def receiveMove():
    global pos,start
    while True:
        if start and user:
            try:
                data,addr = clientSocket.recvfrom(1024)
                data = data.decode()
                print(data)
                if data == "Play Again":              
                    reset()
                elif data == "Fun Times":               
                    gameOver()                         
                else:
                    pos,board.lastMove = data.split("-")
                    board.playMoveOnBoard(int(pos),board.lastMove)
                    updateBoard()
                    lblTurn["text"] = "You"
                    play()
            except:
                pass

def acceptConnection():
    print("Thread created")
    global clientSocket,clientAddress,start
    clientSocket,clientAddress = serverSocket.accept()
    message = "Incoming play request from "+str(clientAddress)+" client?"
    answer = messagebox.askyesno("Question",message)
    if answer:
        sendData = '{}'.format("accepted").encode()
        clientSocket.send(sendData)
        start = True
        reset()
        resetStat()
        print(sendData)
        print("Client connected from: ",clientAddress)
        receive()
    else:
        sendData = '{}'.format("Not accepted").encode()
        clientSocket.send(sendData)
        clientSocket.close()
        print("Client socket closes")
def clickQuit():
    if start or user:
        serverSocket.close()
    window.destroy()
