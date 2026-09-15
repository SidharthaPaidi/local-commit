from pathlib import Path
import subprocess

class GitError(RuntimeError):
    """Raised when a Git command fails."""
    
def run_git(*arguments : str) -> str:
    #create a subprocess to run provided commands
    result = subprocess.run( #the result will stored a completedProcess instance
        ["git", *arguments], # treats as one command git + arguments
        cwd = Path.cwd(),
        text=True,
        capture_output=True,
        check=False
    )

    #returnCode property checks if the command worked ? if no returns 0 (exit code)
    if result.returncode != 0:
        raise GitError(f"Git command failed: {' '.join(arguments)}\n{result.stderr}")
    
    return result.stdout

# passing a list of commands (*arguments is tuple) in run_git()
def get_status() -> str:
    return run_git("status","--short") # in subprocess.run() -> git status --short will be executed

def get_staged_diff() -> str:
    return run_git("diff","--cached") # same as line 25

def create_commit(message: str) -> None:
    run_git("commit","-m",message) # same as line 25


# testing temporarily the function in this file
# if __name__ == "__main__":
#     print("Git status:")
#     print(get_status())

#     print("Staged diff:")
#     print(get_staged_diff())