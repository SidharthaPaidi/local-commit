# prompt for llm
def build_commit_prompt(diff: str) -> str:
    return f"""
    You generate Git commit messages.

    Analyze the following staged Git diff and create a concise Conventional Commit message.

    Rules:
    - Use one of these types: feat, fix, refactor, docs, test, build, chore, perf, ci.
    - Use an imperative subject.
    - Keep the subject under 72 characters.
    - Do not mention files unless useful.
    - Return only the commit message.
    - Do not use Markdown formatting.

    Staged Git diff:
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
