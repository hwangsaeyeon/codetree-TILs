def is_inrange(x,y):
    return 0<=x<L and 0<=y<L

def damage(need_move): 
    damage_knight_list = need_move[1:] #첫번째 기사는 명령을 받은 기사이므로 제외 
    for i in damage_knight_list : 
        _,_,_,_,k = knight[i] 
        damage_cnt = 0 
        for j in range(len(knight_pos[i])) : #w×h 직사각형 내에 놓여 있는 함정의 수만큼만 피해를 입게됨
            x,y = knight_pos[i][j]
            #print(x,y)
            if board[x][y] == 1 : 
                damage_cnt += 1 

        if k <= damage_cnt : #현재 체력 이상의 데미지를 받을 경우 체스판에서 사라진다
            knight[i][-1] = 0 #현재 체력을 업데이트한다
            save[i] = False #죽었다고 표시
            for p in range(len(knight_pos[i])) : #체스판에서 사라지게 한다
                knight_pos[i][p] = (-1,-1)
            #print(i,'번 기사 체력')
            #print(knight[i][-1])
        else : 
            damage_val[i] += damage_cnt #데미지의 합계를 업데이트한다
            knight[i][-1] = k - damage_cnt #피해를 받은만큼 체력이 깎인다. 현재 체력을 업데이트 한다 
            #print(i,'번 기사 체력')
            #print(knight[i][-1])
    


def knight_move(idx, d): 
    #idx : 1번 기사 -> 0 으로 받는다 
    #d : 0,1,2,3 = 상,우,하,좌 

    dx, dy = [-1,0,1,0], [0,1,0,-1] #상우하좌

    if save[idx] == False: #체스판에서 사라진 기사에게 명령을 내리면 아무런 반응이 없다
        return 
    
    move, need_move = recur(idx,[idx])
    #print(move, need_move)
    if move : #연쇄적으로 모두 이동시킬 수 있다면 기사의 위치를 이동시킨다
        #print('이동시킬 수 있는 기사 리스트')
        #print(need_move)
        for i in need_move:
            for j in range(len(knight_pos[i])): 
                x, y = knight_pos[i][j]
                nx,ny = x+dx[d], y+dy[d]
                knight_pos[i][j] = nx,ny  
        #print('이동 후 기사 위치')
        #print(knight_pos)
        damage(need_move)
        #print('대미지 후 기사 위치')
        #print(knight_pos)

#그 기사도 함께 연쇄적으로 한칸 밀려난다
#그 옆에 또 기사가 있다면 연쇄적으로 한칸씩 밀린다


def real_move() : 
    dx, dy = [-1,0,1,0], [0,1,0,-1]




def recur(idx,need_move):  
    #print(need_move)
    dx, dy = [-1,0,1,0], [0,1,0,-1]
    move = True
    for i in range(len(knight_pos[idx])): #기사의 위치 순회
        x, y = knight_pos[idx][i] 
        #print('현재 좌표')
        #print(x,y)
        nx, ny = x+dx[d], y+dy[d] #첫번째 위치에서 이동 
        #print('이동 좌표')
        #print(nx,ny)
        if not is_inrange(nx,ny) : #이동하려는 방향이 범위를 벗어난다면 모든 기사는 이동할 수 없다
            move = False
            return move, need_move

        if board[nx][ny] == 2 : #이동하려는 방향의 끝에 벽이 있다면 모든 기사는 이동할 수 없다
            move = False
            return move, need_move
        
        for j in range(N): 
            if j in need_move : 
                continue 
            if (nx,ny) in knight_pos[j]: #이동하려는 칸에 다른 기사가 있다면
                #print('재귀시작')
                move, need_move = recur(j,need_move+[j]) #move, need_move 값을 받아와야한다
                #print(move, need_move)
            if not move:
                break 
        
        if not move: 
            break 
            
                
    return move, need_move
        
    

 
    





L, N, Q = map(int,input().split())

board = []
for i in range(L): 
    board.append(list(map(int,input().split())))
    

knight = []
knight_pos = [[] for _ in range(N)]

damage_val = [0 for _ in range(N)] 
save = [True for _ in range(N)]
for i in range(N): 
    r,c,h,w,k = map(int,input().split())
    knight.append([r-1,c-1,h,w,k])
    for rr in range(r-1, r+h-1): 
        for cc in range(c-1, c+w-1):
            knight_pos[i].append((rr,cc))

#print('기사 위치')
#print(knight_pos)


for i in range(Q): 
    #print(i+1,'번째 명령')
    index, d = map(int,input().split())
    knight_move(index-1, d) 
    #print(damage_val)


#생존한 기사의 총 데미지 합 출력
ans = 0 
for i in range(N):
    if save[i]: 
        ans += damage_val[i]
print(ans)