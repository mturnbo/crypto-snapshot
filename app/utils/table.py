from rich.console import Console
from rich.table import Table

def show_data_table(data):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    column_titles = data[0].keys()
    for column_title in column_titles:
        table.add_column(column_title)
    for row in data:
        string_values = [str(value) for value in row.values()]
        table.add_row(*string_values)
    console.print(table)
