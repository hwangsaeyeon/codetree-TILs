'''

트리: 동적 노드 추가, 색깔 변경 명령을 처리할 수 있음
처음에는 아무 노드 없음

(1) 노드 추가
- m(고유번호), p(부모노드번호), c(색깔), max(최대깊이)
- color (1~5) 빨주노초파
- if p == -1 : 새로운 트리의 루트 노드
- max는 서브트리의 최대 깊이, 자기자신 == 1
- max 모순 발생 -> 현재 노드는 추가하지 않음 **

(2) 색 변경
- m을 루트로하는 서브트리의 모든 노드의 색깔을 변경

(3) 색 조회
- m의 현재 색 조회

(4) 점수 조회
- 모든 노드의 가치를 계산, 가치 제곱의 합 출력
- 각 노드의 가치 : 해당 노드를 루트로하는 서브트리 내 서로 다른 색의 수
'''

from copy import deepcopy

def color_change(visited,m,c):
    for node in tree[m]:
        if not visited[node]:
            info[node][0] = c
            visited[node] = True
            color_change(visited,node,c)

def cal_value(visited, node, values, color_check):
    for j in tree[node]:
        if not visited[j]:
            if info[j][0] not in color_check:
                color_check.append(info[j][0])
                values += 1

            visited[j] = True
            values = cal_value(visited, j, values, color_check)

    return values




Q = int(input())
info, tree = dict(), dict()
for _ in range(Q):
    orders = list(map(int, input().split()))
    if orders[0] == 100:

        m,p,c,d = orders[1:] #id, parent, color, max_depth

        #parent가 본인인 경우
        if p == -1 :
            tree[m] = [m]
            info[m] = [c,p,d]

        else :
            #깊이 check
            cur_depth = 1
            check_node = m
            parent = p
            check = True
            while parent != -1:
                # 깊이+1 > 부모 노드의 최대 깊이 라면 check=False
                if cur_depth + 1 > info[parent][2] :
                    check = False
                    break
                parent = info[parent][1]
                cur_depth += 1

            if check:
                tree[m] = [m]
                tree[p].append(m)
                info[m] = [c, p, d]


    elif orders[0] == 200:
        m,c = orders[1:]
        visited = dict()
        for key in info.keys():
            visited[key] = False
        color_change(visited,m,c)


    elif orders[0] == 300:
        m = orders[1]
        print(info[m][0])


    elif orders[0] == 400:
        value_sum = 0

        #for key in info.keys():
        #    visited[key] = False

        for i in tree.keys():
            visited = dict()
            #print('n번 노드 탐색:',i)
            visited = [False for _ in range(100000)]
            values = cal_value(visited, i, 0, [])
            #print(i,'번 노드 value:',values)
            value_sum += (values) ** 2

        print(value_sum)