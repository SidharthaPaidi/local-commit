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
    You are a Git commit message generator.

    Your task is to analyze the COMPLETE git diff and generate EXACTLY ONE commit message.

    IMPORTANT RULES:
    1. Return ONLY ONE commit message.
    2. NEVER generate multiple commit messages.
    3. NEVER output a list, bullets, multiple lines, or alternatives.
    4. The output MUST be a SINGLE LINE.
    5. Use Conventional Commits format:
    type(scope): description
    6. Choose ONE type only: feat, fix, refactor, docs, test, chore, build, ci, perf.
    7. Choose ONE scope that best represents the main area changed.
    8. If the diff contains multiple related changes, COMBINE them into ONE concise description.
    9. Do NOT describe every file separately.
    10. Mention the most important changes together in one sentence.
    11. Prefer a compact description using "and", commas, or "with".
    12. Do not include unnecessary details, implementation-level details, or filenames.
    13. Keep the commit message between 8 and 18 words.
    14. Do not add Markdown, quotes, explanations, prefixes, or suffixes.

    Examples:

    Diff:
    - Added config file loading
    - Added CLI commit creation
    - Added Ollama options
    - Added commit prompt builder

    Output:
    feat(cli): add config loading, commit creation, Ollama options, and prompt builder

    Diff:
    - Fixed authentication token handling
    - Fixed API error handling
    - Added retry logic

    Output:
    fix(api): improve authentication, error handling, and request retries

    Diff:
    - Renamed functions
    - Extracted helper methods
    - Simplified duplicated logic

    Output:
    refactor(core): simplify logic and extract reusable helpers

    Now analyze this git diff and return EXACTLY ONE SINGLE-LINE commit message:
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
