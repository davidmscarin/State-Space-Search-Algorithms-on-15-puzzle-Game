import numpy as np
import heapq
import sys
import time
from collections import deque


#constantes
ROWS = 4
COLS = 4

class State:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent if isinstance(parent, State) else None

#estrutura do puzzle
class Puzzle:
    def __init__(self, initial_state, final_state): #construtor da classe
        self.initial_state = np.array(initial_state).reshape((ROWS, COLS))
        self.final_state = np.array(final_state).reshape((ROWS, COLS))
    
    def is_even(self, n): #verifica se um inteiro n e par
        return n%2==0

    def solvable(self):  # verificar se e possivel alcancar o estado final do estado inicial

        row_initial,col_initial = np.argwhere(self.initial_state == 0)[0]
        row_final,col_final = np.argwhere(self.final_state == 0)[0]

        initial = self.initial_state.flatten()
        final = self.final_state.flatten()

        sum_initial = 0
        sum_final = 0


        for i in range(len(initial) - 1):
            for j in range(i, len(initial)):
                if initial[j] < initial[i] and initial[j] != 0:
                    sum_initial += 1
                if final[j] < final[i] and final[j] != 0:
                    sum_final += 1

        #Condition initial
        if self.is_even(sum_initial) != self.is_even(row_initial):
            cond_initial = True
        else:
            cond_initial = False
        if self.is_even(sum_final) != self.is_even(row_final):
            cond_final = True
        else:
            cond_final = False
        if cond_initial == cond_final:
            print("E possivel alcancar o estado final dado este estado inicial")
            return
        print("Nao e possivel alcancar o estado final dado este estado inicial")
        exit()


    def is_goal_state(self, state): #verifica se um dado estado e o estado objetivo
        return np.array_equal(state, self.final_state)
    
    def get_states(self, state): #dada uma configuracao do tabuleiro retorna todos os estados possiveis a partir dela
        possible_states = []
        row0, col0 = np.argwhere(state == 0)[0]

        if row0+1<=3:
            new_state = np.copy(state)
            new_state[row0][col0] = new_state[row0+1][col0]
            new_state[row0+1][col0] = 0
            possible_states.append(new_state)
        
        if row0-1>=0:
            new_state = np.copy(state)
            new_state[row0][col0] = new_state[row0-1][col0]
            new_state[row0-1][col0] = 0
            possible_states.append(new_state)
        
        if col0+1<=3:
            new_state = np.copy(state)
            new_state[row0][col0] = new_state[row0][col0+1]
            new_state[row0][col0+1] = 0
            possible_states.append(new_state)
        
        if col0-1>=0:
            new_state = np.copy(state)
            new_state[row0][col0] = new_state[row0][col0-1]
            new_state[row0][col0-1] = 0
            possible_states.append(new_state)
        
        return possible_states
    

    def misplaced(self, state): #o numero de pecas "fora do sitio"
        count = 0
        for i in range(ROWS):
            for j in range(COLS):
                if state[i][j] != self.final_state[i][j]:
                    count += 1
        return count
    
    def manhattan(self, state): #manhattan distance
        final_state = self.final_state
        distance = 0

        for i in range(ROWS):
            for j in range(COLS):
                x, y = np.argwhere(final_state==state[i][j])[0]
                distance+=abs(x-i)+abs(y-j)
        
        return distance
    
    def dfs(self, max_depth):
        stack = [(State(self.initial_state), 0)]
        visited = set()
        nodes_in_memory = 1

        while stack:
            current_state, steps = stack.pop()
            visited.add((tuple(current_state.state.flatten()), steps))
            nodes_in_memory = max(nodes_in_memory, len(visited)+len(stack))

            if self.is_goal_state(current_state.state):
                path = [current_state.state]
                while current_state.parent:
                    current_state = current_state.parent
                    path.append(current_state.state)
                path.reverse()
                print("Solucao encontrada em", steps, "passos.")
                print("Numero maximo de nos em memoria:", nodes_in_memory)
                return path

            if steps < max_depth:
                for new_state in self.get_states(current_state.state):
                    if (tuple(new_state.flatten()), steps+1) not in visited:
                        new_state = State(new_state, parent=current_state)
                        stack.append((new_state, steps+1))

        return None
    
    def bfs(self, max_depth):
        queue = deque([(State(self.initial_state), 0)])
        visited = set()
        nodes_in_memory = 1

        while queue:
            current_state, steps = queue.popleft()
            visited.add(tuple(current_state.state.flatten()))
            nodes_in_memory = max(nodes_in_memory, len(visited)+len(queue))

            if self.is_goal_state(current_state.state):
                path = [current_state.state]
                while current_state.parent:
                    current_state = current_state.parent
                    path.append(current_state.state)
                path.reverse()
                print("Solucao encontrada em", steps, "passos")
                print("Numero maximo de nos em memoria:", nodes_in_memory)
                return path

            if steps<max_depth:
                for new_state in self.get_states(current_state.state):
                    if tuple(new_state.flatten()) not in visited:
                        new_state = State(new_state, parent= current_state)
                        queue.append((new_state, steps+1))
                        
        return None
    

    def idfs(self, max_depth):
        for depth in range(max_depth+1):
            result = self.dfs(depth)
            if result is not None:
                return result
        return None
    

    def greedy_misplaced(self, max_depth):
        queue = [(self.misplaced(self.initial_state), 0, id(self.initial_state), State(self.initial_state))]
        visited = set()
        nodes_in_memory = 1

        while queue:
            h, steps, state_id, current_state = heapq.heappop(queue)
            visited.add(tuple(current_state.state.flatten()))
            nodes_in_memory = max(nodes_in_memory, len(visited)+len(queue))

            if self.is_goal_state(current_state.state):
                path = [current_state.state]
                while current_state.parent:
                    current_state = current_state.parent
                    path.append(current_state.state)
                print("Solucao encontrada em", steps, "passos")
                print("Numero maximo de nos em memoria:", nodes_in_memory)
                return path

            if steps<max_depth:
                for new_state in self.get_states(current_state.state):
                    if tuple(new_state.flatten()) not in visited:
                        new_state = State(new_state, parent=current_state)
                        heapq.heappush(queue, (self.misplaced(new_state.state), steps+1, id(new_state.state), new_state))

        return None
    
    def greedy_manhattan(self, max_depth):
        queue = [(self.manhattan(self.initial_state), 0, id(self.initial_state), State(self.initial_state))]
        visited = set()
        nodes_in_memory = 1        

        while queue:
            h, steps, state_id, current_state = heapq.heappop(queue)
            visited.add(tuple(current_state.state.flatten()))
            nodes_in_memory = max(nodes_in_memory, len(visited)+len(queue))

            if self.is_goal_state(current_state.state):
                path = [current_state.state]
                while current_state.parent:
                    current_state = current_state.parent
                    path.append(current_state.state)
                print("Solucao encontrada em", steps, "passos")
                print("Numero maximo de nos em memoria:", nodes_in_memory)
                return path

            if steps<max_depth:
                for new_state in self.get_states(current_state.state):
                    if tuple(new_state.flatten()) not in visited:
                        new_state = State(new_state, parent=current_state)
                        heapq.heappush(queue, (self.manhattan(new_state.state), steps+1, id(new_state.state), new_state))

        return None
        

    def astar_misplaced(self, max_depth):
        priority_queue = [(self.misplaced(self.initial_state), 0, id(self.initial_state), State(self.initial_state))]
        visited = set()
        nodes_in_memory = 1

        while priority_queue:
            f, steps, state_id, current_state = heapq.heappop(priority_queue)
            visited.add(tuple(current_state.state.flatten()))
            nodes_in_memory = max(nodes_in_memory, len(visited)+len(priority_queue))

            if self.is_goal_state(current_state.state):
                path = [current_state.state]
                while current_state.parent:
                    current_state = current_state.parent
                    path.append(current_state.state)
                path.reverse()
                print("Solucao encontrada em", steps, "passos")
                print("Numero maximo de nos em memoria:", nodes_in_memory)
                return path

            if steps < max_depth:
                for new_state in self.get_states(current_state.state):
                    if tuple(new_state.flatten()) not in visited:
                        new_state = State(new_state, current_state)
                        g = steps + 1
                        h = self.misplaced(new_state.state)
                        f = g + h
                        heapq.heappush(priority_queue, (f, g, id(new_state.state), new_state))

        return None

    def astar_manhattan(self, max_depth):
        priority_queue = [(self.manhattan(self.initial_state), 0, id(self.initial_state), State(self.initial_state))]
        visited = set()
        nodes_in_memory = 1

        while priority_queue:
            f, steps, state_id, current_state = heapq.heappop(priority_queue)
            visited.add(tuple(current_state.state.flatten()))
            nodes_in_memory = max(nodes_in_memory, len(visited)+len(priority_queue))

            if self.is_goal_state(current_state.state):
                path = [current_state.state]
                while current_state.parent:
                    current_state = current_state.parent
                    path.append(current_state.state)
                path.reverse()
                print("Solucao encontrada em", steps, "passos")
                print("Numero maximo de nos em memoria:", nodes_in_memory)
                return path

            if steps < max_depth:
                for new_state in self.get_states(current_state.state):
                    if tuple(new_state.flatten()) not in visited:
                        new_state = State(new_state, current_state)
                        g = steps + 1
                        h = self.manhattan(new_state.state)
                        f = g + h
                        heapq.heappush(priority_queue, (f, g, id(new_state.state), new_state))

        return None

 

