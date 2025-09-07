from flask import Flask, request, flash, redirect, render_template
import pymysql

board=[]
turn=0
player=[1,-1]
p=0

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



app=Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method=='GET'):
        return redirect('/login')
    else:
        id=request.form.get('id')
        password=request.form.get('password')
        string=request.form.get('id')+request.form.get('password')
        connection=pymysql.connect(host='127.0.0.1', user="root", password='jin664255@', db='othelo', charset='utf8')
        cursor=connection.cursor()
        cursor.execute('select * from users where id=%s', (id))
        rows=cursor.fetchall()
        for row in rows:
            print(row)
        return redirect('/game')

@app.route('/game', methods=['POST', 'GET'])
def game():
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
        else:
            return redirect('/game')
    else:
        board_set()
    return render_template('index.html', board=board,player=player[p])

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if(request.method=='GET'):
        return render_template('register.html')
    else:
        nickname=request.form.get('nickname')
        id=request.form.get('id')
        password=request.form.get('password')
        re_password=request.form.get('re_password')
        if(re_password!=password):
            return redirect('/register')
        else:
            connection=pymysql.connect(host="127.0.0.1", user="root", password="jin664255@", db="othelo", charset="utf8")
            cursor=connection.cursor()
            cursor.execute('insert into users values(%s,%s,%s,0)', (id, password, nickname))
            connection.commit()
            connection.close()
            return redirect('/login')

@app.route('/end')
def end():
    global board
    player1_cnt=0;
    player2_cnt=0
    winner=''
    for i in range(0,8,1):
        for j in range(0,8,1):
            if(board[i][j]==player[1]):
                player1_cnt+=1
            else:
                player2_cnt+=1
    if(player1_cnt>player2_cnt):
        winner='player 1(O)'
    else:
        winner='player 2(X)'
    
    return f''''
        <DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                승자는 {winner}입니다. 
            </body>
        </html>
'''

if __name__=="__main__":
    board_set()
    app.run(port=5000, debug=True)
    