import json
import torch

class EvalReader():

    def __init__(self):
        self.file = open("./data/lichess_db_eval.json", "r")

    def __del__(self):
        self.file.close()

    def get_eval(self):
        line = self.file.readline()
        line_json = json.loads(line)

        fen_str = line_json['fen']
        eval = line_json['evals'][0]['pvs'][0]['cp']
        return (fen_str, eval)

    def get_eval_batch(self, batch_size):
        line = self.file.readline()
        line_json = json.loads(line)

        result = []
        n = batch_size
        while n > 0:
            fen_str = line_json['fen']
            eval = line_json['evals'][0]['pvs'][0]['cp']
            result.append(fen_str, eval)
        return result
    
    def get_eval_batch(self, train_size, test_size):
        line = self.file.readline()
        line_json = json.loads(line)

        train_x = []
        train_y = []
        n = train_size
        while n > 0:
            fen_str = line_json['fen']
            eval = line_json['evals'][0]['pvs'][0]['cp']
            train_x.append(fen_str)
            train_y.append(eval)
            n -= 1

        test_x = []
        test_y = []
        n = test_size
        while n > 0:
            fen_str = line_json['fen']
            eval = line_json['evals'][0]['pvs'][0]['cp']
            test_x.append(fen_str)
            test_y.append(eval)
            n -= 1

        return train_x, train_y, test_x, test_y

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
        return tensor.reshape([768]).squeeze()
    
    def get_n(self, n : int):
        x = torch.zeros(10, 768)
        y = x = torch.zeros(n)

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

            tensor_list.append(EvalReader.fen_to_tensor(fen_str))
            y[i] = torch.tensor(eval)
            i += 1

        x = torch.stack(tensor_list)
        return x, y
        

        



#eval = EvalReader()
#tensor = EvalReader.fen_to_tensor('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
#print(eval.get_all()[0])
