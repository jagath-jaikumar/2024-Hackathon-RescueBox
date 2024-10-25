import typer
import requests
import sys
import base64
import yaml
import ollama


app = typer.Typer()

APPS_REPOSITORY = "https://api.github.com/repos/UMass-Rescue/2024-Hackathon-RescueBox/contents/tool-suite"
ignore_files = [".gitkeep"]

try:
    apps = requests.get(APPS_REPOSITORY).json()
except Exception as e:
    print(f"Could not fetch available apps, {e}")
    sys.exit(1)

app_names = [_["name"] for _ in apps if _["name"] not in ignore_files]

docs = []
for rb_app in app_names:
    app_url = APPS_REPOSITORY + "/" + rb_app + "/app.yaml"
    content = base64.b64decode(requests.get(app_url).json()["content"]).decode()
    docs.append(content)


@app.command()
def list_apps():
    print("Available apps: \n")
    print(*app_names, sep="\n")


@app.command()
def app_details(name: str):
    app_url = APPS_REPOSITORY + "/" + name + "/app.yaml"
    content = base64.b64decode(requests.get(app_url).json()["content"])
    print(content.decode())


@app.command()
def ask(question: str):

    stream = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an AI assistant designed to support the product RescueBox. RescueBox is a tool for federal law enforcement agents to assist in cases. Rescuebox is a collection of plugins, each with its own documentation. Always answer according to the documentation. The documentation is provided here: 
                
                {docs}

                RULES:
                - Never answer in the first person!
                - Answer in less than 100 words always.
                - Always answer based on the documentation. Do not make up any documentation!
                - Don't explain outside the bounds of the question.
                - Do not make up any documentation!
                - Do not describe python flags and what python is.
                - Do not answer any questions that are not related to rescuebox.
                - Always answer as if talking to an industry professional.
                - If you do not know a specific answer to a question, recommend contacting Brian Levine.
                - If a user asks for a sample command, just provide the command with no other explanation.
                """,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        stream=True,
    )

    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)


if __name__ == "__main__":
    app()
