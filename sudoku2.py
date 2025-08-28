import sys
 
N = 0
b = 0
subblock_height = 0
subblock_width = 0
symbol_set = ""
rows = []
cols = []
blocks = []
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
 
def print_board(state):
    x = len(state)
    for i in range(0, x):
        for j in range(0, x):
            print(state[i+j], end=' ')
        print()
    return state
 
def create_dict():
    rows = []
    cols = []
    blocks = []
    blockshelp = []
 
    [rows.append([j+(i*N) for j in range(N)]) for i in range(N)]
    [cols.append([i+(j*N) for j in range(N)]) for i in range(N)]
    # for i in range(0, N):
    #     nlist = list()
    #     blocks.append(nlist)
    # for i in range(0, len(symbol_set), N):
    #     for j in range(0, N, subblock_width):
    #         for k in range(j, j+subblock_width):
    #             blocks[int(i/(N*subblock_height))*subblock_height+int(j/subblock_width)].append(i+k)
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
                break
        for j in cols:
            if i in j:
                mylist.append(j)
                break
        for j in blocks:
            if i in j:
                mylist.append(j)
                break
        mydict[i] = mylist
    return rows, cols, blocks
 
def get_most_constrained_var(state):
    const = N
    for i in range(0, len(state)):
        if len(state[i]) > 1 and len(state[i]) < const:
            const = i
    return const
 
def get_sorted_vals(state, var):
    vals = []
    for i in state[var]:
        vals.append(i)
    return vals
 
def forward_helper(state):
    biglist = []
    for var in range(0, len(state)):
        if state[var] == '.':
            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            vals = []
            for i in range(1, N+1):
                o = 0
                if i <= 9:
                    o = i
                else:
                    o = letters[abs(i-N)]
                vals.append(str(o))
            biglist.append("".join(vals))
        else:
            biglist.append(state[var])
    solved = []
    for i in range(0, len(biglist)):
        if len(biglist[i]) == 1:
            solved.append(i)
    return biglist, solved
 
def forward_looking(state, indices):
    cor = indices
    while len(cor) != 0:
        var = cor[0]
        row = mydict[var][0]
        col = mydict[var][1]
        box = mydict[var][2]
        for j in row:
            if state[var] in state[j] and var != j:
                nst = state[j].index(state[var])
                state[j] = state[j][0:nst:] + state[j][nst+1::]
                if len(state[j]) == 1:
                    cor.append(j)
                elif len(state[j]) == 0:
                    return None
        for j in col:
            if state[var] in state[j] and var != j:
                nst = state[j].index(state[var])
                state[j] = state[j][0:nst:] + state[j][nst+1::]
                if len(state[j]) == 1:
                    cor.append(j)
                elif len(state[j]) == 0:
                    return None
        for j in box:
            if state[var] in state[j] and var != j:
                nst = state[j].index(state[var])
                state[j] = state[j][0:nst:] + state[j][nst+1::]
                if len(state[j]) == 1:
                    cor.append(j)
                elif len(state[j]) == 0:
                    return None
        cor.pop(0)
    return state
 
def constraint_propogation(state):
    changes = []
    if state is None:
        return None, None
    for i in range(0, len(rows)):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for j in range(1, N+1):
            num = 0
            num2 = 0
            num3 = 0
            index = 0
            o = 0
            if j <= 9:
                o = str(j)
            else:
                o = letters[abs(j-N)]
            for k in rows[i]:
                if o in state[k]:
                    if len(state[k]) > 1:
                        num+=1
                        num2+=1
                        index = k
                    else:
                        num2+=1
                        num3+=1
            if num == 1 and num3 < 1:
                state[index] = o
                changes.append(index)
            if num2 == 0:
                return None, None
    for i in range(0, len(cols)):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for j in range(1, N+1):
            num = 0
            num2 = 0
            num3 = 0
            index = 0
            o = 0
            if j <= 9:
                o = str(j)
            else:
                o = letters[abs(j-N)]
            for k in cols[i]:
                if o in state[k]:
                    if len(state[k]) > 1:
                        num+=1
                        num2+=1
                        index = k
                    else:
                        num2+=1
                        num3+=1
            if num == 1 and num3 < 1:
                state[index] = o
                changes.append(index)
            if num2 == 0:
                return None, None
    for i in range(0, len(blocks)):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for j in range(1, N+1):
            num = 0
            num2 = 0
            num3 = 0
            index = 0
            o = 0
            if j <= 9:
                o = str(j)
            else:
                o = letters[abs(j-N)]
            for k in blocks[i]:
                if o in state[k]:
                    if len(state[k]) > 1:
                        num+=1
                        num2+=1
                        index = k
                    else:
                        num2+=1
                        num3+=1
            if num == 1 and num3 < 1:
                state[index] = o
                changes.append(index)
            if num2 == 0:
                return None, None
    return state, changes
 
def goal_test(state):
    for i in state:
        if len(i) > 1:
            return False
    return True

def solve_help(state, index):
    s = index
    check = state
    while len(s) > 0 and s != None:
        current_state = check
        if current_state is not None:
            current_state = forward_looking(current_state, s)
            if current_state == None:
                s = None
        if current_state is not None:
            check, s = constraint_propogation(current_state)
        if check == None or s == None:
            return None
    return current_state
 
def backtrack_with_forward_looking(state):
    if goal_test(state): return state
    var = get_most_constrained_var(state)
    for val in get_sorted_vals(state, var):
        new_state = state.copy()
        new_state[var] = val
        checked_state = solve_help(new_state, [var])
        if checked_state is not None:
            result = backtrack_with_forward_looking(checked_state)
            if result is not None:
                return result
    return None
 
count = 0
with open(sys.argv[1]) as f:
    line_list = [line.strip() for line in f]
for line in line_list:
    if count < 100000:
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
        rows, cols, blocks = create_dict()
        suppl, solved = forward_helper(symbol_set)
        suppl2 = forward_looking(suppl, solved)
        print("".join(backtrack_with_forward_looking(suppl2)))
        count+=1
 
# The Plan
#
# Cons.Prop. returns a list of solved squares in the process instead of "changes" CHECK
#
# Forward looking pass in a list of specific indices to work with CHECK
#
# Forward helper change so that it runs initial call of forward looking with the initial number/letter values CHECK
#
# Solve function works so that while the length of the list that cons.prop. produces isn't empty,
# it runs forward looking, but runs forward looking first
#
 
 
 
