import json
import torch

class EvalReader():

    def __init__(self):
        self.file = open("./data/lichess_db_eval.json", "r")

    def __del__(self):
        self.file.close()

    def piece_to_dimension(piece):
        dim = {
            'K': 0,
            'Q': 1,
            'R': 2,
            'B': 3,
            'N': 4,
            'P': 5,
            'k': 6,
            'q': 7,
            'r': 8,
            'b': 9,
            'n': 10,
            'p': 11
        }
        return dim[piece]

    def fen_to_tensor(fen_str):
        tensor = torch.zeros([8, 8, 12])

        i = 0
        j = 0
        for c in fen_str:
            if c == "/":
                i += 1
                j = 0
            elif c in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
                j += int(c)
            elif c == " ":
                break
            else:
                d = EvalReader.piece_to_dimension(c)
                tensor[i, j, d] = 1
                j += 1
        return tensor
    
    def get_n(self, n : int):
        y = torch.zeros(n)

        tensor_list = []
        i = 0
        while i < n:
            line = self.file.readline()
            line_json = json.loads(line)

            fen_str = line_json['fen']
            eval = line_json['evals'][0]['pvs'][0].get('cp')

            if eval is None:
                mate = line_json['evals'][0]['pvs'][0]['mate']
                if mate > 0:
                    eval = 1000
                else:
                    eval = -1000

            tensor = EvalReader.fen_to_tensor(fen_str)
            tensor_list.append(tensor.reshape([768]).squeeze())
            y[i] = torch.tensor(eval)
            i += 1

        x = torch.stack(tensor_list)
        return x, y
        
    def get_cnn(self, n : int):
        y = torch.zeros(n)

        tensor_list = []
        i = 0
        while i < n:
            line = self.file.readline()
            line_json = json.loads(line)

            fen_str = line_json['fen']
            eval = line_json['evals'][0]['pvs'][0].get('cp')

            if eval is None:
                mate = line_json['evals'][0]['pvs'][0]['mate']
                if mate > 0:
                    eval = 1000
                else:
                    eval = -1000

            tensor = EvalReader.fen_to_tensor(fen_str).permute(2, 0, 1).squeeze()
            tensor_list.append(tensor)
            y[i] = torch.tensor(eval)
            i += 1

        x = torch.stack(tensor_list)
        return x, y

        



#eval = EvalReader()
#tensor = EvalReader.fen_to_tensor('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
#print(eval.get_all()[0])
