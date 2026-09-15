import tomllib

from pathlib import Path
from typing import Optional


class Config:
    def __init__(self):
        self.model: str = "llama3.2:latest"
        self.ollama_url: str = "http://localhost:11434"
        self.max_diff_chars: int = 12000
        self._load_config_file()
            
    def _load_config_file(self) -> None:
        config_path = Path.home() / ".config" / "local_commit" / "config.toml"  # path of config file to parse it
        
        if not config_path.exists():
            return
        
        try:
            #parse the config file
            with open(config_path, "rb") as f:
                data = tomllib.load(f)
                
            self.model = data.get("model", self.model)
            self.ollama_url = data.get("ollama_url", self.ollama_url)
            self.max_diff_chars = data.get("max_diff_chars",self.max_diff_chars)
            
        except Exception as err:
            print(f"Warning : Could not load config file {config_path}: {err}")
            
            
def load_config() -> Config:
    return Config()

