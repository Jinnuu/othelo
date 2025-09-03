# Basic Othelo Game with console
# This is practice for implement my ablility of fundumental programming 

# player (1 or -1)
# location (list: [0:8][0:8])
def my_turn(player, location):
    global board
    x=int(location[0])
    y=int(location[1])
    board[x][y]=player
    for i in range(x+1,8,1):
        if(board[i][y]==player):
            for j in range(x+1,i,1):
                board[j][y]=player
            break
    for i in range(x-1,-1,-1):
        if(board[i][y]==player):
            for j in range(x-1,i,-1):
                board[j][y]=player
            break
    for i in range(y+1,1,8):
        if(board[x][i])==player:
            for j in range(y+1,i,1):
                board[x][j]=player
            break
    for i in range(y-1,-1,-1):
        if(board[x][i]==player):
            for j in range(y-1,i,-1):
                board[x][j]=player


def find_winner():
    global board
    player1=0 #  1
    player2=0 # -1
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j]==1:
                player1+=1
            else:
                player2+=1
    if player1>player2:
        return 1
    elif player1<player2:
        return -1
    else:
        return 0


board=[]

turn=0

#board set
for i in range(0,8,1):
    temp=[]
    for j in range(0,8,1):
        temp.append(0)
    board.append(temp)
board[3][3]=board[4][4]=1
board[3][4]=board[4][3]=-1



player=1
while(1):
    print("turn: "+str(player))
    for i in range(0,8):
        for j in range(0,8):
            print(board[i][j], end=' ')
        print('')
    site=input("자리를 입력하세요: ").strip().split(' ')
    if(board[int(site[0])][int(site[1])]!=0):
        print("해당 자리에 놓을 수 없습니다. ")
        continue

    my_turn(player, site)
    if(player==1):
        player=-1
    else:
        player=1
    
    if turn==60:
        print('game over')
        result=find_winner()