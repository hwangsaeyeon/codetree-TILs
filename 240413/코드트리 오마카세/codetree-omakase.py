import sys
from collections import deque
from copy import deepcopy
#sys.stdin = open("input.txt","r")


l, q = map(int,input().split()) #초밥 벨트의 길이 L, 명령수 Q

sushi = [['empty'] for _ in range(l)]

ppl = ['' for _ in range(l)]
eat = [0 for _ in range(l)]


order_q = deque()
for i in range(q):
    order_q.append(list(map(str,input().split())))

sushi_num = 0
ppl_num = 0

t = 0
while True:
    t+=1
    picture = False

    #0. 회전시킨다
    temp = sushi.pop()
    sushi.insert(0, temp)


    #1-0. 명령이 하나도 남지 않았다면 탈출한다.
    if len(order_q) == 0 :
        break 

    #1. 명령수행
    #명령 큐에서 하나 꺼내고
    order = order_q.popleft()

    #시간이 일치하는지 확인한다
    #시간이 일치하지 않다면 다시 명령 큐 가장 앞부분에 넣는다

    if int(order[1]) != t :
        order_q.appendleft(order)
        continue #다음 시간으로 패스



    #시간이 일치한다면 명령을 수행한다
    if order[0] == '100':
        _, _, x, name = order
        # 1-1. 초밥을 올린다
        if sushi[int(x)] == ['empty']:
            sushi[int(x)] = [name]
        else:
            sushi[int(x)] += [name]
        sushi_num += 1

    elif order[0] == '200':
        _, _, x, name, n = order
        # 1-2. 손님이 입장한다
        ppl[int(x)] = name
        eat[int(x)] = int(n)
        ppl_num += 1

    elif order[0] == '300':
        _, _ = order
        # 1-3. 사진을 찍는다
        #명령 3번이라면 아래 행동을 먼저 수행한다
        picture = True

    # 손님과 초밥의 위치가 같다면
    # 먹이고, sushi에서 지우고, eat-1
    # eat이 0이된다면 ppl 리스트에서 지워준다

    for i in range(l):

        if ppl[i] in sushi[i] :
            cnt = 0
            #sushi에 ppl의 name을 가진 접시가 몇접시있는지 체크한다
            for j in range(len(sushi[i])):
                if sushi[i][j] == ppl[i]:
                    cnt += 1


            sushi_num -= cnt
            eat[i] -= cnt

            if cnt == len(sushi[i]) :
                sushi[i] = ['empty']

            else :
                for k in range(cnt):
                    sushi[i].remove(ppl[i])



            if eat[i] == 0:  # 사람이 정해진 양의 초밥을 먹으면
                ppl[i] = ''  # 떠난다
                ppl_num -= 1

    '''
    for i in range(l):

        #벨트에 초밥이 하나 있음
        if len(sushi[i]) == 1:
            if sushi[i][0] == ppl[i] : #초밥과 사람의 위치가 동일하다면
                sushi_num -= 1 #초밥을 하나 먹는다
                eat[i] -= 1
                sushi[i] = ['empty'] #벨트 위에 초밥이 없음

                if eat[i] == 0 : #사람이 정해진 양의 초밥을 먹으면
                    ppl[i] = '' #떠난다
                    ppl_num -= 1

        else :
            remove_lst = []
            #벨트에 초밥이 여러개 있을 때
            sushi_num = len(sushi[i])
            for j in range(len(sushi[i])) :
                # 초밥과 사람의 위치가 동일하다면
                print(sushi)
                print(ppl)
                print(j)
                if sushi[i][j] == ppl[i] :
                    sushi_num -= 1
                    eat[i] -= 1 #초밥을 하나 먹는다
                    remove_lst.append(sushi[i][j])
                    if len(remove_lst) == sushi_num:
                        sushi[i] = ['empty']
                    else:
                        sushi[i].remove(sushi[i][j]) #for문에서 remove는 쓰지 않는다

                    #사람이 정해진 양의 초밥을 먹으면
                    if eat[i] == 0 :
                        ppl[i] = ''
                        ppl_num -= 1
    '''




    #명령 3번이었다면
    if picture :
        #이제 촬영한다 (남아있는 사람수, 초밥수)
        print(ppl_num, end=' ')
        print(sushi_num)
        #남아있는 사람수, 초밥수가 0, 0 이라면 while 문을 탈출한다
        #if ppl_num == 0 and sushi_num == 0 :