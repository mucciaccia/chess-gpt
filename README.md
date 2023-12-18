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

Observação: A profundidade do minimax está configurada como 1 para que os oponentes executem
mais rápido. Porém as avaliações foram feitos com profundidade 7.

# Para jogar contra o Chat GPT 4
É necessário criar uma api key no site da open AI.
Após isso, criar um arquivo com o nome "api_key.txt" na pasta principal do projeto
e inserir apenas a api key no arquivo.

# Para treinar as redes neurais

O treinamento foi feito com o banco de dados de avaliação de partidas do lichess
que pode ser baixada por meio do link a seguir.

    https://database.lichess.org/lichess_db_eval.json.zst

Para treinar as redes é necessário fazer o download e descompactar o arquivo na pasta /data
Após isso é necessário descomentar as duas últimas linhas (dos dois scripts) e executar o script de treinamento

Para a MLP:

    python3 evaluator_MLP.py

E para a CNN:

    python3 evaluator_CNN.py



Obs: A ideia é fazer por reinforcement learning no futuro, para que os programas aprendam jogando contra eles mesmos,
após algumas tentativas percebi que isso é mais difícil que parece e acabei treinando os bots com dados de avaliação de 
partidas do lichess.
