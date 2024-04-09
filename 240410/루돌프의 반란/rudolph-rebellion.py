def is_inrange(x,y):
    return 0<=x<n and 0<=y<n

#def 루돌프 이동
def rudolf_move():
    global rr, rc
    global santa_info

    direction = -1 
    idx = -1 
    min_dist = 999999
    short_x, short_y = -1, -1 

    for i in range(p) : #가장 가까운 산타를 찾는다 
        x,y = santa_info[i] #산타의 x,y 좌표 
        if not is_inrange(x,y): #산타가 좌표 밖에 있으면(탈락한 산타라면) 선택하지 않는다
            continue
        if (rr-x)**2 + (rc-y)**2 < min_dist : #산타와의 거리를 계산한다 
            short_x, short_y = x, y #가장가까운 산타 좌표 업데이트
            min_dist = (rr-x)**2 + (rc-y)**2 #가장가까운 산타 거리 업데이트 
            idx = i #가장 가까운 산타 인덱스 업데이트
        elif (rr-x)**2 + (rc-y)**2 == min_dist :#가까운 거리가 2개 이상이라면
            if x > short_x : #r좌표가 큰 산타를 선택한다 
                short_x, short_y = x, y 
                idx = i 
            elif x == short_x : #r좌표가 큰 산타가 2명 이상
                if y > short_y : #c좌표가 큰 산타를 선택한다 
                    short_x, short_y = x, y 
                    idx = i 
                    
    
    #print('선택한 산타좌표')
    #print(short_x, short_y)

    move_min = 99999
    temp_x, temp_y = -1, -1 
    #인접한 8방향 중 하나로 가까워지는 방향으로 돌진한다
    #상, 우, 하, 좌, 우하, 좌상, 좌하, 우상 
    dx, dy = [-1,0,1,0,1,-1,1,-1], [0,1,0,-1,1,-1,-1,1]
    for dir in range(8): 
        nx, ny = rr+dx[dir], rc+dy[dir]
        if not is_inrange(nx,ny): #격자 밖으로 빠져나간다면 선택하지 않는다
            continue
        if (nx-short_x)**2 + (ny-short_y)**2 < move_min : 
            temp_x, temp_y = nx, ny 
            move_min = (nx-short_x)**2 + (ny-short_y)**2
            direction = dir
    
    #print('direction:', direction )
    #print('루돌프 이동좌표')
    #print(temp_x, temp_y)

    rr, rc = temp_x, temp_y #루돌프 좌표 업데이트

    #충돌 
    if (rr, rc) == (short_x, short_y) : 
        crush('rudolf', idx, direction)




#def 산타이동
def santa_move(): 
    global santa_info

    direction = -1 
    for i in range(p): #1번부터 P번까지 순서대로 움직임 
        if fail[i] == 1: #이미 탈락한 산타는 움직일 수 없음
            continue 
        if k < kijul[i] : #기절한 산타는 움직일 수 없음 
            continue 
        
        
        sx,sy = santa_info[i]
        #print(i+1, '번 산타 현재 위치')
        #print(santa_info[i])

        cur_dist = (sx-rr)**2 + (sy-rc)**2 #현재 거리 : 산타 거리와 루돌프의 거리
        temp_x, temp_y = sx,sy #임시 산타 좌표
        dx, dy = [-1,0,1,0], [0,1,0,-1]
        for j in range(4): 
            nx, ny = sx+dx[j], sy+dy[j]
            if not is_inrange(nx,ny): continue #게임판 밖으로 움직일 수 없다 
            if (nx,ny) in santa_info : continue #다른 산타가 있는 칸으로 움직일 수 없다 : 이게 안됐음.. 

            if (nx-rr)**2 + (ny-rc)**2 < cur_dist : #거리가 가까워지는 방향으로 상우하좌 우선순위로 1칸 이동, 가까워지지 않는다거나 움직일 수 없으면 이동X, 
                temp_x, temp_y = nx, ny #임시 산타 좌표를 업데이트 
                cur_dist = (nx-rr)**2 + (ny-rc)**2 #현재 최단 거리를 업데이트
                direction = j 
        santa_info[i] = (temp_x, temp_y) #4방향 탐색후, 최종 산타 좌표를 업데이트 

        #print(i+1, '번 산타이동좌표')
        #print(santa_info[i])

        if (rr, rc) == santa_info[i] : 
            crush('santa', i, direction)



            

    
