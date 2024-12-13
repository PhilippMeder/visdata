import warnings

from visdata import get_numpy


class BaseTableOutput:

    separator = f"{'':4}"
    linebreak = "\n"
    newline = "\n"

    def __init__(
        self,
        data,
        n_columns,
        formatter,
        caption=None,
        column_labels=None,
        row_labels=None,
        linestyle=None,
    ):
        self._data = data
        self._caption = caption
        self._row_labels = row_labels
        self._column_labels = column_labels
        self._n_columns = n_columns
        if row_labels is not None:
            self._n_columns += 1
            self._column_labels = ("", *column_labels)

        self._linestyle = linestyle
        self._formatter = formatter
        if formatter is not None:
            try:
                self._column_width = int(self._formatter.split(".")[0])
            except ValueError:
                self._column_width = 0
        else:
            self._column_width = 0

        self.set_baserule()

    def set_baserule(self):
        sep = len(self.separator)
        total_length = self._n_columns * (self._column_width + sep) - sep
        self._baserule = f"{'':\u2500>{total_length}}{self.linebreak}"

    @property
    def baserule(self):
        return self._baserule

    def rule(self, ruletype):
        match ruletype, self._linestyle:
            case ("top" | "mid" | "bottom"), "scientific":
                return self.baserule
            case _:
                return ""

    def formatted_heading(self, heading):
        if self._column_width:
            return f"{heading:{self._column_width}}"
        else:
            return heading

    def formatted_value(self, value):
        if self._formatter is not None:
            return f"{value:{self._formatter}}"
        else:
            return f"{value}"

    def begin(self):
        if self._caption is not None:
            try:
                caption = (
                    f"{f'Table: {self._caption}':^{len(self.baserule)}}{self.linebreak}"
                )
            except Exception as err:
                # Older python versions do not support all string formats
                caption = f"Table: {self._caption}{self.linebreak}"
        else:
            caption = ""

        return caption

    def header(self, tab=None):
        if tab is None:
            tab = ""
        header = tab + self.rule("top") + tab
        if self._column_labels is not None:
            sep = self.separator
            header += f"{sep}".join(map(self.formatted_heading, self._column_labels))
            header += f"{self.newline}{tab}{self.rule('mid')}"
        return header

    def content_rows(self):
        sep = self.separator
        headings = self._row_labels
        if headings is not None:
            rows = [
                f"{self.formatted_heading(heading)}{sep}"
                + f"{sep}".join(map(self.formatted_value, row_data))
                for heading, row_data in zip(headings, self._data, strict=True)
            ]
        else:
            rows = [
                f"{sep}".join(map(self.formatted_value, row_data))
                for row_data in self._data
            ]

        return rows

    def content(self, tab=None):
        if tab is None:
            return f"{self.newline}".join(self.content_rows()) + self.newline
        else:
            return (
                f"{self.newline}".join(f"{tab}{row}" for row in self.content_rows())
                + self.newline
            )

    def footer(self, tab=None):
        if tab is None:
            tab = ""
        footer = tab + self.rule("bottom")
        return footer

    def end(self):
        return ""

    def __call__(self):
        return (
            self.begin() + self.header() + self.content() + self.footer() + self.end()
        )


class CSVTableOutput(BaseTableOutput):

    separator = ","


