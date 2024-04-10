def is_inrange(x,y):
    return 0<=x<n and 0<=y<n

def hider_move(seeker_pos, hider):
    hider_x,hider_y,hider_direction = hider_pos[hider]

    dx, dy = [-1,0,1,0],[0,1,0,-1] #상우하좌
    new_direction = [2,3,0,1]

    # 술래와의 거리가 3이하라면 도망간다
    if abs(seeker_x - hider_x) + abs(seeker_y - hider_y) <= 3:

        #바라보는 방향으로 1칸 이동한다
        nx, ny = hider_x + dx[hider_direction], hider_y + dy[hider_direction]

        #이동하는 곳이 격자 내라면
        if is_inrange(nx,ny) :
            if (nx,ny) != seeker_pos :
                #술래가 없다면 이동한다
                hider_pos[hider] = nx,ny,hider_direction

        #이동하는 곳이 격자 밖이라면
        else :
            #방향을 반대로 틀어준다
            new_dir = new_direction[hider_direction]
            nx, ny = hider_x + dx[new_dir], hider_y + dy[new_dir]

            #술래가 없다면 1칸 앞으로 이동한다.
            if (nx, ny) != seeker_pos :
                hider_pos[hider] = nx, ny, new_dir

            else :
                hider_pos[hider] = hider_x, hider_y, new_dir

def seeker_move(seeker_pos,d,move_dist,direction_cnt,cnt,inout): # d : 술래의 방향, inout : 안에서 밖으로
    x,y = seeker_pos #술래의 현재 좌표

    dx, dy = [-1, 0, 1, 0], [0, 1, 0, -1]

    nx, ny = x + dx[d], y + dy[d]  # 술래는 방향대로 1칸 움직인다
    cnt += 1

    if inout : #안에서 밖으로

        if cnt == move_dist:  # 이동 칸수만큼 움직이면
            d = (d + 1) % 4  # 방향을 바꾼다
            direction_cnt += 1  # 방향 바꾼 횟수 +1
            cnt = 0

        if direction_cnt == 2:  # 방향을 두번 바꾸면
            move_dist += 1  # 이동할 수 있는 거리를 하나 늘려준다
            direction_cnt = 0

        #좌표 업데이트

    else : #밖에서 안으로

        if cnt == move_dist:  # 이동 칸수만큼 움직이면
            d = (d - 1) % 4  # 방향을 바꾼다
            direction_cnt += 1  # 방향 바꾼 횟수 +1
            cnt = 0

        if direction_cnt == 2:  # 방향을 두번 바꾸면
            move_dist -= 1  # 이동할 수 있는 거리를 하나 줄여준다
            direction_cnt = 0

    # 한칸 이동
    seeker_pos = (nx,ny)
    # 이동 후의 위치가 방향이 틀어지는 지점이라면 바로 방향을 틀어준다

    # 정중앙 혹은 (0,0)에 도달한다면 방향을 바로 틀어준다
    if seeker_pos == (0,0) :
        inout = False
        d = 2
        move_dist = n
        direction_cnt = 1  # 방향 2번 바꾸면 move_dist 하나 감소
        cnt = 1  # 현재까지 이동 몇칸했는지

    elif seeker_pos == (n//2,n//2) :
        inout = True
        d = 0
        move_dist = 1  # 방향 2번 바꾸면 move_dist 1증가
        direction_cnt = 0  # 방향을 2번 바꿨는지 확인하는 변수
        cnt = 0  # 현재까지 이동 몇 칸 했는지

    arr = [[-1 for _ in range(n)] for _ in range(n)]
    arr[nx][ny] = d


    return seeker_pos, d, move_dist, direction_cnt, cnt, inout #술래 좌표, 술래의 이동 방향, 방향을 바꿔야 하는 횟수, 이동할 수 있는 칸 수, 현재 이동 칸, 나선형 방향






n,m,h,k = map(int,input().split())
seeker_pos = (n//2,n//2)
hider_pos = [] #x좌표,y좌표,방향
tree_pos = []

for i in range(m): #도망자 좌표
    x,y,d = map(int,input().split())
    hider_pos.append((x-1,y-1,d)) #d=1 좌(우), d=2 상(하)

for i in range(h):
    x,y = map(int,input().split())
    tree_pos.append((x-1,y-1))

move_dist = 1  # 방향 2번 바꾸면 move_dist 1증가
direction_cnt = 0  # 방향을 2번 바꿨는지 확인하는 변수
cnt = 0  # 현재까지 이동 몇 칸 했는지
inout = True
d = 0







scores = 0


for t in range(1, k+1):
    disappear_cnt = 0 #턴에 따라 잡는 도망자 수 초기화

    seeker_x, seeker_y = seeker_pos



    #1. m명의 도망자 이동
    for hider in range(m):
        #잡힌 도망자라면
        if len(hider_pos[hider]) == 0 :
            continue


        hider_move(seeker_pos, hider) #도망자의 좌표 업데이트

    #2. 술래 이동
    # 술래 좌표, 술래의 이동 방향, 방향을 바꿔야 하는 횟수, 이동할 수 있는 칸 수, 현재 이동 칸
    seeker_pos, d, move_dist, direction_cnt, cnt, inout = seeker_move(seeker_pos,d,move_dist,direction_cnt,cnt,inout)

    #3. 도망자 잡음
    dx, dy = [-1, 0, 1, 0], [0, 1, 0, -1]

    #현재 바라보고 있는 방향칸 3칸에
    # 도망자가 있다면 잡음 -> 사라짐
    seeker_x, seeker_y = seeker_pos
    for i in range(m):
        #잡힌 도망자라면
        if len(hider_pos[i]) == 0 :
            continue

        hider_x, hider_y, _ = hider_pos[i]
        # 바라보고 있는 방향 3칸에 도망자가 있음
        # 방향이 왼쪽이나 위쪽이라면 (상우하좌 0123)
        if d == 3 or d == 0 :
            if seeker_x + dx[d]*2 <= hider_x <= seeker_x :
                if seeker_y + dy[d]*2 <= hider_y <= seeker_y :
                    #해당 칸에 나무가 있다면 잡지 않는다
                    if (hider_x,hider_y) in tree_pos :
                        pass
                    else:
                        hider_pos[i] = [] #좌표에서 사라지게 한다
                        disappear_cnt += 1
    
        else :

            if seeker_x <= hider_x <= seeker_x + dx[d]*2 :
                if seeker_y <= hider_y <= seeker_y + dy[d]*2 :
                    #해당 칸에 나무가 있다면 잡지 않는다
                    if (hider_x,hider_y) in tree_pos :
                        pass
                    else:
                        hider_pos[i] = [] #좌표에서 사라지게 한다
                        disappear_cnt += 1

    #점수 계산(획득) : t * 사라진 도망자 수
    scores += (t * disappear_cnt)


print(scores)