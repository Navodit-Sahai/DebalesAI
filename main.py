import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.append(str(Path(__file__).parent))

from src.agent import run_agent
from src.rag import build_index


def handle_command(cmd, history):
    if cmd in ["/quit", "quit", "exit"]:
        print("Goodbye!")
        exit()

    if cmd == "/clear":
        print("[System] History cleared\n")
        return []

    if cmd == "/rebuild":
        print("[System] Rebuilding knowledge base...")
        build_index(force=True)
        print("[System] Done\n")
        return history

    return None



def main():
    print("Debales AI Assistant (type /quit to exit)\n")
    
    history = []

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            cmd_result = handle_command(user_input.lower(), history)
            if cmd_result is not None:
                history = cmd_result
                continue

            answer = run_agent(user_input, history)
            print("Assistant:", answer, "\n")

            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": answer})

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()