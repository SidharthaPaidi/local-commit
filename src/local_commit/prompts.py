# prompt for llm

from rich.console import Console

console = Console()


def build_commit_prompt(
    diff: str,
    max_diff_chars: int = 12000,
) -> str:
    if len(diff) > max_diff_chars:
        Console.print(
            f"[yellow]Diff is large, using the first "
            f"{max_diff_chars} characters.[/yellow]"
        )
        diff = diff[:max_diff_chars]

    return f"""
    Generate exactly ONE Conventional Commit message from the git diff.

    Rules:
    - Output exactly ONE line.
    - Never output multiple messages.
    - Never output bullets or explanations.
    - Format: type(scope): description
    - Use only one type: feat, fix, refactor, docs, test, chore, build, ci, perf.
    - Summarize ALL important changes in ONE message.
    - If there are multiple changes, combine them using "and", commas, or "with".
    - Do not describe files individually.
    - Keep it concise: 8-18 words.
    - Output only the commit message.

    Example:
    Multiple changes:
    config loading + CLI commit creation + Ollama options + prompt builder

    Output:
    feat(cli): add config loading, commit creation, Ollama options, and prompt builder

    Git diff:

    {diff}
    """.strip()


# sample for testing
# if __name__ == "__main__":
#     example_diff = """\
#     diff --git a/example.py b/example.py
#     +def hello():
#     +    return "Hello"
#     """

#     print(build_commit_prompt(example_diff))
