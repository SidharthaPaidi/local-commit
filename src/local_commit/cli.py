import typer

# A context manager to capture the result of print() or log() in a string
from rich.console import Console
from rich.panel import Panel
from .git import GitError, create_commit, get_status, get_staged_diff
from .ollama import OllamaError, generate_commit_message
from .prompts import build_commit_prompt

from .config import load_config

app = typer.Typer()
console = Console()


@app.command()
def main(
    model: str | None = typer.Option(None, "--model", help="Ollama model to use."),
    commit: bool = typer.Option(
        False,
        "--commit",
        help="Create the Git commit after confirmation.",
    ),
) -> None:
    config = load_config()

    if model is None:
        model = config.model

    # display staged git changes
    try:
        # check status
        status = get_status()

        # if no changes are made
        if not status:
            console.print("[yellow]No Git changes found.[/yellow]")
            raise typer.Exit()

        # get staged diff
        diff = get_staged_diff()

        # if no changed made yet
        if not diff.strip():
            console.print(
                "[yellow]No staged changes found.Run 'git add <file>' first.[/yellow]"
            )
            raise typer.Exit(code=1)

        # build prompt for commit message
        console.print("[cyan]Generating commit message...[/cyan]")
        prompt = build_commit_prompt(diff, max_diff_chars=config.max_diff_chars)

        # calling ollama
        message = generate_commit_message(
            prompt, model=model, base_url=config.ollama_url
        )

        # result
        console.print(Panel(message, title="Suggested commit", style="green"))

        # create commit
        if commit:
            if typer.confirm("Create this commit?"):
                create_commit(message)
                console.print("[green]Commit created.[/green]")
            else:
                console.print("[yellow]Commit cancelled.[/yellow]")
        else:
            console.print("[dim]Run with --commit to create the commit.[/dim]")
    
    except GitError as err:
        typer.echo(f"Git error:{err}", err=True)
        raise typer.Exit(code=1)

    except OllamaError as err:
        typer.echo(f"Ollama error: {err}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
