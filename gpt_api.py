import requests


class GptApi:

    def get_api_key():
        file = open("api_key.txt", "r")
        api_key = file.readline().rstrip('\n')
        file.close()
        return api_key

    def call_gpt_api(prompt, model="gpt-4-turbo", max_tokens=100):

        api_key = GptApi.get_api_key()

        url = "https://api.openai.com/v1/chat/completions".format(model=model)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-4", 
            "messages": [{"role": "user", "content": f"{prompt}"}], 
            "temperature": 0.9
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()
    
    def move(fen_str, move_history_str, possible_moves_str):
        # Example usage
        prompt = "We are playing chess, this is board represented in FEN notation:\n"
        prompt += fen_str
        prompt += "This are the possible moves on this position:\n"
        prompt += possible_moves_str
        prompt += "Please make your next move. Send me only the move in long algebraic notation (example a2-d4).\n"
        print(f'Prompt:\n{prompt}')
        response = GptApi.call_gpt_api(prompt)
        text = response['choices'][0]['message']['content'] 
        print('==================================================================')
        print('==================================================================')
        print(f'Chat gpt:\n{text}')
        print('==================================================================')
        print('==================================================================')
        return text
