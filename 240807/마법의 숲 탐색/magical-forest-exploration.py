from collections import deque
def is_inrange(x, y):
    return 0<=x<R and 0<=y<C

#해당 방향으로 이동할 수 있는지 check
def check(direction,x,y):
    if direction == 'south': #남쪽
        if x+2 <= R-1 : #가장 끝 지점만 살펴보도록, 격자를 벗어나는 경우 고려(수정)
            if arr[x+2][y] == 0 and arr[x+1][y+1] == 0 and arr[x+1][y-1] == 0 : #빈 공간인지 고려
                return True
    if direction == 'west': #서쪽
        if x+2 <= R-1 and y-2 >= 0 :
            if arr[x][y-2] == 0 and arr[x-1][y-1] == 0 and arr[x+1][y-1] == 0 :
                if arr[x+1][y-2] == 0 and arr[x+2][y-1] == 0: #추가
                    return True

    if direction == 'east': #동쪽
        if x+2 <= R-1 and y+2 <= C-1 :
            if arr[x][y+2] == 0 and arr[x-1][y+1] == 0 and arr[x+1][y+1] == 0 :
                if arr[x+1][y+2] == 0 and arr[x+2][y+1] == 0 :
                    return True

    return False

#현재 array를 업데이트
def update_arr(i,x,y,d):
    arr[x][y], arr[x-1][y], arr[x+1][y], arr[x][y-1], arr[x][y+1] = i, i, i, i, i
    if d == 0 : #북
        arr[x-1][y] = -1
    elif d == 1 : #동
        arr[x][y+1] = -1
    elif d == 2 : #남
        arr[x+1][y] = -1
    else : #서
        arr[x][y-1] = -1



#----main 함수----#
def golem_move(i,c,d):
    x,y = -1, c

    while ( x+1 != R-1 ):

        if check('south', x, y):
            x,y = x+1, y
            continue

        else:
            if check('west', x, y):
                x, y = x+1, y-1 #x, y-1
                d = (d-1) % 4
                continue

            else:
                if check('east', x, y):
                    x, y = x+1, y+1 #x, y+1
                    d = (d+1) % 4
                    continue
                else:
                    break

    update_arr(i,x,y,d)

    return x,y,d



def jungryung_move(x,y): #(x,y) : 방문하는 골렘 위치
    dx, dy = [-1,0,1,0], [0,1,0,-1] #북동남서



    q = deque()
    q.append((x,y))
    visited = [[0 for _ in range(C)] for _ in range(R)]
    visited[x][y] = 1

    while q :
        cx, cy = q.popleft()


        for i in range(4):
            nx, ny = cx + dx[i], cy + dy[i]
            # 출구와 인접한 골렘을 찾는 경우
            if arr[cx][cy] == -1:
                if is_inrange(nx, ny):
                    if visited[nx][ny] != 1:
                        if arr[nx][ny] != 0:  # 자기 자신이 아닌 다른 골렘을 찾는다
                            q.append((nx+dx[i], ny+dy[i])) #해당 방향으로 한번 더 이동
                            visited[nx][ny] = 1
                            visited[nx+dx[i]][ny+dy[i]] = 1

            # 출구를 찾고 이동하는 경우
            else :
                if is_inrange(nx, ny):
                    if visited[nx][ny] != 1:
                        if arr[nx][ny] == -1:
                            q.append((nx,ny))
                        visited[nx][ny] = 1




        #출구가 다른 골렘과 인접해있는지 확인한다
        for i in range(4):
            nx, ny = cx+dx[i], cy+dy[i]
            if is_inrange(nx, ny):
                if visited[nx][ny] != 1:
                    if arr[cx][cy] > 0 : # 출구를 찾는 경우
                        if arr[nx][ny] == -1:
                            adjacent = True

                        elif arr[nx][ny] == arr[cx][cy]: #자기자신(탐색) 이거나 출구

                            q.append((nx,ny))
                            visited[nx][ny] = 1



    #다른 골렘과 인접해있지 않으면 해당 골렘의 남쪽으로 이동한다
    # visited 함수의 가장 남단이 최남단 row가 된다

    for i in range(R-1,-1,-1):
       if sum(visited[i]) >= 1 :
        row = (i+1)
        break

    return row




if __name__ == "__main__" :
    ans = 0
    R, C, k = map(int,input().split())
    arr = [[0 for _ in range(C)] for _ in range(R)]

    for i in range(1,k+1):
        c, d = map(int, input().split()) #d:[0,1,2,3] 북,동,남,서
        golem_x, golem_y, d = golem_move(i, c-1,d)

        if not is_inrange(golem_x, golem_y):
            arr = [[0 for _ in range(C)] for _ in range(R)] #초기화
        else :
            row = jungryung_move(golem_x, golem_y)
            ans += row


    print(ans)