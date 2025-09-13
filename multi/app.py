from flask import Flask, request, flash, redirect, render_template
import time
import json
import pymysql
app=Flask(__name__)


def my_turn(location, board, turn, p):

    player=[1,-1]

    
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
    return board, turn, p
   

def board_set():
    board=[]
    turn=0
    p=0
    for i in range(0,8,1):
        temp=[]
        for j in range(0,8,1):
            temp.append(0)
        board.append(temp)
    board[3][3]=board[4][4]=1
    board[3][4]=board[4][3]=-1
    return board,turn, p

def count_score(board):
    player1_score=0
    player2_score=0
    for i in range(8):
        for j in range(8):
            if(board[i][j]==1):
                player1_score+=1
            elif(board[i][j]==-1):
                player2_score+=1
    return player1_score, player2_score
            


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
        return redirect('/game_mode/'+str(id))
    
@app.route('/game_mode/<string:player_id>', methods=['GET', 'POST'])
def game_mode(player_id):
    if(request.method=='GET'):
        return render_template('game_mode.html', player_id=player_id)

@app.route('/waiting/online/<string:player_id>', methods=['POST', 'GET'])
def waiting(player_id):
    connection=pymysql.connect(host='127.0.0.1', user='root', password='jin664255@', db='othelo', charset='utf8')
    cursor=connection.cursor()
    cursor.execute('select * from game where player1_id=%s or player2_id=%s', (player_id, player_id))
    row=cursor.fetchone()
    if(row):
        return redirect('/game/online/'+player_id+'/'+row[1]+'&'+row[2])
    else:
        cursor.execute('select * from waiting where player_id=%s', (player_id,))
        row=cursor.fetchone()
        if(cursor.rowcount>0):
            # waiting에서 대기 중이면 기다려
            cursor.execute('select * from waiting')
            rows=cursor.fetchall()
            if(cursor.rowcount<2):
                print(cursor.rowcount)
                return render_template('waiting.html', player_id=player_id, ok=False)
            else:
                print(rows)
                i=0
                players=[]
                for r in rows:
                    print('next: '+r[0])
                    players.append(r[0])
                    cursor.execute('delete from waiting where player_id=%s',(r[0],))
                    i=i+1
                board,turn,p=board_set()
                json_board=json.dumps(board)
                cursor.execute('insert into game(player1_id, player2_id, player1_score, player2_score, turn, p, board, is_over) values(%s, %s,%s, %s, %s,%s,%s, True)', (players[0], players[1], 2,2,turn,p,json_board))
                connection.commit()
                connection.close()
                return redirect('/game/online/'+player_id+'/'+players[0]+'&'+players[1])
        else:
            cursor.execute('insert into waiting values(%s, %s, now())', (player_id, 0))
            connection.commit()
            connection.close()
            return render_template('waiting.html', player_id=player_id, ok=False)
    
    # if(ok<5):
    #     ok=ok+1
    #     # print(ok)
    #     return render_template('waiting.html', player_id=player_id, ok=ok)
    # else:
    #     return redirect('/game/online/'+player_id)
@app.route('/waiting2/online/<string:player_id>')
def waiting2(player_id):
    connection=pymysql.connect(host='127.0.0.1', user='root', password='jin664255@', db='othelo', charset='utf8')
    cursor=connection.cursor()
    cursor.execute('select * from game where player1_id=%s or player2_id=%s', (player_id, player_id))
    row=cursor.fetchone()
    if(row):
        return redirect('/game/online/'+player_id+'/'+row[1]+'&'+row[2])
    else:
        cursor.execute('select * from waiting where player_id=%s', (player_id,))
        row=cursor.fetchone()
        if(cursor.rowcount>0):
            # waiting에서 대기 중이면 기다려
            cursor.execute('select * from waiting')
            rows=cursor.fetchall()
            if(cursor.rowcount<2):
                print(cursor.rowcount)
                return render_template('waiting2.html', player_id=player_id, ok=False)
            else:
                print(rows)
                i=0
                players=[]
                for r in rows:
                    print('next: '+r[0])
                    players.append(r[0])
                    cursor.execute('delete from waiting where player_id=%s',(r[0],))
                    i=i+1
                board,turn,p=board_set()
                json_board=json.dumps(board)
                cursor.execute('insert into game(player1_id, player2_id, player1_score, player2_score, turn, p, board, is_over) values(%s, %s,%s, %s, %s,%s,%s, False)', (players[0], players[1], 2,2,turn,p,json_board))
                connection.commit()
                connection.close()
                return redirect('/game/online/'+player_id+'/'+players[0]+'&'+players[1])
        else:
            cursor.execute('insert into waiting values(%s, %s, now())', (player_id, 0))
            connection.commit()
            connection.close()
            return render_template('waiting2.html', player_id=player_id, ok=False)

