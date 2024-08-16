from collections import deque

def is_inrange(x,y):
    return 3<=x<3+R and 0<=y<C

def inrange(x,y):
    return 0<=x<3+R and 0<=y<C

def update_pos(pos, dir):
    if dir == "south":
        for i in range(5):
            pos[i][0], pos[i][1] = pos[i][0]+1, pos[i][1]+0

    if dir == "west":
        for i in range(5):
            pos[i][0], pos[i][1] = pos[i][0]+1, pos[i][1]-1

    if dir == "east":
        for i in range(5):
            pos[i][0], pos[i][1] = pos[i][0]+1, pos[i][1]+1

    return pos

def move_check(pos, dir, arr):
    if dir == "south":
        if inrange(pos[2][0]+1, pos[2][1]) and inrange(pos[3][0]+1, pos[3][1]) and inrange(pos[4][0]+1, pos[4][1]):
            if arr[pos[2][0]+1][pos[2][1]] == 0 and \
                arr[pos[3][0]+1][pos[3][1]] == 0 and \
                    arr[pos[4][0]+1][pos[4][1]] == 0 :
                    return True

    if dir == "west":
        if inrange(pos[0][0],pos[0][1]-1) and \
                inrange(pos[3][0],pos[3][1]-1) and \
                inrange(pos[2][0],pos[2][1]-1) and \
                inrange(pos[2][0]+1,pos[2][1]-1) and \
                inrange(pos[3][0]+1,pos[3][1]-1):

            if arr[pos[0][0]][pos[0][1]-1] == 0 and \
                    arr[pos[3][0]][pos[3][1]-1] == 0 and \
                    arr[pos[2][0]][pos[2][1]-1] == 0 and \
                    arr[pos[2][0]+1][pos[2][1]-1] == 0 and \
                    arr[pos[3][0]+1][pos[3][1]-1] == 0 :
                    return True

    if dir == "east":
        if inrange(pos[0][0],pos[0][1]+1) and \
            inrange(pos[4][0],pos[4][1]+1) and \
            inrange(pos[2][0],pos[2][1]+1) and \
            inrange(pos[2][0]+1,pos[2][1]+1) and \
            inrange(pos[4][0]+1,pos[4][1]+1) :

            if arr[pos[0][0]][pos[0][1]+1] == 0 and \
                    arr[pos[4][0]][pos[4][1]+1] == 0 and \
                    arr[pos[2][0]][pos[2][1]+1] == 0 and \
                    arr[pos[2][0]+1][pos[2][1]+1] == 0 and \
                    arr[pos[4][0]+1][pos[4][1]+1] == 0 :
                return True
    return False

def map_update(pos, arr, index, dir):
    # 골렘 위치 표시
    for i in range(5):
        arr[pos[i][0]][pos[i][1]] = index-1

    # 출구 위치 표시
    if dir == 0 :
        arr[pos[0][0]][pos[0][1]] = index
    elif dir == 1 :
        arr[pos[4][0]][pos[4][1]] = index
    elif dir == 2 :
        arr[pos[2][0]][pos[2][1]] = index
    elif dir == 3 :
        arr[pos[3][0]][pos[3][1]] = index

    return arr

def golem_move(index,c,d,arr):
    pos = [[0,c],[1,c],[2,c],[1,c-1],[1,c+1]] #초기 위치
    while pos[0][0] != R:
        if move_check(pos, "south", arr):
            pos = update_pos(pos, "south")
            continue
        else:
            if move_check(pos, "west", arr):
                pos = update_pos(pos, "west")
                d = (d-1) % 4
                continue
            else :
                if move_check(pos, "east", arr):
                    pos = update_pos(pos, "east")
                    d = (d+1) % 4
                    continue
                else:
                    break #모든 곳으로 이동할 수 없음
    arr = map_update(pos, arr, index,d)
    return pos, arr

def jungryung_move(pos,arr):
    result = 0
    x, y = pos[1]
    dx, dy = [-1, 0, 1, 0], [0, 1, 0, -1]
    visited = [[0 for _ in range(C)] for _ in range(R+3)]

    q = deque()
    q.append((x,y))
    visited[x][y] = 1


    while q:
        x,y = q.popleft()
        for d in range(4):
            nx, ny = x+dx[d], y+dy[d]
            if is_inrange(nx, ny) and visited[nx][ny] == 0 and arr[nx][ny] != 0:
                if arr[x][y] % 2 == 0 : #출구라면 작은 값을 찾는다
                    if arr[nx][ny] < arr[x][y]:
                        q.append((nx, ny))
                        visited[nx][ny] = 1
                else: #출구가 아니라면 같거나 큰 값을 찾는다
                    if arr[nx][ny] >= arr[x][y]:
                        q.append((nx, ny))
                        visited[nx][ny] = 1


    #정령의 가장 최남단 위치 찾기
    for row in range(R+2, 2, -1):
        if sum(visited[row]) >= 1:
            return row-2

def golem_in(pos):
    In = True
    for i in range(5):
        tf = is_inrange(pos[i][0], pos[i][1])
        In = In and tf
    #False가 하나라도 있으면 False 반환해야함
    return In



def main():
    global R, C
    ans = 0
    R,C,K = map(int, input().split())

    arr = [[0 for _ in range(C)] for _ in range(R+3)]

    for index in range(1,K+1):
        c,d = map(int, input().split())
        c = c-1
        pos, arr = golem_move(index*2,c,d,arr)

        if not golem_in(pos):
            arr = [[0 for _ in range(C)] for _ in range(R+3)]
        else :
            ans += jungryung_move(pos,arr)

    print(ans)



if __name__ == "__main__":
    main()