#obter argumentos da command line para a estrategia e o ficheiro de input e inicializar o objeto puzzle:

filename = sys.argv[2] #ficheiro de input

#inicializar objeto puzzle
with open(filename, "r") as file:
    initial_state = list(map(int, file.readline().split()))
    final_state = list(map(int, file.readline().split()))

initial_state = np.array(initial_state).reshape(ROWS, COLS)
final_state = np.array(final_state).reshape(ROWS, COLS)

print("Estado inicial:\n", initial_state)
print("Estado final:\n", final_state)

puzzle = Puzzle(initial_state, final_state)
puzzle.solvable() #antes de fazer qualquer pesquisa, verificar se o problema tem solucao

prompt = sys.argv[1] #obter a pesquisa a ser realizada

start_time = time.time()

#executar a estrategia pedida:

if prompt=="DFS":
    print("Algoritmo DFS com profundidade maxima 12:")
    path = puzzle.dfs(12)
    if path is not None:
        print("Solucao encontrada dentro da profundida maxima. Estados do jogo:")
        for state in path:
            print(state)
    else:
        print("Solucao nao encontrada na profunidade especificada")

elif prompt=="BFS":
    print("Algoritmo BFS com profundidade maxima 12:")
    path = puzzle.bfs(12)
    if path is not None:
        print("Solucao encontrada dentro da profundida maxima. Estados do jogo:")
        for state in path:
            print(state)
    else:
        print("Solucao nao encontrada na profunidade especificada")


