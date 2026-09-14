import httpx

class OllamaError(RuntimeError):
    """Raised when an Ollama command fails."""
    
def generate_commit_message(
    prompt:str,
    model:str="llama3.2:latest",
    base_url:str="http://localhost:11434"
) -> str: 
    try:
        response = httpx.post( #response will be json ; contains commit message 
            f"{base_url}/api/generate",
            json={
                "model":model,
                "prompt":prompt,
                "stream":False,
            },
            timeout=120
        )
    except httpx.RequestError as err:
        raise OllamaError(
            "Could not connect to Ollama"
        ) from err
        
    if response.status_code != 200:
        raise OllamaError(
            f"Ollama returned HTTP {response.status_code}"
            f"{response.text}"
        )
        
    data = response.json()
    
    if "response" not in data:
        raise OllamaError(
            f"Ollama returned unexpected response: {data}"
        )
        
    return data["response"].strip()

# testing this

# if __name__ == "__main__":
#     message = generate_commit_message(
#         "Add a function that reads the staged Git diff"
#     )
#     print(message)