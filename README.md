# chess-gpt

# Requerimentos:
pip3 install torch
pip3 install numpy
pip3 install pygame

# Para executar o jogo:
python3 main.py

# Para escolher um oponente

No arquivo main.py as duas primeiras variáveis são oponent e player_white

oponent=0     # O jogador controla as peças brancas e pretas
oponent=1     # Jogar contra o chat GPT (Necessária uma api-key)
oponent=2     # Jogar contra o minimax + MLP
oponent=3     # Jogar contra o minimax + CNN

player_white=True     # O jogador joga com as peças brancas e o oponente com as pretas
player_white=False    # O jogador joga com as peças pretas e o oponente com as brancas

# Para jogar contra o Chat GPT 4
É necessário criar uma api key no site da open AI.
Após isso, criar um arquivo com o nome "api_key.txt" na pasta principal do projeto
e inserir apenas a api key no arquivo.
