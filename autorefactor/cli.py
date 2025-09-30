import sys
import click
from .core import analyze_file

try:
    from rich.console import Console
    from rich.markdown import Markdown
    console = Console()
    USE_RICH = True
except ImportError:
    USE_RICH = False

@click.command()
@click.argument("path", type=click.Path(exists=True))
def main(path):
    suggestions = analyze_file(path)
    if not suggestions:
        msg = "No suggestions. Nice clean code!"
        if USE_RICH:
            console.print(f"[green]{msg}[/green]")
        else:
            print(msg)
        sys.exit(0)

    for s in suggestions:
        header = f"{s.get('file','-')}:{s.get('line','-')}"
        if USE_RICH:
            console.rule(header)
            console.print(Markdown(f"**Suggestion:** {s.get('message','-')}"))
            if s.get("code"):
                console.print("\n[bold]Snippet:[/bold]")
                console.print(s.get("code"))
        else:
            print("----")
            print(header)
            print("Suggestion:", s.get("message","-"))
            if s.get("code"):
                print("Snippet:")
                print(s.get("code"))

if __name__ == "__main__":
    main()
