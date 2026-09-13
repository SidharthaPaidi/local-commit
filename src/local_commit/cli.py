import typer

app = typer.Typer()

@app.command()
def main(name : str = "Developer") -> None:
    """Test the ai-commit command"""
    typer.echo(f"Hello, {name}!")
    
if __name__ == "__main__":
    app()   