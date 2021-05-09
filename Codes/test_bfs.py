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

class bfs_solver:
    def __init__(self, n, m, main_map):
        self.n, self.m = (n, m)
        self.main_map = main_map
        self.visited = [[set() for i in range(m)] for j in range(n)]
        self.par = [[{} for i in range(m)] for j in range(n)]
        self.st_cnt = 0

    def cell_is_good(self, i, j, balls_st):
        if cell_is_in_grid(self.n, self.m, i, j) == True and self.main_map[i][j] != '*'\
            and balls_st not in self.visited[i][j]:
            return True
        else:
            return False

    def test_reached(self, st, t, k):
        return st[LOC] == t and st[BALLS_ST].count(DELIVERED) == k

    def proc_state(self, st, q, t, c, k):
        self.st_cnt += 1
        
        if self.test_reached(st, t, k):
            return True
        cur_balls_st = st[BALLS_ST]
        map_cell = self.main_map[st[LOC][0]][st[LOC][1]]
        if map_cell[0] == '@':
            ball_idx = int(map_cell[1])
            if st[BALLS_ST][ball_idx] == CARRYING:
                new_balls_st = st[BALLS_ST][:ball_idx] + DELIVERED + st[BALLS_ST][ball_idx + 1:]
                par_st = self.par[st[LOC][0]][st[LOC][1]][st[BALLS_ST]]
                self.visited[st[LOC][0]][st[LOC][1]].add(new_balls_st)
                self.par[st[LOC][0]][st[LOC][1]][new_balls_st] = par_st
                cur_balls_st = new_balls_st
                
                self.st_cnt += 1
                if self.test_reached(st, t, k):
                    return True

        for d in DIRS:
            n_loc = tuple(map(add, list(st[LOC]), d))
            if self.cell_is_good(n_loc[0], n_loc[1], cur_balls_st):
                q.append((st[DIST] + 1, n_loc, cur_balls_st))
                self.par[n_loc[0]][n_loc[1]][cur_balls_st] = st
                self.visited[n_loc[0]][n_loc[1]].add(cur_balls_st)

        if map_cell[0] == '!':
            ball_idx = int(map_cell[1])
            if cur_balls_st[ball_idx] == UNGRABBED and st[BALLS_ST].count(CARRYING) < c:
                new_balls_st = cur_balls_st[:ball_idx] + CARRYING + cur_balls_st[ball_idx + 1:]
                if self.cell_is_good(st[LOC][0], st[LOC][1], new_balls_st):
                    q.append((st[DIST] + 1, st[LOC], new_balls_st))
                    self.par[st[LOC][0]][st[LOC][1]][new_balls_st] = st
                    self.visited[st[LOC][0]][st[LOC][1]].add(new_balls_st)
        
        return False

    def bfs(self, s, t, c, k):
        q = []
        q.append((0, s, UNGRABBED * k))
        self.par[s[0]][s[1]][UNGRABBED * k] = None
        self.visited[s[0]][s[1]].add(UNGRABBED * k)
        
        while len(q) > 0:
            st = q.pop(0)
            if self.proc_state(st, q, t, c, k) == True:
                print('found a path with dist={}'.format(st[DIST]))
                
                print('state count: total={0}, distinct={1}'.format(self.st_cnt, self.st_cnt))
                return st

        return None

def read_intlist(file):
    return [int(i) for i in file.readline().split()]

def print_map(map_):
    color_dict = {'-': 'grey', '*': 'white', '+': 'cyan', '!': 'yellow', '@': 'green'}
    for i in range(len(map_)):
        for j in range(len(map_[i])):
            print(colored(map_[i][j][0], color_dict[map_[i][j][0]], attrs=['bold']), end=' ')
        print()

def test_bfs(test_idx):
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
    
    # print_map(main_map)

    bsolv = bfs_solver(n ,m, main_map)
    t_st = bsolv.bfs(s, t, c, k)

    exec_time = time.time() - start_time

    cur_st = t_st
    path = []
    while (cur_st != None):
        path.append(cur_st)
        cur_st = bsolv.par[cur_st[LOC][0]][cur_st[LOC][1]][cur_st[BALLS_ST]]

    for s in path:
        main_map[s[LOC][0]][s[LOC][1]] = '+'

    while len(path) > 0:
        print(path[-1])
        path.pop()

    print()
    # print_map(main_map)

    return exec_time

for i in range(5):
    print(colored('Running test {}...'.format(i), 'yellow'))
    print('=' * 45)
    exec_time = test_bfs(i)
    print('=' * 45)
    print(colored('--- {} seconds ---'.format(exec_time), 'green'))
    print()