class LatexTableOutput(BaseTableOutput):

    separator = " & "
    newline = " \\\\\n"
    tab = f"{'':4}"

    def __init__(
        self,
        *args,
        use_booktabs=True,
        position=None,
        alignment=None,
        label=None,
        math_mode=True,
        **kwargs,
    ):
        self.use_booktabs = use_booktabs
        self.math_mode = math_mode
        self._position = "htbp" if position is None else position
        self._label = "XXX" if label is None else label

        super().__init__(*args, **kwargs)

        if alignment is None:
            self._alignment = "".join(["c" for _ in range(self._n_columns)])
        elif len(alignment) == 1:
            self._alignment = "".join([alignment for _ in range(self._n_columns)])
        else:
            self._alignment = alignment

        if self._column_labels is None:
            self._column_labels = ["" for _ in range(self._n_columns)]

    def rule(self, ruletype):
        match ruletype, self._linestyle, self.use_booktabs:
            case ("top" | "mid" | "bottom"), "scientific", False:
                return r"\hline" + self.linebreak
            case "top", "scientific", True:
                return r"\toprule" + self.linebreak
            case "mid", "scientific", True:
                return r"\midrule" + self.linebreak
            case "bottom", "scientific", True:
                return r"\bottomrule" + self.linebreak
            case _:
                return ""

    def formatted_value(self, value):
        formatted_value = super().formatted_value(value)
        if self.math_mode:
            return f"${formatted_value}$"
        else:
            return formatted_value

    def begin(self):
        caption = "XXX" if self._caption is None else self._caption
        return (
            rf"\begin{{table}}[{self._position}]{self.linebreak}"
            rf"{self.tab}\centering{self.linebreak}"
            rf"{self.tab}\caption{{{caption}}}{self.linebreak}"
            rf"{self.tab}\begin{{tabular}}[{self._alignment}]{self.linebreak}"
        )

    def end(self):
        return (
            rf"{self.tab}\end{{tabular}}{self.linebreak}"
            rf"{self.tab}\label{{tab:{self._label}}}{self.linebreak}"
            rf"\end{{table}}{self.linebreak}"
        )

    def __call__(self):
        tab = f"{self.tab}{self.tab}"
        return (
            self.begin()
            + self.header(tab=tab)
            + self.content(tab=tab)
            + self.footer(tab=tab)
            + self.end()
        )


class Table:

    def __init__(self, data, description=None, row_labels=None, column_labels=None):
        self._data = data
        self._description = description
        self._row_labels = row_labels
        self._column_labels = column_labels

        try:
            self._n_rows, self._n_columns = self.data.shape
            self._is_numpy = True
        except (AttributeError, TypeError):
            self._n_rows = len(self.data)
            self._n_columns = len(self.data[0])
            self._is_numpy = False

    @property
    def data(self):
        return self._data

    @property
    def description(self):
        return self._description

    @property
    def n_rows(self):
        return self._n_rows

    @property
    def n_columns(self):
        return self._n_columns

    @property
    def shape(self):
        return (self.n_rows, self.n_columns)

    @property
    def is_numpy(self):
        return self._is_numpy

    def row(self, index):
        return self.data[index]

    def column(self, index):
        column = [row[index] for row in self.data]
        if self.is_numpy:
            return get_numpy().array(column)
        else:
            return column

    def output(self, output_type, formatter=None, linestyle=None, **kwargs):
        match output_type:
            case "base" | "cmd" | "terminal" | "console":
                output_cls = BaseTableOutput
            case "csv" | "CSV":
                output_cls = CSVTableOutput
                if linestyle is not None:
                    warnings.warn(
                        f"Recommended 'linestyle' for '{output_type}' output is 'None', not '{linestyle}'.",
                        UserWarning,
                    )
                if (
                    formatter is not None
                    and (formatter_split := formatter.split("."))[0]
                ):
                    warnings.warn(
                        f"Recommended 'formatter' for '{output_type}' output is '.{'.'.join(formatter_split[1:])}', not '{formatter}'.",
                        UserWarning,
                    )
            case "latex":
                output_cls = LatexTableOutput

        output = output_cls(
            self.data,
            self.n_columns,
            formatter,
            caption=self.description,
            linestyle=linestyle,
            row_labels=self._row_labels,
            column_labels=self._column_labels,
            **kwargs,
        )

        return output()

    def latex(self, formatter=None, **kwargs):
        return self.output(
            "latex", formatter=formatter, linestyle="scientific", **kwargs
        )

    def csv(self, formatter=None, delimiter=None):
        if delimiter is None:
            delimiter = ","
        if formatter is not None and (formatter_split := formatter.split("."))[0]:
            formatter = "." + ".".join(formatter_split[1:])
        return self.output("csv", formatter=formatter, linestyle=None)

    def __str__(self):
        return self.output("base", "10.2e", linestyle="scientific")