@app.route('/game/<string:game_mode>/<string:player_id>/<string:player1_id>&<string:player2_id>', methods=['POST', 'GET'])
def game(game_mode,player_id, player1_id,player2_id):

    player=[1,-1]

    connection=pymysql.connect(host='127.0.0.1', user='root', password='jin664255@', db='othelo', charset='utf8')
    cursor=connection.cursor()
    cursor.execute('select * from game where player1_id=%s or player1_id=%s', (player1_id,player2_id))
    
    players=[]
    players.append(player1_id)
    players.append(player2_id)
    
    if(request.method=="POST"):

        row=cursor.fetchone()
        game_id=row[0]
        player1_score=row[3]
        player2_score=row[4]
        turn=row[5]
        p=row[6]
        board=json.loads(row[7])
        print(row)
            
        temp=request.form.get("cell").split(',')
        print(temp)
        x=int(temp[0])
        y=int(temp[1])
        if(board[x][y]==0):
            turn+=1
            
        board,turn,p=my_turn([x,y], board,turn,p)
        for i in range(0,8,1):
            for j in range(0,8,1):
                print(board[i][j], end=' ')
            print()
        if(turn>=60):
            cursor.execute('update game set player1_score=%s, player2_score=%s, turn=%s, p=%s, board=%s where game_id=%s', (player1_score,player2_score,turn,p,json.dumps(board), game_id))
            connection.commit()
            connection.close()
            return redirect('/end/'+str(game_id))
        else:
            player1_score, player2_score=count_score(board)
            cursor.execute('update game set player1_score=%s, player2_score=%s, turn=%s, p=%s, board=%s where game_id=%s', (player1_score,player2_score,turn,p,json.dumps(board), game_id))
            connection.commit()
            connection.close()
            return render_template('index.html', player_turn=players[p], game_mode=game_mode, player_id=player_id, player1_id=player1_id, player2_id=player2_id, board=board,player=player[p], player1_score=player1_score,player2_score=player2_score)
    else:
        board,turn,p=board_set()
        connection=pymysql.connect(host='127.0.0.1', user='root', password='jin664255@', db='othelo', charset='utf8')
        cursor=connection.cursor()
        if(game_mode=='online'):
            cursor.execute('select * from game where player1_id=%s or player1_id=%s', (player1_id,player2_id))
            row=cursor.fetchone()
            game_id=row[0]
            player1_score=row[3]
            player2_score=row[4]
            turn=row[5]
            p=row[6]
            board=json.loads(row[7])
        else:
            cursor.execute('insert into game(player1_id,player2_id,player1_score,player2_score,turn,p,board) values(%s, %s, 2,2,%s,%s,%s)', (player1_id,player2_id,turn,p,json.dumps(board)))
            connection.commit()
        cursor.close()
        
        return render_template('index.html', player_turn=players[p], game_mode=game_mode, player_id=player_id, player1_id=player1_id, player2_id=player2_id, board=board,player=player[p], player1_score=2,player2_score=2)

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

@app.route('/end/<string:game_id>')
def end(game_id):
    player1_cnt=0
    player2_cnt=0
    player=[1,-1]
    winner=''
    connection=pymysql.connect(host='127.0.0.1', user='root', password='jin664255@', db='othelo', charset='utf8')
    cursor=connection.cursor()
    cursor.execute('select * from game where game_id=%s', (game_id,))
    row=cursor.fetchone()
    board=json.loads(row[7])
    cursor.close()
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
    