#def 충돌 
def crush(who, idx, direction): 
    global santa_info
    global fail 
    #who : 누가 들이댓는ㄱ 
    #idx : 어떤 산타와 충돌했는가 
    #direction : 어느 방향으로 왔는가 

    #상, 우, 하, 좌, 우하, 좌상, 좌하, 우상 
    #하, 좌, 상, 우, 좌상, 우하, 우상, 좌하 
    

    x, y = santa_info[idx]

    if who == 'rudolf': 
        dx, dy = [-1,0,1,0,1,-1,1,-1], [0,1,0,-1,1,-1,-1,1]
        scores[idx] += c
        nx = x + dx[direction]*c 
        ny = y + dy[direction]*c #산타는 이동해온 방향으로 C만큼 밀려난다
        
    
    elif who == 'santa':
        dx, dy = [1,0,-1,0,-1,1,-1,1], [0,-1,0,1,-1,1,1,-1]
        scores[idx] += d #해당 산타는 D만큼의 점수를 얻게 된다 
        nx = x + dx[direction]*d
        ny = y + dy[direction]*d #산타는 자신이 이동해온 반대 방향으로 D만큼 밀려나게 된다(정확히 원하는 위치에)
    #print(scores)
    #산타는 루돌프와의 충돌후 기절을 한다. k+2번째 턴부터 정상상태가 된다
    kijul[idx] = k+2

    #밀려난 위치가 게임판 밖이라면 산타는 게임에서 탈락된다 
    if not is_inrange(nx,ny): 
        fail[idx] = 1 #탈락 정보 업데이트 
        santa_info[idx] = (-1,-1) #산타 정보 업데이트 
    else : 
        santa_info[idx] = (nx,ny) #산타 정보 업데이트 
        chain = [idx]
        recur(nx,ny, dx, dy,direction, chain)





def recur(nx,ny, dx, dy,direction, chain):
    #밀려난 칸에 다른 산타가 있으면 상호작용이 발생한다
    #다른 산타는 1칸 해당 방향으로 밀려난다
    #다른 산타가 있다면 연쇄적으로 1칸씩 밀려난다
    #게임판 밖으로 밀려나오면 게임에서 탈락된다   
    for i in range(p): 
        if i in chain : #나를 다른 산타로 착각하는경우 ^^; 패쓰 -> 이미 연쇄 작용이 일어난 산타의 경우 패쓰
            continue 
        sx, sy = santa_info[i]
        if (nx,ny) == (sx, sy) : 
            nx, ny = sx+dx[direction], sy+dy[direction]
            #밀려난 칸에 다른 산타가 있으면 연쇄적으로 처리(탈락여부 , 좌표)
            if not is_inrange(nx, ny): 
                santa_info[i] = (-1,-1)
                fail[i] = 1 
                return 
            else : 
                santa_info[i] = nx,ny
                chain.append(i)
                recur(nx,ny,dx,dy,direction,chain) 
    return 


        



#입출력
from collections import deque
from copy import deepcopy


if __name__ == "__main__" :
    n, m, p, c, d = map(int,input().split())

    rr,rc = map(int,input().split())
    rr, rc = rr-1, rc-1 

    santa_info = [[] for _ in range(p)] #나중에 탈락한 산타 좌표 처리해줘야함(-1,-1) 

    for i in range(p): 
        pn,sr,sc = map(int,input().split())
        santa_info[pn-1] = (sr-1,sc-1)


    #새로운 변수, 리스트 
    fail = [0 for _ in range(p)] #산타 탈락 여부 
    scores = [0 for _ in range(p)] #산타 점수 
    kijul = [0 for _ in range(p)] #산타 기절 여부

    #m번의 판 동안 
    for k in range(m): 

        #0. 모든 산타가 탈락하면 break 
        if sum(fail) == p : 
            break 
        #1. 루돌프 이동
        rudolf_move()
        #2. 산타 이동   
        santa_move()
        #3. 탈락하지 않은 산타에게 +1점 부여
        for i in range(p): 
            if fail[i] == 0 :
                scores[i] += 1  
    
print(*scores)