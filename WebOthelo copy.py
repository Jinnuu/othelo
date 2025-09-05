# Othelo(Reverse) Game with Web UI (CSS, HTML, FLASK)
# This is practice for implement my ablility of fundumental programming 

from flask import Flask, request, redirect, render_template

app=Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    global board
    global player
    global turn
    global p
    
    if(request.method=="POST"):
        temp=request.form.get("cell").split(',')
        print(temp)
        x=int(temp[0])
        y=int(temp[1])
        if(board[x][y]==0):
            turn+=1
            
        my_turn([x,y])
        for i in range(0,8,1):
            for j in range(0,8,1):
                print(board[i][j], end=' ')
            print()
        if(turn>=60):
            return redirect('/end')
        else: return redirect('/')

    return render_template('index.html', board=board,player=player[p])

# player (1 or -1)
# location (list: [0:8][0:8])

def my_turn(location):
    global board
    global turn
    global player
    global p
    
    x=int(location[0])
    y=int(location[1])
    
    if(board[x][y]==0):
        board[x][y]=player[p]
        ok=False
        i=0
        dir=[[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]]
        route=[0,0,0,0,0,0,0,0]
        ok=[0,0,0,0,0,0,0,0]
        for i in range(0,8,1):
            tx=dir[i][0]
            ty=dir[i][1]
            for j in range(1,8,1):
                if(0<=x+tx*j<8 and 0<=y+ty*j<8):
                    if(board[x+tx*j][y+ty*j]==0):
                        route[i]=-1
                        continue
                    elif(board[x+tx*j][y+ty*j]==player[(p+1)%2]):
                        if(route[i]==0):
                            route[i]=1
                        elif(route[i]==1):
                            continue
                        else:
                            break
                    elif(board[x+tx*j][y+ty*j]==player[p]):
                        if(route[i]==1):
                            ok[i]=1
                        else:
                            break
                print(route)
                print(ok)
        for k in range(0,8,1):
            tx=dir[k][0]
            ty=dir[k][1]
            if(ok[k]==1):
                for r in range(1,8,1):
                    if(board[x+tx*r][y+ty*r]==player[p]):
                        break
                    elif(board[x+tx*r][y+ty*r]==player[(p+1)%2]):
                        board[x+tx*r][y+ty*r]=player[p]
                    else:
                        print('Something is wrong')

        p=(p+1)%2
            
def board_set():
    global board
    global turn
    global player
    global p
    for i in range(0,8,1):
        temp=[]
        for j in range(0,8,1):
            temp.append(0)
        board.append(temp)
    board[3][3]=board[4][4]=1
    board[3][4]=board[4][3]=-1

board=[]
turn=0
player=[1,-1]
p=0
board_set()

if __name__=="__main__":
    app.run(port=5000, debug=True)