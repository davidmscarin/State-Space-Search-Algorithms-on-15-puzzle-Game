Algoritmos de pesquisa no 15 Puzzle Game

- Este script de Python implementa os algoritmos de pesquisa Depth-First Search, Breadth-First Search, Iterative Deepening Depth-First Search, Greedy Search e A* (com heuristicas Misplaced e Manhattan)

Para executar o programa:
- certificar-se que está no diretório correto
- tem instalado na máquina o interpretador de Pythonno
- no mesmo diretório estão os ficheiros "15puzzle.py" e "input.txt"
- no ficheiro "input.txt" o texto esta estruturado da forma:
"1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0
1 2 3 4 5 6 7 8 9 10 11 12 13 14 0 15"
em as linhas são, respetivamente, a configuração inicial e final do tabuleiro

executar na linha de comandos um comando do seguinte tipo:
"python 15puzzle.py <algoritmo_de_pesquisa> <ficheiro_de_input>"

Ex: "python 15puzzle.py DFS input.txt" executa o programa com uma pesquisa Depth-First Search recebendo o input do ficheiro "input.txt"

No terminal serão impressos pela seguinte ordem:

- Os estados inicial e final que foram dados no input do programa
- Uma mensagem afirmando que é ou não possível chegar do estado inicial ao final
- Uma mensagem com o algoritmo que está a ser aplicado e qual a sua profundidade máxima
- Uma mensagem quando o algoritmo encontrar o estado objetivo e o número de passos necessários para tal
- Representação do "caminho" que leva o tabuleiro desde o estado inicial até ao final
- O tempo de execução do programa
