from typing import Union

from .cells import cell_len, get_character_cell_size as get_char_size
from .console import Console, ConsoleOptions, RenderResult
from .jupyter import JupyterMixin
from .style import Style
from .text import Text


class Rule(JupyterMixin):
    r"""A console renderable to draw a horizontal rule (line).
    
    Args:
        title (Union[str, Text], optional): Text to render in the rule. Defaults to "".
        characters (str, optional): Character(s) used to draw the line. Defaults to "─".
        style (StyleType, optional): Style of Rule. Defaults to "rule.line".
        end (str, optional): Character at end of Rule. defaults to "\\n"
    """

    def __init__(
        self,
        title: Union[str, Text] = "",
        *,
        characters: str = "─",
        style: Union[str, Style] = "rule.line",
        end: str = "\n",
    ) -> None:
        if cell_len(characters) < 1:
            raise ValueError(
                "'characters' argument must have at least a cell width of 1"
            )
        self.title = title
        self.characters = characters
        self.style = style
        self.end = end

    def __repr__(self) -> str:
        return f"Rule({self.title!r}, {self.characters!r})"

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        width = options.max_width

        characters = self.characters or "─"

        if cell_len(characters) == 1:
            chars_len = get_char_size(characters)
        else:
            chars_len = 0
            for i in list(characters):
                chars_len += get_char_size(i)
        if not self.title:
            yield Text(characters * (width // chars_len), self.style)
        else:
            if isinstance(self.title, Text):
                title_text = self.title
            else:
                title_text = console.render_str(self.title, style="rule.text")

            if cell_len(title_text.plain) > width - 4:
                title_text.truncate(width - 4, overflow="ellipsis")

            title_text.plain = title_text.plain.replace("\n", " ")
            title_text = title_text.tabs_to_spaces()
            rule_text = Text(end=self.end)
            side_width = (width - cell_len(title_text.plain)) // 2
            if chars_len == 1:
                side = Text(characters * side_width)
            else:
                side = Text(characters * (side_width // (chars_len - 1)))
            side.truncate(side_width - 1)
            rule_text.append(str(side) + " ", self.style)
            rule_text.append(title_text)
            rule_text.append(" " + str(side), self.style)
            if len(rule_text) < width:
                rule_text.append(characters[0], self.style)
            yield rule_text


if __name__ == "__main__":  # pragma: no cover
    from rich.console import Console
    import sys

    try:
        text = sys.argv[1]
    except IndexError:
        text = "Hello"
    console = Console(width=16)
    console.print(Rule(title="fo", characters="=."))
