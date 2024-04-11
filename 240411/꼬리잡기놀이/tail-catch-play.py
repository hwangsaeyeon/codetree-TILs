from collections import deque


#1. 머리 사람을 따라 한칸 이동 --------------------------------------
def move(idx):
    x,y = team_pos[idx].pop()
    #좌표 업데이트
    team_pos[idx].insert(0, (x,y))

    #배열 업데이트

    for i in range(len(team_pos[idx])) :
        if i == 0 :
            ppl = 1
        elif i < team_member[idx]-1 :
            ppl = 2
        elif i == team_member[idx]-1 :
            ppl = 3
        else :
            ppl = 4

        x, y = team_pos[idx][i]
        arr[x][y] = ppl



#2. 라운드에 따라 공을 던짐, 선에 사람이 있으면 --------------------------------------
def search(round, direction):
    # 방향 0 : 왼쪽부터 행탐색, 1 : 아래쪽부터 열탐색, 2: 오른쪽부터 행탐색, 3: 위쪽부터 열탐색
    # round가 1이라면 0번째 행(or열) 2라면 1번째 행(or 열 탐색)
    meet_first = - 1 #최초에 만나는 사람

    if direction == 0 : #(round-1, 0) 부터 (round-1, n-1) 까지 탐색
        for i in range(n):
            if 0 < arr[round-1][i] < 4 : #최초에 만나는 사람
                meet_first = arr[round-1][i]

                for j in range(m):
                    for idx in range(len(team_pos[j])):
                        if team_pos[j][idx] == (round-1, i):
                            return idx+1, j # 최초에 만나는 사람의 팀이 어느 팀인지 구한다


    elif direction == 1 : #(n-1, round-1) 부터 (0, round-1)까지 탐색
        for i in range(n,-1,-1):
            if 0 < arr[i][round-1] < 4 : #최초에 만나는 사람
                meet_first = arr[i][round-1]

                for j in range(m):
                    for idx in range(len(team_pos[j])):
                        if team_pos[j][idx] == (i, round-1):
                            return idx+1, j  # 최초에 만나는 사람의 팀이 어느 팀인지 구한다

    elif direction == 2 : #(round-1, n-1) 부터 (round-1,0) 까지 탐색
        for i in range(n,-1,-1):
            if 0 < arr[round-1][i] < 4 : #최초에 만나는 사람
                meet_first = arr[round-1][i]

                for j in range(m):
                    for idx in range(len(team_pos[j])):
                        if team_pos[j][idx] == (round - 1, i):
                            return idx+1, j  # 최초에 만나는 사람의 팀이 어느 팀인지 구한다

    elif direction == 3 : #(0, round-1) 부터 (n, round-1)까지 탐색
        for i in range(n):
            if 0 < arr[i][round-1] < 4 : #최초에 만나는 사람
                meet_first = arr[i][round-1]

                for j in range(m):
                    for idx in range(len(team_pos[j])):
                        if team_pos[j][idx] == (i, round-1):
                            return idx+1, j  # 최초에 만나는 사람의 팀이 어느 팀인지 구한다

    return meet_first, None #-1라면 아무도 없는 것임, 최초에 만나는 사람의 팀


#0. 입력처리 --------------------------------------
def is_inrange(x,y):
    return 0<=x<n and 0<=y<n

def bfs(head_pos, team_idx):
    dx, dy = [0,-1,0,1],[1,0,-1,0]
    q = deque()

    head_x, head_y = head_pos
    visited = [[False for _ in range(n)] for _ in range(n)]

    q.append((head_x, head_y))
    visited[head_x][head_y] = True

    max_val = 2
    cnt = 0

    while q :
        x, y = q.popleft()

        team_pos[team_idx].append((x,y))

        if arr[x][y] < 4 :
            cnt += 1


        for i in range(4) :
            nx, ny = x + dx[i], y + dy[i]

            if is_inrange(nx,ny):
                if not visited[nx][ny]:
                    if arr[nx][ny] > 0 :
                        if arr[nx][ny] <= max_val :
                            q.append((nx, ny))
                            visited[nx][ny] = True
                            if arr[nx][ny] == max_val :
                                max_val += 1

    team_member[team_idx] = cnt




n,m,k = map(int,input().split())


arr = []
for _ in range(n):
    arr.append(list(map(int,input().split())))


team_pos = [[] for _ in range(m)]
team_member = [[] for _ in range(m)]

head_pos = []

#머리 좌표
for i in range(n):
    for j in range(n):
        if arr[i][j] == 1 :
            head_pos.append((i,j))


#머리, 꼬리 좌표, 팀(0~) 위치 좌표
for i in range(m):
    bfs(head_pos[i], i)


dir = -1
score = 0

for t in range(1, k+1) : #턴은 1부터 시작
    
    for i in range(m) : #팀 순회
        # 1. 머리 사람을 따라 한 칸 이동
        move(i)

    # 2. 라운드에 따라 공이 던져진다

    round = t % (n+1)
    if round == 1 :
        dir = (dir + 1) % 4 #round는 1~n까지 존재, 방향은 0~3까지 존재

    meet_first, team_num = search(round, dir)

    # 3. 선에 사람이 있으면 최초에 만나는 사람만 점수를 얻는다
    if meet_first != -1: #선에 만나는 최초의 사람
        score += (meet_first) ** 2

        #머리 사람과 꼬리 사람을 바꾼다
        #meet_first 는 team_num 의 멤버이다

        #좌표를 업데이트한다
        member_num = team_member[team_num]
        new_order = []

        while member_num != 0 :
            x, y = team_pos[team_num].pop(member_num-1) #member_num은 index이다.
            new_order.append((x,y))
            member_num -= 1

        while team_pos[team_num] :
            x, y = team_pos[team_num].pop() #끝에서부터 꺼낸다
            new_order.append((x,y))

        team_pos[team_num] = new_order

        #배열을 업데이트한다
        for i in range(len(team_pos[team_num])):
            if i == 0:
                ppl = 1
            elif i < team_member[team_num]- 1:
                ppl = 2
            elif i == team_member[team_num]- 1:
                ppl = 3
            else:
                ppl = 4

            x, y = team_pos[team_num][i]
            arr[x][y] = ppl

print(score)