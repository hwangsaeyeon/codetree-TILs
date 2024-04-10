import sys
from collections import deque

sys.stdin = open("input.txt","r")

def is_inrange(x,y):
    return 0<=x<n and 0<=y<n
def step_one(x,y,d):
    #본인이 향하는 방향대로 한칸 이동한다
    #0,1,2,3 상,우,하,좌
    dx,dy = [-1,0,1,0],[0,1,0,-1]
    nx,ny = x+dx[d], y+dy[d]
    nd = d


    #격자를 벗어나는 경우 정반대 방향으로 방향을 바꾼다
    #0,1,2,3 하,좌,상,우

    ox, oy = [1,0,-1,0],[0,-1,0,1]
    new_direction = [2,3,0,1]
    if not is_inrange(nx,ny): #격자를 벗어나는 경우
        nx,ny = x+ox[d], y+oy[d]
        nd = new_direction[d]

    return nx,ny,nd #이동 위치, 이동 방향 리턴



def gun_switch(x,y,idx):
    if arr[x][y] != [0] : #총이 있는 경우
        original = gun_power[idx]

        if original < max(arr[x][y]) :#놓인 총이 더크다면
            #더 큰 것을 가지고
            gun_power[idx] = max(arr[x][y])
            arr[x][y].remove(max(arr[x][y]))

            #원래 값이 0이 아니었더라면(가지고 있는 총이 없었음) 나머지는 해당 격자에 둔다
            if original != 0 :
                arr[x][y].append(original)

            if len(arr[x][y]) == 0: #총을 가져서 리스트가 []가 되는 경우
                arr[x][y] = [0]


def fight(player_idx, other_player_idx, x,y,ox,oy):
    #플레이어 초기 능력치 + 총의 공격력 합 계산
    #다른 플레이어 초기 능력치 + 총의 공격력 합 계산
    winner_idx = -1
    loser_idx = -1
    player_val = player_info[player_idx][-1] + gun_power[player_idx]
    other_player_val = player_info[other_player_idx][-1] + gun_power[other_player_idx]


    # 값이 더 큰 플레이어
    if player_val > other_player_val:
        winner_idx = player_idx
        loser_idx = other_player_idx
    elif player_val == other_player_val:  # 값이 같다면 초기 능력치가 큰 플레이어가 이긴다
        if player_info[player_idx][-1] > player_info[other_player_idx][-1] :
            winner_idx = player_idx
            loser_idx = other_player_idx
        else :
            winner_idx = other_player_idx
            loser_idx = player_idx
    else :
        winner_idx = other_player_idx
        loser_idx = player_idx

    #이긴 플레이어, 진 플레이어 인덱스 저장
    #이긴 플레이어는 포인트를 획득한다 : abs(초기능력치 + 총의 공격력의 차)

    scores[winner_idx] += abs(player_val - other_player_val)

    return winner_idx, loser_idx #이긴 플레이어, 진 플레이어 인덱스 반환

def find_other(idx, x, y): #자기 인덱스, 자기 x 좌표, 자기 y 좌표 :: 다른 사람이 있는지 찾는 함수
    for i in range(m):
        if i == idx :
            continue
        fx, fy, _, _, = player_info[i]
        if (fx, fy) == (x, y):  # 다른 플레이어가 있다면
            return True

    return False

def loser_move(loser):
    lx, ly, ld, ls = player_info[loser]
    dx, dy = [-1, 0, 1, 0], [0, 1, 0, -1]
    x,y = lx + dx[ld], ly + dy[ld] #원래 방향으로 한 칸 이동한 좌표

    # 격자 안, 사람 없으면
    if is_inrange(x,y):
        if not find_other(loser,x,y):
            #그 칸으로 이동한다
            player_info[loser] = x,y,ld,ls
            return

    # 격자 안에 없거나, 사람이 있음
    for i in range(ld+1, ld+4):
        nd = i%4
        nx, ny = lx+dx[nd], ly+dy[nd]
        if not is_inrange(nx,ny):
            continue
        if find_other(loser,nx,ny):
            continue

        #그 칸으로 이동한다
        player_info[loser] = nx,ny,nd,ls
        return




def step_two(player_idx, other_player_idx, x,y,ox,oy):
    # 싸움 : 스코어 계산
    winner, loser = fight(player_idx, other_player_idx, x,y,ox,oy)
    wx,wy,wd,ws= player_info[winner]
    lx, ly, ld, ls = player_info[loser]

    # 진 플레이어 :
    #총을 내려놓는다
    if gun_power[loser] == 0 :
        pass
    else:
        if arr[lx][ly] == [0]:
            arr[lx][ly] = [gun_power[loser]]
        else:
            arr[lx][ly].append(gun_power[loser])

    gun_power[loser] = 0

    #진 플레이어는 이동한다
    loser_move(loser)
    lx,ly,ld,ls = player_info[loser]

    #이동한 칸에 총이 있다면 gun switch
    gun_switch(lx,ly,loser)

    #====================

    # 이긴 플레이어 :
    #현재 칸에서 gun switch
    gun_switch(wx,wy,winner)





n, m, k = map(int, input().split()) #n: 격자, m : 플레이어 수, k 라운드

#격자 정보 업데이트
arr = [[[] for _ in range(n)] for _ in range(n)] #총이 2개 이상 위치 할 수 있어 3차원으로 설정
for i in range(n):
    line = list(map(int, input().split()))
    for j in range(n):
        arr[i][j] = [line[j]]

ability = [] #능력치 리스트

gun_power = [[] for _ in range(m)] #가지고 있는 총의 공격력 비교 배열
player_info = [[] for _ in range(m)] #플레이어 정보 리스트

#플레이어 정보 x,y,d,s (x,y) 초기위치, (d) 초기방향, (s) 초기 능력치
for i in range(m):
    x,y,d,s = map(int,input().split())
    player_info[i] = [x-1,y-1,d,s]
    gun_power[i] = 0

scores = [0 for _ in range(m)] #포인트 리스트
for t in range(k): #k 라운드 동안 게임 순차적 진행

    for i in range(m): #각 플레이어가 순서대로 진행
        x,y,d,s = player_info[i]
        #첫번째 스텝 : 본인이 향하는 방향대로 한 칸 이동한다(무조건 이동)
        #=====================================

        nx,ny,nd = step_one(x,y,d)
        player_info[i] = nx,ny,nd,s #업데이트 한다

        # =====================================


        #두번째 스텝 :
        meet = False
        for j in range(m):
            if i == j : # 본인일 경우 pass
                continue

            other_x, other_y, _, _ = player_info[j]

            if (nx,ny)  == (other_x, other_y) :#2-2-1 이동한 방향에 플레이어가 있다면
                ## (fight)
                step_two(i,j,nx,ny,other_x,other_y)
                meet = True
                break


        #2-1 이동한 방향에 플레이어가 없다면
        if not meet :
            #이동한 방향에 플레이어가 없는 경우 (총 switch)
            gun_switch(nx,ny, i)



    #출력 : 각 플레이어들이 획득한 포인트
    print(*scores)