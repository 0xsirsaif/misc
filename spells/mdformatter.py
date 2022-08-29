"""
A Command-line tool to reformatting a plain-text into Markdown, and then publish to my blog

** API Design **
- mdformatter [arguments] [source] [build-dir]
- arguments
    - --blog [serioussaif/else]
    - --target [content folder name]
    - --name [folder name]
    - --img [image path]
    - --push True [False by default]

** Requirements **
- detect newline -> <br>
- blank line -> blank line
- md special chars -> escape by default
- headings #HL# -> <b> </b>
- provide a valid frontmatter
- images

** Algorithm **
"""
import typer
import pathlib


def formatter(src_file: pathlib.Path):
    all_lines: list = []
    with open(src_file, "rt") as f:
        for line in f:
            line = line.strip("\n")
            if len(line.strip()) == 0:
                line = "\n"
            elif line == "-":
                all_lines[-1] += "\n"
                line = "\\- "
            elif "#B#" in line:
                line = f"<b> {line.strip('#B#')} </b>"
            all_lines.append(line + "<br>" + "\n")

    return all_lines


def cleaning():
    """
    - Remove frontmatter
    - Remove Image, if exists
    """


def closing(out_file: pathlib.Path, all_lines: list, meta: dict):
    """
    - Add opening and closing <div dir="rtl"></div>
    - Add Image
    - Iterate over the output file and append "\n" to each "\\- <br>"
    - remove <br> from each <b></b>
    """

    def _add_frontmatter(title, description, date):
        return f"+++\ntitle = {title}\ndescription = {description}\ndate = {date}\n+++\n"

    new_lines = (
        [_add_frontmatter(**meta), '\n<div dir="rtl">\n\n']
        + ["![alt](image.jpg)\n\n"]
        + all_lines
        + ["\n</div>\n"]
    )

    for i in range(len(new_lines)):
        if new_lines[i] == "\\- <br>\n":
            new_lines[i] += "\n"
        if "<b>" in new_lines[i]:
            new_lines[i] = new_lines[i].replace("<br>", "")

    with open(out_file, "wt") as fw:
        for line in new_lines:
            fw.write(line)


def main(
    src: pathlib.Path,
    out: pathlib.Path,
    title: str = "",
    description: str = "",
    date: str = "",
):
    _meta = {
        "title": title,
        "description": description,
        "date": date,
    }
    all_lines = formatter(src)
    closing(out, all_lines, _meta)


if __name__ == "__main__":
    typer.run(main)
