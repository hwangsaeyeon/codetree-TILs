import sys
from collections import deque
#sys.stdin = open("input.txt","r")

#1. 몬스터 복제 시도
def duplicate_monster(idx):
    '''
    :param idx: 몬스터의 인덱스
    :return:
    '''

    #1-1. 자신과 방향이 같은 몬스터 복제
    r, c, d = monster_pos[idx]
    if (r,c,d) != (-1,-1,-1):
        egg_pos.append((r,c,d))

def is_inrange(x,y):
    return 0<=x<4 and 0<=y<4

#2. 몬스터 이동
def monster_move(idx):
    '''
    :param idx: 몬스터의 인덱스
    :return: r,c,d 이동한 뒤의 몬스터 좌표
    '''

    x, y, d = monster_pos[idx]
    if (x,y) == (-1,-1):
        return x,y,d

    #2-1. 방향대로 1칸 이동
    dx, dy = [-1,-1,0,1,1,1,0,-1],[0,-1,-1,-1,0,1,1,1]
    nx,ny = x+dx[d], y+dy[d]

    #2-2. 몬스터 시체가 있거나, 팩맨이 있거나, 격자를 벗어나는 경우 방향을 반시계 45'로 돌려 이동가능할 때 이동한다
    if is_inrange(nx,ny) :
        if (nx,ny) not in dead_pos :
            if (nx,ny) != (packman_r, packman_c) :
                return nx,ny,d

    nd = d #nd에 현재 방향 저장

    for i in range(8):
        nd = (nd+1) % 8 #반시계 방향으로 계속 전환한다
        nx, ny = x+dx[nd], y+dy[nd]

        if is_inrange(nx, ny):
            if (nx, ny) not in dead_pos:
                if (nx, ny) != (packman_r, packman_c):
                    return nx, ny, nd

    #2-3. 8방향을 돌았는데 이동이 불가능하다면 이동하지 않는다 **(방향을 원래방향으로 해야되나?)
    return x, y, nd

#3. 팩맨 이동
def dfs(x,y,move_cnt,monster_cnt):
    '''
    :param r: 팩맨의 행 좌표
    :param c: 팩맨의 열 좌표
    :param move_cnt: 현재까지의 이동횟수
    :return:
    '''
    dx, dy = [-1, 0, 1, 0], [0, -1, 0, 1]

    visited[x][y] = True

    if move_cnt == 3 :
        eat[x][y] = monster_cnt
        return #현재까지 먹은 몬스터의 개수



    for i in range(4):
        nx, ny = x + dx[i], y + dy[i]
        if not is_inrange(nx,ny) : continue
        if visited[nx][ny] : continue

        crr_cnt = 0 #해당 방향에서 먹을 수 있는 몬스터 수
        for idx in range(m):
            mx,my, _ = monster_pos[idx]
            if (nx,ny) == (mx,my) :
                crr_cnt += 1

        path_x[nx][ny] = x #우선 순위 경로 저장
        path_y[nx][ny] = y

        dfs(nx,ny,move_cnt+1,monster_cnt+crr_cnt)

    #알, 움직이기 전에 함께 있었던 몬스터는 먹지 않는다




def packman_move(packman_r, packman_c,turn):
    global m
    # 3칸 이동하는데 먹는 팩맨이 최대가 되도록 하는 경우
    dfs(packman_r,packman_c,0,0)

    max_x, max_y, max_val = -1,-1,0

    for i in range(4):
        for j in range(4):
            if eat[i][j] > max_val :
                max_val = eat[i][j]
                max_x, max_y = i,j


    past_x = max_x
    past_y = max_y
 
    # 이동하는 경로에 있는 몬스터를 시체처리한다 (좌표에서 삭제하자)
    while (past_x, past_y) != (packman_r, packman_c):
        #하나의 좌표에 몬스터가 두개 있을 수도 있다
        for idx in range(m):
            mx,my,_= monster_pos[idx]
            if (past_x, past_y) == (mx,my):
                monster_pos[idx] = (-1,-1,-1)  #몬스터를 제거한다

                if (past_x, past_y) not in dead_pos :
                    dead_pos.append((past_x, past_y))
                    dead_time.append(turn + 2)


        tempx = path_x[past_x][past_y]
        tempy = path_y[past_x][past_y]
        past_x, past_y = tempx, tempy


    #팩맨의 좌표를 업데이트한다
    packman_r, packman_c = max_x, max_y
    return packman_r, packman_c


#0. 몬스터의 마리수 m, 진행되는 턴의 수 t
#팩맨의 격자에서의 초기위치 r,c
m,t = map(int,input().split())
tr, tc = map(int,input().split())
packman_r, packman_c = tr-1, tc-1

#몬스터의 위치 r,c와 방향정보 d
monster_pos = [[] for _ in range(m)]

#몬스터 복제 배열
egg_pos = []

#시체 시간, 시체 좌표 배열
#시체는 몬스터 이동에만 고려되므로 다른 배열과 독립적임
dead_time = []
dead_pos = []




for i in range(m):
    r, c, d = map(int,input().split())
    monster_pos[i] = r-1, c-1,d-1




for i in range(t):
    #1. 몬스터 복제 시도
    for m_idx in range(m):
        duplicate_monster(m_idx)

    #2. 몬스터 이동
    for m_idx in range(m):
        r,c,d = monster_move(m_idx)
        monster_pos[m_idx] = r,c,d

    #3. 팩맨 이동
    visited = [[False for _ in range(4)] for _ in range(4)]
    path_x = [[-1 for _ in range(4)] for _ in range(4)]
    path_y = [[-1 for _ in range(4)] for _ in range(4)]
    eat = [[0 for _ in range(4)] for _ in range(4)]

    path_x[packman_r][packman_c] = packman_r
    path_y[packman_r][packman_c] = packman_c

    packman_r, packman_c = packman_move(packman_r, packman_c, i)

    #4. 몬스터 시체 소멸
    #pop을 하는 순간 좌표가 바뀜에 주의한다

    for idx in range(len(dead_time)):
        if dead_time[idx] == i : #현재 턴이 시체 소멸 시간을 넘으면
            dead_pos[idx] = (-1,-1) #시체 좌표에서 제거한다


    #5. 몬스터 복제 완성
    for m_idx in range(len(egg_pos)):
        dr, dc, dd = egg_pos[m_idx]
        monster_pos.append((dr,dc,dd))

    #5-1. 몬스터 개수 업데이트
    m = len(monster_pos)

    #5-2. 복제 배열 초기화
    egg_pos = []


ans = 0
for i in range(m):
    if monster_pos[i] != (-1,-1,-1):
        ans+=1

print(ans)