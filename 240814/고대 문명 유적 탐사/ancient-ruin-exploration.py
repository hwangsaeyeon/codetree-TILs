from copy import deepcopy

def rotation(i, j, arr): #중심 좌표(i,j)
    new = [[0 for _ in range(5)] for _ in range(5)]
    rotated = deepcopy(arr)

    for y in range(i-1, i+2):
        for x in range(j-1, j+2):
            oy, ox = y-i+1, x-j+1
            ry, rx = ox, 3-oy-1
            new[i-1+ry][j-1+rx] = arr[y][x]

    for r in range(i-1,i+2):
        for c in range(j-1,j+2):
            rotated[r][c] = new[r][c]

    return rotated

def explore(arr):
    ans= 0
    finxy = []
    fin = []
    #회전 각도가 가장 우선
    for col in range(1,4): #중심점
        for row in range(1,4):
            new = rotation(row, col, arr)
            val, xys= get_ruins(new)

            if val > ans :
                ans = val
                finxy = xys
                fin = new

    #180도
    for col in range(1,4):
        for row in range(1,4):
            new = rotation(row, col, arr)
            new = rotation(row, col, new)
            val, xys = get_ruins(new)

            if val > ans :
                ans = val
                finxy = xys
                fin = new

    #270도 회전
    for col in range(1, 4):
        for row in range(1, 4):
            new = rotation(row, col, arr)
            new = rotation(row, col, new)
            new = rotation(row, col, new)
            val, xys = get_ruins(new)

            if val > ans :
                ans = val
                finxy = xys
                fin = new




    return ans, finxy, fin

def is_inrange(x,y):
    return 0<=x<5 and 0<=y<5
def recur(x,y,val,xy,visited,new):
    cnt = 0
    for i in range(5):
        cnt += sum(visited[i])

    if cnt == 25:
        return val, xy

    dx, dy = [-1,1,0,0], [0,0,-1,1]
    for d in range(4):
        nx, ny = x+dx[d], y+dy[d]
        if is_inrange(nx,ny) and visited[nx][ny] == 0 and new[nx][ny] == new[x][y]:
            visited[nx][ny] = 1
            val, xy = recur(nx, ny, val+1, xy+[(nx,ny)], visited,new)

    return val, xy
def get_ruins(new):
    visited = [[0]*5 for _ in range(5)]
    total = 0
    fin_xy = []

    for i in range(5):
        for j in range(5):
            xy = [(i,j)]
            visited[i][j] = 1

            val, coordinate = recur(i,j,1,xy,visited,new)

            if val >= 3 : #연속되는 유적지가 3개 이상
                total += val

                fin_xy += coordinate

    return total, fin_xy

#arr = [[7,6,7,6,7],[6,7,6,7,6],[6,7,1,5,4],[7,6,3,2,1],[5,4,3,2,7]]
#print(explore(arr))

def replace(ans, finxy, arr, hubo):
    replace_total = 0

    while ans >= 3: #3개 연속일때 까지
        finxy.sort(key=lambda x: (x[1], -x[0]))
        for i in range(ans):
            arr[finxy[i][0]][finxy[i][1]] = hubo[i]

        hubo = hubo[ans:]
        ans, finxy = get_ruins(arr)
        replace_total += ans



    return arr, hubo, replace_total

def main():
    global M
    K, M = map(int, input().split())
    arr = []
    for _ in range(5):
        arr.append(list(map(int, input().split())))

    hubo = (list(map(int, input().split())))

    for _ in range(K):
        #유물탐사, 유물획득
        ans, finxy, arr = explore(arr)
        if ans == 0 : # 유물을 획득할 수 없음
            break

        #조각 채우기
        arr, hubo, replace_total = replace(ans, finxy, arr, hubo)
        # 더 이상 유물이 발견이 되지 않음
        print(ans+replace_total, end=" ")



if __name__ == "__main__" :
   main()