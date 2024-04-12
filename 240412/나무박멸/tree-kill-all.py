import sys
from collections import deque
from copy import deepcopy
#sys.stdin = open("input.txt","r")

def is_inrange(x,y):
    return 0<=x<n and 0<=y<n

#1. 성장
def grow(arr):
    temp_grow = deepcopy(arr)

    for i in range(n):
        for j in range(n):
            # 나무가 있다면
            cnt = 0
            if arr[i][j] >= 1:

                # 인접한 네 칸 탐색
                for dx,dy in ((-1,0),(0,1),(1,0),(0,-1)):
                    nx,ny = i + dx, j + dy
                    if not is_inrange(nx,ny) : continue
                    if arr[nx][ny] >= 1 :
                        cnt += 1

                temp_grow[i][j] += cnt

    arr = temp_grow
    return arr




#2. 번식
def breed(arr):
    temp_breed = deepcopy(arr)
    for i in range(n):
        for j in range(n):
            #나무가 있는 칸
            cnt = 0
            if arr[i][j] >= 1 :

                # 인접한 네 칸 탐색
                for dx, dy in ((-1, 0), (0, 1), (1, 0), (0, -1)):
                    nx, ny = i + dx, j + dy
                    if not is_inrange(nx, ny): continue
                    #번식할 수 있는 칸
                    if arr[nx][ny] == 0 :
                        cnt += 1

                for dx, dy in ((-1, 0), (0, 1), (1, 0), (0, -1)):
                    nx, ny = i + dx, j + dy
                    if not is_inrange(nx, ny): continue
                    if arr[nx][ny] == 0:
                        temp_breed[nx][ny] += arr[i][j] // cnt

    arr = temp_breed
    return arr


#3. 제초제 뿌림
def burn_calculate():

    #칸 당 제초제가 뿌려지는 수
    burn_num = [[0 for _ in range(n)] for _ in range(n)]


    for i in range(n):
        for j in range(n):

            #나무가 있는 칸
            if arr[i][j] >= 1 :
                #일단 본인 더함
                burn_num[i][j] += arr[i][j]
                #4개의 대각선 방향으로 k만큼
                for dx, dy in ((-1,-1),(-1,1),(1,-1),(1,1)):
                    temp_k = k
                    nx,ny = i+dx, j+dy
                    #if not is_inrange(nx,ny) : continue

                    while temp_k != 0 :
                        #벽이나 나무 없는 칸을 만나면 그 칸까지만 뿌린다
                        #제초제 뿌린 칸을 만나면?
                        if not is_inrange(nx, ny): break
                        if arr[nx][ny] <= 0 :
                            break

                        else :
                            burn_num[i][j] += arr[nx][ny]
                            nx,ny = nx+dx, ny+dy
                            temp_k -= 1

    return burn_num






ans = 0

arr = []
n,m,k,c = map(int,input().split())

#0-0. 배열 정보 받기
for i in range(n):
    arr.append(list(map(int,input().split())))

#0-1. 벽을 -10000으로 바꿔준다
for i in range(n):
    for j in range(n):
        if arr[i][j] == -1 :
            arr[i][j] = -10000

#m년 동안 박멸 진행
for turn in range(m):

    #1. 성장
    #인접한 네 칸 중 나무가 있는 칸수만큼 성장한다
    #성장은 동시에 발생한다
    arr = grow(arr)

    #2. 번식
    #인접한 네 칸 중 벽, 다른 나무, 제초제 없는 칸에 번식
    #각 칸의 나무 그루 수 // 총 번식이 가능한 칸
    #번식은 "동시에" 발생한다
    arr = breed(arr)

    #3. 제초제 뿌림
    burn_num = burn_calculate()

    max_i, max_j, max_num = 0,0,0
    for i in range(n):
        for j in range(n):
            if burn_num[i][j] > max_num :
                max_num = burn_num[i][j]
                max_i, max_j = i, j

    #박멸되는 나무 수를 계산한다
    ans += max_num

    #가장 많이 박멸되는 칸에 제초제를 뿌린다

    arr[max_i][max_j] = -(c+1)

    # 4개의 대각선 방향으로 k만큼
    for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        temp_k = k
        nx, ny = max_i + dx, max_j + dy
        #if not is_inrange(nx, ny): continue

        while temp_k != 0:
            # 벽이나 나무 없는 칸을 만나면 그 칸까지만 뿌린다
            # 제초제 뿌린 칸을 만나면?
            if not is_inrange(nx, ny): break

            if arr[nx][ny] < -1000 : #벽에는 제초제를 뿌리지 않는다
                break

            if arr[nx][ny] <= 0: #벽 < 0, 나무없는 칸 == 0
                arr[nx][ny] = -(c+1)
                break

            else:
                arr[nx][ny] = -(c+1)
                nx, ny = nx + dx, ny + dy
                temp_k -= 1

    # 제초제가 사라지게 한다
    for i in range(n):
        for j in range(n):
            if arr[i][j] < 0:
                arr[i][j] += 1


print(ans)