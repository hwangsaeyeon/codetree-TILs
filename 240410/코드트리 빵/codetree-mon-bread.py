import sys
from collections import deque


def is_inrange(x,y):
    return 0<=x<n and 0<=y<n

#def move_to_convenient():
#def arrive_convenient():

def move_to_basecamp(start_x, start_y):
    q = deque()
    q.append((start_x, start_y,0))
    depth = [[0 for _ in range(n)] for _ in range(n)]
    visited = [[False for _ in range(n)] for _ in range(n)]
    visited[start_x][start_y] = True

    dx, dy = [-1, 0, 0, 1], [0, -1, 1, 0]

    while q:
        x, y, d = q.popleft()

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if not is_inrange(nx, ny): continue  # 좌표 밖으로 넘어가면
            if visited[nx][ny]: continue  # 최단거리가 아니면

            # !!지나갈 수 없는 편의점이나 지나갈 수 없는 베이스캠프가 있다면 continue!!
            if (nx, ny) in arrived_store:
                continue
            if (nx, ny) in arrived_basecamp:
                continue

            depth[nx][ny] = d+1

            q.append((nx, ny,d+1))
            visited[nx][ny] = True

    min_depth = 300
    mx, my = -1,-1
    for i in range(n):
        for j in range(n): #행, 열이 작은 것이 우선 순위

            if arr[i][j] == 1 : #베이스캠프의 위치에 도달
                if depth[i][j] < min_depth : #베이스캠프까지의 거리 중 더 작은 깊이라면
                    min_depth = depth[i][j] #갱신한다
                    mx, my = i,j #이동할 베이스캠프의 좌표도 갱신한다


    return mx,my

    #return mx,my 는 튜플로 return 됨


def bfs(start_x, start_y, target_x, target_y):
    q = deque()
    q.append((start_x,start_y))
    visited = [[False for _ in range(n)] for  _ in range(n)]
    visited[start_x][start_y] = True
    dx,dy = [-1,0,0,1], [0,-1,1,0]
    to_x, to_y = (-1,-1) #1칸 이동하려하는 좌표

    history_x = [[-1 for _ in range(n)] for _ in range(n)]
    history_y = [[-1 for _ in range(n)] for _ in range(n)]
    history_x[start_x][start_y] = start_x
    history_y[start_x][start_y] = start_y
    history = []

    while q :
        x,y = q.popleft()
        if (x,y) == (target_x, target_y): #편의점으로의 최단거리에 도달하였으면
            #경로를 역추척해서 1칸 이동 했을 시의 좌표를 구한다
            hx = history_x[x][y]
            hy = history_y[x][y]

            if (hx,hy) == (start_x, start_y) :
                return [target_x, target_y]

            while (hx,hy) != (start_x,start_y) :
                history.append((hx,hy))

                tempx = history_x[hx][hy]
                tempy = history_y[hx][hy]

                hx, hy = tempx, tempy
            return history[-1] #딱 1칸 이동했을 때의 좌표

        for i in range(4):
            nx,ny = x+dx[i], y+dy[i]
            if not is_inrange(nx,ny): continue #좌표 밖으로 넘어가면
            if visited[nx][ny] : continue #최단거리가 아니면

            #!!지나갈 수 없는 편의점이나 지나갈 수 없는 베이스캠프가 있다면 continue!!
            if (nx,ny) in arrived_store :
                continue
            if (nx,ny) in arrived_basecamp :
                continue


            history_x[nx][ny] = x
            history_y[nx][ny] = y
            q.append((nx,ny))
            visited[nx][ny] = True








n, m = map(int,input().split())
arr = []
for i in range(n):
    arr.append(list(map(int,input().split())))


#베이스캠프의 pos를 받는다
basecamp_pos = []
for i in range(n):
    for j in range(n):
        if arr[i][j] == 1 :
            basecamp_pos.append((i,j))



#나중에 디버깅요소가 될거같은 쎄한느낌
#people_pos = [[(-1,-1)] for _ in range(m)] 
#people_pos = [[] for _ in range(m)]  #처음에는 격자 밖에 나와있다
x_pos = [-1 for _ in range(m)]
y_pos = [-1 for _ in range(m)]


arrived = [False for _ in range(m)]
arrived_store = []
arrived_basecamp = []

#------



convenient_pos = [[] for _ in range(m)] #편의점 위치
for i in range(m):
    x,y = map(int,input().split()) #사람 0번부터 m-1번까지 설정
    convenient_pos[i] = x-1, y-1 #인덱스 0번부터 n-1번까지로 재설정

t=0 #1분부터 시작
while True :
    #0. 모든 사람이 편의점에 도착한다면 시간을 출력하고 중단한다
    #=============================================
    cnt = 0
    for i in range(m):
        if arrived[i] :
            cnt += 1

    if cnt == m :
        print(t)
        break
    
    t+=1 #이걸안해서 막히다니...

    #=============================================
    
    #1분동안 순서대로 진행한다

    #1. 격자에 있는 사람이 있으면, 편의점을 향해 1칸 이동한다
    #=============================================
    for i in range(m):
        if arrived[i] == True : #편의점에 도착한 사람이라면 움직이지 않는다
            continue
        px, py = x_pos[i], y_pos[i]
        cx, cy = convenient_pos[i]
        if is_inrange(px,py): #격자에 사람이 있으면
            move_pos = bfs(px,py,cx,cy) #편의점을 향해 1칸 이동한다
            mx,my = move_pos
            x_pos[i], y_pos[i] = mx,my
           

    #여기서 people pos를 업데이트한다
    #격자에 있는 사람이 모두 이동하였다
    #=============================================




    #2. 편의점에 도착하면? 멈춘다
    for i in range(m):
        if arrived[i]:
            continue

        if (x_pos[i], y_pos[i]) == convenient_pos[i] :
            arrived_store.append((convenient_pos[i])) #해당 편의점으로 이동할 수 없다
            arrived[i] = True #앞으로 i번 사람은 이동하지 않아도 된다
            

    #=============================================

    #3. 현재시간이 t<=m을 만족하면 t번 사람은 가까운 베이스캠프로 이동한다
    #t는 1번부터 시작하고 m은 0번부터 시작하기 때문에 m+1(=t)번 사람이 가까운 베이스 캠프로 이동한다
    #=============================================

    if t <= m :
        
        #t-1 번 사람이 가까운 베이스캠프로 이동한다
        #bx, by = x_pos[t-1],y_pos[t-1]  #bx,by 이동할 사람의 좌표
        bx, by = convenient_pos[t-1] #가고싶은 편의점 좌표
        mx,my = move_to_basecamp(bx,by) #mx,my 이동할 베이스캠프의 좌표
        
        #사람 위치 업데이트
        
        x_pos[t-1],y_pos[t-1] = mx,my 
        #해당 베이스캠프는 이동할 수 없다
        arrived_basecamp.append((mx,my))