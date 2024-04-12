#############################################################

def m_duplicate(idx):
    r,c,d = m_pos[idx]
    if (r,c) != (-1,-1):
        e_pos.append((r,c,d))

#############################################################
def is_inrange(x,y):
    return 0<=x<4 and 0<=y<4

def m_move(idx):
    r,c,d = m_pos[idx]
    if (r,c) == (-1,-1) :
        return

    dx, dy = [-1,-1,0,1,1,1,0,-1],[0,-1,-1,-1,0,1,1,1]


    nr, nc = r+dx[d], c+dy[d]

    if is_inrange(nr,nc):
        if (nr,nc) != (pr,pc) :
            if (nr,nc) not in d_pos:
                m_pos[idx] = nr, nc, d
                return

    #8방향 반시계 방향으로 회전
    nd = d #현재 방향 복사
    for i in range(8):
        nd = (nd+1) % 8 # % len
        nr, nc = r+dx[nd], c+dy[nd] #현재 위치에서 방향만 트는 것
        if is_inrange(nr, nc):
            if (nr, nc) != (pr, pc):
                if (nr, nc) not in d_pos:
                    m_pos[idx] = nr, nc, nd
                    return

    return

#############################################################
def p_move(pr, pc):

    dx, dy = [-1,0,1,0],[0,-1,0,1] #상좌하우
    path = []
    mc = 0


    for i in range(4): #첫번째이동
        fr, fc = pr+dx[i], pc+dy[i]
        if not is_inrange(fr,fc):continue

        for j in range(4): #두번째이동
            sr, sc = fr+dx[j], fc+dy[j]
            if not is_inrange(sr,sc):continue

            for k in range(4): #세번째이동
                eat_cnt = 0 #방향 전환시 먹을 수 있는 몬스터 수 초기화
                tr, tc = sr+dx[k], sc+dy[k]
                if not is_inrange(tr,tc):continue

                # 현재 방향으로 세칸이동할 때 먹을 수 있는 몬스터의 수
                # 똑같은 자리에 두번 오게 되면 첫번째 먹은 것만 카운트한다.
                # 첫번째, 세번째만 비교해주면된다. 두번째가 중복된 자리여도, 처음에 있던 자리는 먹지 않은 상태이기 때문
                if (fr,fc) == (tr,tc):
                    eat_cnt = (arr[fr][fc] + arr[sr][sc])
                else:
                    eat_cnt = (arr[fr][fc] + arr[sr][sc] + arr[tr][tc])

                if eat_cnt > mc :
                    mc = eat_cnt
                    path = [(fr,fc),(sr,sc),(tr,tc)]



    #모든 경로 탐색 완료
    #팩맨이 먹을 수 없는 경우도 있으려남?

    #팩맨 이동
    pr, pc = path[-1][0], path[-1][1]

    for x,y in path :
        #최대 경로대로 먹고
        #시체 처리한다 (m_pos, d_pos, d_time, arr 업데이트 필요)

        if arr[x][y] > 0 : #경로 내에 몬스터가 있었다면
            d_pos.append((x,y))
            d_time.append(turn+2)
            arr[x][y] = 0

        #몬스터 좌표 업데이트
        for i in range(m):
            r,c,d = m_pos[i]
            if (r,c) == (x,y):
                m_pos[i] = -1,-1,-1


    return pr, pc





#############################################################

m,t = map(int, input().split())

r,c = map(int, input().split())
pr, pc = r-1, c-1

m_pos = [] #몬스터 위치
for _ in range(m):
   r,c,d = map(int,input().split())
   m_pos.append((r-1,c-1,d-1))

e_pos = [] #알 위치
d_pos = [] #시체 위치
d_time = [] #시체 소멸 시간

arr = [[0 for _ in range(4)] for _ in range(4)]

#############################################################

for turn in range(t):

    # 1. 몬스터 복제 시도
    for i in range(m):
        m_duplicate(i)

    #2. 몬스터 이동
    for i in range(m):
        m_move(i)


    #3-0. 격자에 몬스터 개수 표현
    arr = [[0 for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for idx in range(m):
                r,c,_ = m_pos[idx]
                if (r,c) == (i,j):
                    arr[i][j] += 1


    #3. 팩맨 이동
    pr, pc = p_move(pr, pc)


    #4. 시체 소멸
    for i in range(len(d_time)) :
        if d_time[i] == turn :
            d_time[i] = -1
            d_pos[i] = (-1,-1)

    #5. 복제 완성
    for i in range(len(e_pos)):
        m_pos.append(e_pos[i])

    m = len(m_pos)
    e_pos = []




#살아남은 몬스터의 수
ans = 0
for i in range(m):
    r,c,d = m_pos[i]
    if (r,c) != (-1,-1):
        ans += 1

print(ans)