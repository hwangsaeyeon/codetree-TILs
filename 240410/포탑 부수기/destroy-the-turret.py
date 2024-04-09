from collections import deque

#1. 공격자 선정
def select_attacker():
    attacker_x, attacker_y = (-1,-1)#공격자 좌표
    min_val = 5001

    #1-1. 가장 약한 포탑을 공격자로 선정한다
    for i in range(n):
        for j in range(m):
            if arr[i][j] == 0 : #부서지면 continue
                continue
            if arr[i][j] < min_val : #공격력이 가장 낮다면
                min_val = arr[i][j]
                attacker_x, attacker_y = (i,j)
            elif arr[i][j] == min_val : #공격력이 가장 낮은 것이 2개 이상이라면
                if lately_attack[i][j] > lately_attack[attacker_x][attacker_y]: #가장 최근에 공격한 공격자 선택
                    attacker_x, attacker_y = (i,j)
                elif lately_attack[i][j] == lately_attack[attacker_x][attacker_y]:
                    if i+j > attacker_x + attacker_y: #행+열이 가장 큰
                        attacker_x, attacker_y = (i,j)
                    elif i+j == attacker_x + attacker_y : #열 값이 가장 큰
                        if j > attacker_y:
                            attacker_x, attacker_y = (i,j)

    #가장 약한 포탑의 좌표 : attacker (i,j)
    # 1-2. 공격자의 공격력을 업데이트한다
    arr[attacker_x][attacker_y] += (n+m)
    return attacker_x, attacker_y

#2. 공격자 공격
def select_target(attacker_x,attacker_y):
    #x,y 공격자(attacker) 좌표

    #target : 자신을 제외한 가장 강한 포탑
    #2-1. 가장 강한 포탑을 선정한다
    max_val = -1
    target_x, target_y = (-1,-1)
    for i in range(n):
        for j in range(m):
            if save[i][j] == 0 :#부서진 포탑
                continue
            if (i,j) == (attacker_x,attacker_y): #자기자신
                continue
            if arr[i][j] > max_val : #공격력이 가장 높다면
                max_val = arr[i][j]
                target_x, target_y = (i,j)
            elif arr[i][j] == max_val : #공격력이 가장 높은 것이 2개 이상이라면
                if lately_attack[i][j] < lately_attack[target_x][target_y]: #가장 오래전에 공격한 공격자 선택
                    target_x, target_y = (i,j)
                elif lately_attack[i][j] == lately_attack[target_x][target_y]:
                    if i+j < target_x + target_y: #행+열이 가장 작은
                        target_x, target_y = (i,j)
                    elif i+j == target_x + target_y : #열 값이 가장 작은
                        if j < target_y:
                            target_x, target_y = (i,j)
    return target_x, target_y

#2-1. 레이저 공격
def bfs(attacker_x, attacker_y, target_x, target_y):
    q = deque()
    q.append((attacker_x, attacker_y))

    visited = [[False for _ in range(m)] for _ in range(n)]
    visited[attacker_x][attacker_y] = True

    path_x = [[-1 for _ in range(m)] for _ in range(n)] #경로 x 좌표
    path_y = [[-1 for _ in range(m)] for _ in range(n)] #경로 y 좌표


    dx, dy = [0,1,0,-1],[1,0,-1,0] #최단경로인 것이 2개 이상이면 우->하->좌->상의 우선순위를 가짐

    #최단 "경로"가 레이저의 경로가 된다
    min_dist = False #최단경로가 있으면 True
    real_path = [] #실제 경로

    #2-1-1. 최단 경로를 찾는다
    while q:
        x,y = q.popleft()
        if (x,y) == (target_x, target_y):  # 최단 경로를 찾음
            min_dist = True
            # 경로 역추적
            #real_path.append((x, y))
            px = path_x[x][y]
            py = path_y[x][y]

            # 한번에 찾으면
            while (px, py) != (attacker_x, attacker_y):  # 시작점에 도달하기 전까지
                real_path.append((px, py))
                
                tempx = path_x[px][py]
                tempy = path_y[px][py]

                px, py = tempx, tempy #이게 중요 

            return min_dist, real_path

        for i in range(4):
            nx = (x + dx[i] + n) % n
            ny = (y + dy[i] + m) % m
            if arr[nx][ny] <= 0 : #부서진 포탑이라면 이동 불가
                continue

            if visited[nx][ny]:
                continue

            #이동할 수 있다면
            path_x[nx][ny] = x #경로를 저장함
            path_y[nx][ny] = y
            q.append((nx,ny)) #q에 append
            visited[nx][ny] = True #방문 True

    return min_dist, []

