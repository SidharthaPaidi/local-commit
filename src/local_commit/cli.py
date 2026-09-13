import typer

from .git import GitError, get_status, get_staged_diff

app = typer.Typer()

@app.command()
def main(name : str = "Developer") -> None:
    #display staged git changes
    try:
        status = get_status()
        
        # if no changes are made
        if not status: 
            typer.echo("no change found in git")
            raise typer.Exit()
        
        diff = get_staged_diff()
        
        # if no changed made yet
        if not diff.strip():
            typer.echo("No staged changes found, please run 'git add' first")
            raise typer.Exit(code=1)
           
        typer.echo("Here you Go, staged changes:")
        typer.echo(diff)
        
    except GitError as err:
        typer.echo(f"Git error:{err}",err = True)
        raise typer.Exit(code=1) 
          
if __name__ == "__main__":
    app()   