import sys

N = 0
b = 0
subblock_height = 0
subblock_width = 0
symbol_set = ""
mydict = {}

def print_puzzle(puzzle):
    for i in range(0, len(puzzle), N):
        if int(i/N)%subblock_height == 0:
            if N == 9 or N == 10:
                print("-------------------------")
            elif N == 16:
                print("-----------------------------------------")
            elif N == 12:
                print("-------------------------------")
            elif N == 15: 
                print("-------------------------------------")
            elif N == 8:
                print("---------------------")
            elif N == 6:
                print("-----------------")
        for j in range(N):
            if j%subblock_width == 0:
                print("| " + puzzle[i+j] + " ", end = '')
            else: 
                print(puzzle[i+j] + " ", end = '')
        print("| ", end = '')
        print("")
    if N == 9 or N == 10:
        print("-------------------------")
    elif N == 16:
        print("-----------------------------------------")
    elif N == 12:
        print("-------------------------------")
    elif N == 15: 
        print("-------------------------------------")
    elif N == 8:
        print("---------------------")
    elif N == 6:
        print("-----------------")
    print("")

def create_dict():
    rows = []
    cols = []
    blocks = []
    blockshelp = []

    [rows.append([j+(i*N) for j in range(N)]) for i in range(N)]
    [cols.append([i+(j*N) for j in range(N)]) for i in range(N)]
    for i in range(0, N, subblock_height):
        for j in range(0, N, subblock_width):
            for p in range(0, subblock_height):
                blockshelp.append([k+(N*p)+(N*i) for k in range(j, j+subblock_width)])
    for i in range(0, N):
        blocks.append(blockshelp[i*subblock_height])
        for j in range(1, subblock_height):
            blocks[i].extend(blockshelp[i*subblock_height+j])

    for i in range(0, N*N):
        mylist = []
        for j in rows:
            if i in j:
                mylist.append(j)
        for j in cols:
            if i in j:
                mylist.append(j)
        for j in blocks:
            if i in j:
                mylist.append(j)
        mydict[i] = mylist

    return mydict

def get_next_unassigned_var(state):
    return state.index(".")

def get_sorted_vals(state, var):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    vals = []
    for i in range(1, N+1):
        o = 0
        if i <= 9:
            o = i
        else:
            o = letters[abs(i-N)]
        row = mydict[var][0]
        col = mydict[var][1]
        box = mydict[var][2]
        num = 0
        for j in row:
            if state[j] != '.':
                if state[j] not in letters:
                    if int(state[j]) == o and j != var:
                        num+=1
                else:
                    if state[j] == o and j != var:
                        num+=1
        for j in col:
            if state[j] != '.':
                if state[j] not in letters:
                    if int(state[j]) == o and j != var:
                        num+=1
                else:
                    if state[j] == o and j != var:
                        num+=1
        for j in box:
            if state[j] != '.':  
                if state[j] not in letters:
                    if int(state[j]) == o and j != var:
                        num+=1
                else:
                    if state[j] == o and j != var:
                        num+=1
        if num == 0:
            vals.append(o)
    return vals

def goal_test(state):
    if "." in state:
        return False
    return True

def csp_backtracking(state):
    if goal_test(state): return state
    var = get_next_unassigned_var(state)
    for val in get_sorted_vals(state, var):
        new_state = state
        new_state = new_state[:var] + str(val) + new_state[var+1:]
        result = csp_backtracking(new_state)
        if result is not None:
            return result
    return None

count = 0
with open(sys.argv[1]) as f:
    line_list = [line.strip() for line in f]
for line in line_list:
    if count < 1000000:
        symbol_set = line
        N = int(len(symbol_set)**(1/2))
        a = N**(1/2)
        b = int(a)
        if b*b == N:
            subblock_width = b
            subblock_height = b
        else:
            for i in range(b+1, N):
                if N % i == 0:
                    subblock_width = i
                    break
            for j in range(b, 0, -1):
                if N % j == 0:
                    subblock_height = j
                    break
        #print(symbol_set)
        create_dict()
        print(csp_backtracking(symbol_set))
        count+=1