#2-2. 포탄 공격
def potan(attacker_x, attacker_y, target_x, target_y):
    #2-2-1. 타겟 : 타겟의 공격력 - 공격자의 공격력 으로 업데이트
    related = [(attacker_x,attacker_y),(target_x,target_y)]

    arr[target_x][target_y] -= arr[attacker_x][attacker_y]
    #2-2-2. 타겟 주위의 8 방향 : 타겟의 공격력 - 공격자의 공격력//2 로 업데이트
    dx, dy = [0,1,0,-1, 1,1,-1,-1],[1,0,-1,0, 1,-1,1,-1]

    for i in range(8):
        # 벗어난 범위 처리
        nx = (target_x+dx[i] + n ) % n
        ny = (target_y+dy[i] + m ) % m

        # 2-2-3. 주위 8 방향에 부서진 포탑이 있다면 continue
        if arr[nx][ny] <= 0 :
            continue

        # 2-2-4. 주위 8 방향에 공격자가 있다면 continue
        if (nx,ny) == (attacker_x, attacker_y) : #arr[nx][ny]로 잘못 썼다....
            continue

        arr[nx][ny] -= arr[attacker_x][attacker_y] //2
        related.append((nx,ny))

    # 2-2-3. 공격과 관련된 리스트 업데이트

    return related

def laser(attacker_x, attacker_y, target_x, target_y):
    min_dist, real_path = bfs(attacker_x, attacker_y, target_x, target_y)

    #2-1-2. 최단 경로를 찾았으면
    if min_dist :
        #2-1-3. 타겟 : 타겟의 공격력 - 공격자의 공격력 으로 업데이트
        arr[target_x][target_y] -= arr[attacker_x][attacker_y]

        #2-1-4. 타겟과 시작점을 제외한 경로 상에 있는 포탑 : 타겟의 공격력 - 공격자의 공격력 // 2로 업데이트
        for real_px, real_py in set(real_path):
            if (real_px,real_py) == (attacker_x,attacker_y):
                continue
            if (real_px,real_py) == (target_x,target_y):
                continue
            arr[real_px][real_py] -= arr[attacker_x][attacker_y] // 2

        #2-1-5. 공격과 관련된 리스트 업데이트
        related = [(attacker_x,attacker_y), (target_x,target_y)] + real_path

    # 최단 경로를 찾지 못했으면 포탄 공격으로 넘어간다
    else :
        related = potan(attacker_x, attacker_y, target_x, target_y)

    return set(related)

n, m, k = map(int, input().split())
arr = []
for _ in range(n):
    arr.append(list(map(int, input().split())))

save = [[1 for _ in range(m)] for _ in range(n)]  # 0이면 부서진것, 1이면은 살아있음
lately_attack = [[0 for _ in range(m)] for _ in range(n)]  # 가장 최근에 공격한 공격자의 리스트

for t in range(1, k + 1):  # k번째 턴동안 4가지 액션을 순서대로
    if sum(sum(save[i]) for i in range(n)) == 1:  # 부서지지 않은 포탑이 1개 남음
        break

    # 1. 공격자 선정
    attacker_x, attacker_y = select_attacker()

    # 2. 공격자 공격 (공격자 선정)
    target_x, target_y = select_target(attacker_x, attacker_y)

    # 2-1. 레이저 공격, #2-2. 포탄 공격
    related = laser(attacker_x, attacker_y, target_x, target_y)

    # 2-3. 최근의 공격자 업데이트
    lately_attack[attacker_x][attacker_y] = t

    for i in range(n):
        for j in range(m):
            # 3. 포탑 부서짐
            if arr[i][j] <= 0:
                arr[i][j] = 0
                save[i][j] = 0

            # 4. 포탑 정비
            if (i, j) in related:  # 공격과 관련이 있다면 continue
                continue

            if arr[i][j] > 0:  # 부서지지 않은 포탑의 공격력을 1 올린다
                arr[i][j] += 1

# 남아있는 포탑 중에 가장 강한 포탑의 공격력
max_val = -1
for i in range(n):
    for j in range(m):
        #if save[i][j] == 1:
        if arr[i][j] > 0 :
            if arr[i][j] > max_val:
                max_val = arr[i][j]

print(max_val)