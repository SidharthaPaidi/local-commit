import typer

#A context manager to capture the result of print() or log() in a string
from rich.console import Console 
from rich.panel import Panel

from .git import GitError, get_status, get_staged_diff
from .ollama import OllamaError, generate_commit_message
from .prompts import build_commit_prompt

app = typer.Typer()
console = Console()

@app.command()
def main(
        model : str = typer.Option(
            "llama3.2:latest",
            "--model",
            help="Ollama model to use."
        )
    ) -> None:
    #display staged git changes
    try:
        #check status
        status = get_status()
        
        # if no changes are made
        if not status: 
            console.print("[yellow]No Git changes found.[/yellow]")
            raise typer.Exit()
        
        #get staged diff
        diff = get_staged_diff()
        
        # if no changed made yet
        if not diff.strip():
            console.print(
                "[yellow]No staged changes found.Run 'git add <file>' first.[/yellow]"
            )
            raise typer.Exit(code=1)
           
        #build prompt for commit message
        console.print("[lightblue]Generating commit message...[/lightblue]")
        prompt = build_commit_prompt(diff)
        
        #calling ollama
        message  = generate_commit_message(prompt,model=model)
        
        #result
        console.print(Panel(message,title="Suggested commit",style="green"))
        
    except GitError as err:
        typer.echo(f"Git error:{err}",err = True)
        raise typer.Exit(code=1) 
          
if __name__ == "__main__":
    app()   