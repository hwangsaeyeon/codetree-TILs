#입력조건 처리
n, m, k = map(int, input().split())
array = []
for _ in range(n): 
    array.append(list(map(int, input().split()))) 

people = [[] for _ in range(m)]

for i in range(m): 
    r,c = list(map(int,input().split()))
    row, col = r-1, c-1 
    people[i] = (row,col)
    #array[row][col] = -1-i #사람은 음수로 표현


a,b = map(int, input().split())
escape_r, escape_c = a-1, b-1 
array[escape_r][escape_c] = -100 #탈출구 -100

#참가자 이동
dx = [-1,1,0,0]
dy = [0,0,-1,1]

def is_inrange(r,c): 
    return 0<=r<n and 0<=c<n 

def find_square(array): 
    start_r, start_c = -1,-1
    square_size = 2
    
    while square_size <= n : 
        for i in range(n): #시작 행 좌표 
            for j in range(n): #시작 열 좌표 
                people_num = 0 
                escape_in = False 

                if i+square_size-1 > n or j+square_size-1 >n : 
                    continue 

                #사람을 포함한다면
                for k in range(m): 
                    if len(people[k]) > 0 : #탈출하지 않은 사람 !!
                        people_r, people_c = people[k] 
                        if i <= people_r <= i+square_size-1 and j <= people_c <= j+square_size -1 : 
                            people_num += 1
                
                #출구좌표를 포함한다면 
                if i <= escape_r <= i+square_size-1 and j <= escape_c <= j+square_size -1 : 
                    escape_in = True
 
                #정사각형이고, 사람과 출구좌표를 포함한다면 
                if people_num >= 1 and escape_in==True : 
                    start_r, start_c = i, j 
                    return start_r, start_c, square_size 
                    
                
        square_size += 1 

import copy 
def rotate(start_r, start_c, square_size, escape_r, escape_c,people): 
    new_arr = copy.deepcopy(array)

    for r in range(start_r, start_r + square_size):
        for c in range(start_c, start_c+square_size):
            # 1단계 : (0,0)으로 옮겨주는 변환을 진행함
            orow, ocol = r - start_r, c - start_c
            # 2단계 : 90도 회전했을때의 좌표를 구함
            rotate_r, rotate_c = ocol, square_size - orow - 1  
            # 3단계 : 다시 (sy,sx)를 더해줌
            new_arr[start_r + rotate_r][start_c + rotate_c] = array[r][c]
        
    # new_arr 값을 현재 board에 옮겨줌
    temp = [[] for _ in range(m)]
    for r in range(start_r, start_r + square_size):
        for c in range(start_c, start_c+square_size):
            array[r][c] = new_arr[r][c]

            #내구도 -1 
            if new_arr[r][c] > 0 : 
                array[r][c] -= 1 
    
            #탈출구 좌표 업데이트 
            if new_arr[r][c] == -100: 
                escape_r, escape_c = r, c
    
    for i in range(m):
        if len(people[i]) > 0 :  
            r, c = people[i]
            if start_r <= r < start_r + square_size and start_c <= c < start_c + square_size: 
                orow, ocol = r - start_r, c - start_c
                rotate_r, rotate_c = ocol, square_size - orow - 1  
                people[i] = (start_r + rotate_r, start_c + rotate_c)
        

    return array, escape_r, escape_c, people










answer_distance = 0 

for time in range(k): 
    #print('------------------')
    exit = 0 
    #모든 참가자가 이동할 수 있다면 이동시킨다
    #print(array)
    #print(people)
    for i in range(m):
        if len(people[i]) != 0 : #탈출 하지 않은 참가자 
            r,c = people[i] 
            mini_r = r
            mini_c = c
            mini = abs(r - escape_r) + abs(c - escape_c)
            for direction in range(4): 
                
                nr = r + dx[direction] 
                nc = c + dy[direction]
            

                #이동한 곳에 벽이 존재하지 않으면 
                if is_inrange(nr,nc) : 
                    if array[nr][nc] <= 0 : 
                        if abs(nr - escape_r) + abs(nc - escape_c) < mini :               
                            mini = abs(nr - escape_r) + abs(nc - escape_c)
                            mini_r = nr 
                            mini_c = nc 

            #이동한다면 좌표 업데이트 
            if mini_r != r or mini_c != c : 
                
                answer_distance += 1
                #출구에 도착한다면 초기화시켜준다 
                if mini_r == escape_r and mini_c == escape_c : 
                    
                    people[i] = [] 
                        
                        


                #출구에 도착하지 않고 그냥 이동한다면
                else: 
                    #참가자의 좌표를 업데이트
                    people[i] = (mini_r, mini_c)
                    #행렬 업데이트
                    #array[mini_r][mini_c] = -i-1
                #array[r][c] = 0 

                    
    #print(answer_distance)

    #모든 참가자가 미로를 탈출하면 중단 
    for i in range(m): 
        if len(people[i]) == 0 : 
            exit += 1 
    if exit == m : 
        break 

    
    #출구와 참가자를 포함한 가장 작은 정사각형 좌표와 size 찾기 
    start_r, start_c, square_size = find_square(array)


    #90' 회전시키고 정사각형 내 벽의 내구도를 -1 시킨다 
    #배열 업데이트한다(출구 위치 바뀜) 
    array, escape_r, escape_c, people = rotate(start_r, start_c, square_size, escape_r, escape_c,people)

                   

#게임 시작 후 K초가 지났거나 
#모든 참가자가 미로를 탈출했을 때
#모든 참가자들의 이동 거리 합과 출구 좌표
#좌표 + 1 해줄것 
print(answer_distance)
print(escape_r+1, escape_c+1)