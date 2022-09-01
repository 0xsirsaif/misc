"""

"""
import typer
from pathlib import Path


def main(directory_path: Path) -> int:
    for sub_file in [f for f in directory_path.iterdir() if f.suffix in [".srt", ".txt"]]:
        _target_name: str = str(sub_file).split("/")[-1][27:]
        target_name: str = _target_name[:len(_target_name)-18].replace(" ", "_") + sub_file.suffix
        sub_file.rename(Path(directory_path, target_name))
    return 0


if __name__ == "__main__":
    typer.run(main)
    