from .Tabulate import tabulate

class Table:
    def __init__(self, header, columns, values):
        self.header = header
        self.columns = columns
        self.values = values
        
    def tab(self):
        
        table = tabulate([*self.values], self.columns, tablefmt="grid")
        return f'''Log created on {self.header['date']}

Information    {self.header['information']}
Warnings       {self.header['warnings']}
Error          {self.header['errors']}
Total          {self.header['totals']}

{table}
'''