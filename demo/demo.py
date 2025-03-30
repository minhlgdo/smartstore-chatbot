# A simple demo to show the results of the chatbot

API_URL = "http://127.0.0.1:8000/chat"

def demo():
    import requests

    # Prompt the user for a session ID
    while True:
        session_id = input("세션 ID를 입력하세요 (숫자만 입력): ").strip()
        if session_id.isdigit():
            break
        print("유효한 숫자를 입력하세요.")

    print("챗봇과 대화 시작! 종료하려면 'exit' 입력")
    while True:
        user_input = input("\n유저: ")
        if user_input.lower().strip() == "exit":
            break

        # Check if the user input is empty
        if not user_input.strip():
            print("유효한 질문을 입력하세요.")
            continue

        # Send the user input to the chatbot API
        response = requests.post(
            API_URL, json={"session_id": session_id, "question": user_input}, stream=True
        )

        # Check if the response is successful
        if response.status_code == 200:
            print("챗봇: ", end="", flush=True)
            # Print the chatbot's response
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    print(decoded_line, flush=True)
        else:
            print("챗봇과의 대화 중 오류가 발생했습니다.")

if __name__ == "__main__":
    demo()

