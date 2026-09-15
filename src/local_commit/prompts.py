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
        diff = diff[: max_diff_chars]

    return f"""
    You generate concise Conventional Commit messages based on Git diffs. 
    Return ONLY the raw commit message text. No Markdown, no code blocks, no explanations.

    Examples:
    Diff: + console.log('Starting server...');
    Output: chore: add server startup logging

    Diff: - const maxTimeout = 1000; \n + const maxTimeout = 5000;
    Output: fix(timeout): increase max connection timeout to 5000ms

    Analyze the following diff and apply the same format:

    Diff:
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
