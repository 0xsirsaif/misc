import typer
from pathlib import Path
import ctypes

app = typer.Typer()


@app.command()
def nweek():
    nweek_c: Path = Path().absolute() / "nweek.so"
    c_lib = ctypes.CDLL(str(nweek_c))
    answer = c_lib.m


if __name__ == "__main__":
    app()