elif prompt=="IDFS":
    print("Algoritmo IDFS com profundidade maxima 12:")
    path = puzzle.idfs(12)
    if path is not None:
        for state in path:
            print(state)
    else:
        print("Solucao nao encontrada na profunidade especificada")


elif prompt=="Greedy-Misplaced":
    print("Algoritmo Greedy com heuristica misplaced e profundidade maxima 12:")
    path = puzzle.greedy_misplaced(12)
    if path is not None:
        print("Solucao encontrada dentro da profundida maxima. Estados do jogo:")
        for state in path:
            print(state)
    else:
        print("Solucao nao encontrada na profunidade especificada")


elif prompt=="Greedy-Manhattan":
    print("Algoritmo Greedy com heuristica manhattan e profundidade maxima 12:")
    path = puzzle.greedy_manhattan(12)
    if path is not None:
        print("Solucao encontrada dentro da profundida maxima. Estados do jogo:")
        for state in path:
            print(state)
    else:
        print("Solucao nao encontrada na profunidade especificada")

elif prompt=="A*-Misplaced":
    print("Algoritmo A* com heuristica misplaced e profundidade maxima 12:")
    path = puzzle.astar_misplaced(12)
    if path is not None:
        print("Solucao encontrada dentro da profundida maxima. Estados do jogo:")
        for state in path:
            print(state)
    else:
        print("Solucao nao encontrada na profunidade especificada")

elif prompt=="A*-Manhattan":
    print("Algoritmo A* com heuristica manhattan e profundidade maxima 12:")
    path = puzzle.astar_manhattan(12)
    if path is not None:
        print("Solucao encontrada dentro da profundida maxima. Estados do jogo:")
        for state in path:
            print(state)
    else:
        print("Solucao nao encontrada na profunidade especificada")

end_time = time.time()
print("Runtime =", end_time-start_time, "segundos") #tempo que o programa demorou a executar