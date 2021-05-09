import sys, time
from operator import add
from termcolor import colored
from colorama import init

init(autoreset=True)

UNGRABBED, CARRYING, DELIVERED = ('0', '1', '2')
DIRS = [[0, 1], [1, 0], [0, -1], [-1, 0]]
DIST, LOC, BALLS_ST = (0, 1, 2)

def cell_is_in_grid(n, m, i, j):
    if i >= n or i < 0:
        return False
    if j >= m or j < 0:
        return False

    return True

class iddfs_solver:
    def __init__(self, n, m, main_map):
        self.n, self.m = (n, m)
        self.main_map = main_map
        self.visited = [[{} for i in range(m)] for j in range(n)]
        self.par = [[{} for i in range(m)] for j in range(n)]
        self.st_cnt = 0

    def cell_is_good(self, i, j, balls_st, dist):
        if cell_is_in_grid(self.n, self.m, i, j) == True and self.main_map[i][j] != '*':
            if balls_st not in self.visited[i][j]:
                return True
            elif dist < self.visited[i][j][balls_st]:
                return True
            else:
                return False
        else:
            return False
    
    def test_reached(self, st, t, k):
        return st[LOC] == t and st[BALLS_ST].count(DELIVERED) == k

    def dfs(self, st, depth, t, c, k):
        # print('depth: {0}, cur: {1}'.format(depth, st))
        if depth < 0:
            return None
        
        self.st_cnt += 1

        if self.test_reached(st, t, k):
            return st
        
        self.visited[st[LOC][0]][st[LOC][1]][st[BALLS_ST]] = st[DIST]

        cur_balls_st = st[BALLS_ST]
        map_cell = self.main_map[st[LOC][0]][st[LOC][1]]
        if map_cell[0] == '@':
            ball_idx = int(map_cell[1])
            if st[BALLS_ST][ball_idx] == CARRYING:
                par_st = self.par[st[LOC][0]][st[LOC][1]][st[BALLS_ST]]
                cur_balls_st = st[BALLS_ST][:ball_idx] + DELIVERED + st[BALLS_ST][ball_idx + 1:]
                self.par[st[LOC][0]][st[LOC][1]][cur_balls_st] = par_st
                self.visited[st[LOC][0]][st[LOC][1]][cur_balls_st] = st[DIST]
                
                self.st_cnt += 1
                if self.test_reached(st, t, k):
                    return st
        
        for d in DIRS:
            n_loc = tuple(map(add, list(st[LOC]), d))
            if self.cell_is_good(n_loc[0], n_loc[1], cur_balls_st, st[DIST] + 1):
                new_st = (st[DIST] + 1, n_loc, cur_balls_st)
                self.par[n_loc[0]][n_loc[1]][cur_balls_st] = st
                res = self.dfs(new_st, depth - 1, t, c, k)
                if res != None:
                    return res
                
        if map_cell[0] == '!':
            ball_idx = int(map_cell[1])
            if st[BALLS_ST][ball_idx] == UNGRABBED and st[BALLS_ST].count(CARRYING) < c:
                new_balls_st = cur_balls_st[:ball_idx] + CARRYING + cur_balls_st[ball_idx + 1:]
                if self.cell_is_good(st[LOC][0], st[LOC][1], new_balls_st, st[DIST] + 1):
                    new_st = (st[DIST] + 1, st[LOC], new_balls_st)
                    self.par[st[LOC][0]][st[LOC][1]][new_balls_st] = st
                    res = self.dfs(new_st, depth - 1, t, c, k)
                if res != None:
                    return res

        return None

    def iddfs(self, s, t, c, k):
        st = (0, s, UNGRABBED * k)
        self.par[s[0]][s[1]][st[BALLS_ST]] = None

        for i in range(100):
            print('depth: {}'.format(i), end='\r')
            self.visited = [[{} for i in range(self.m)] for j in range(self.n)]
            res = self.dfs(st, i, t, c, k)
            
            if res != None:
                print()
                print('found path at dist={}'.format(i))
                
                dist_st_cnt = 0
                for i in range(self.n):
                    for j in range(self.m):
                        dist_st_cnt += len(self.par[i][j])
                print('state count: total={0}, distinct={1}'.format(self.st_cnt, dist_st_cnt))
                
                return res

        return None

def read_intlist(file):
    return [int(i) for i in file.readline().split()]

def print_map(map_):
    color_dict = {'-': 'grey', '*': 'white', '+': 'cyan', '!': 'yellow', '@': 'green'}
    for i in range(len(map_)):
        for j in range(len(map_[i])):
            print(colored(map_[i][j][0], color_dict[map_[i][j][0]], attrs=['bold']), end=' ')
        print()

def test(test_idx):
    start_time = time.time()
    test = open('../Tests/' + str(test_idx) + '.txt', 'r')
    n, m = read_intlist(test)
    s = tuple(read_intlist(test))
    t = tuple(read_intlist(test))
    c = int(test.readline())
    k = int(test.readline())

    main_map = [['$' for j in range(m)] for i in range(n)]

    ball_locs = []
    for i in range(k):
        line = [int(j) for j in test.readline().split()]
        ball_locs.append(line)

    for i in range(n):
        row = test.readline().split()
        for j in range(m):
            main_map[i][j] = row[j]

    for i in range(k):
        b_loc = ball_locs[i]
        main_map[b_loc[0]][b_loc[1]] = '!' + str(i)
        main_map[b_loc[2]][b_loc[3]] = '@' + str(i)
    
    isolv = iddfs_solver(n, m, main_map)
    t_st = isolv.iddfs(s, t, c, k)

    exec_time = time.time() - start_time

    cur_st = t_st
    path = []
    while cur_st != None:
        path.append(cur_st)
        cur_st = isolv.par[cur_st[LOC][0]][cur_st[LOC][1]][cur_st[BALLS_ST]]

    for st in path:
        main_map[st[LOC][0]][st[LOC][1]] = '+'

    while len(path) > 0:
        print(path[-1])
        path.pop()

    print()
    # print_map(main_map)
    
    return exec_time

for i in range(5):
    print(colored('Running test {}...'.format(i), 'yellow'))
    print('=' * 45)
    exec_time = test(i)
    print('=' * 45)
    print(colored('--- {} seconds ---'.format(exec_time), 'green'))
    print()