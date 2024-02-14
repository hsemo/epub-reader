from rich import print
from rich.layout import Layout

l1 = Layout(name="Main")
l1.split_column(Layout(name="Upper"),Layout(name="Lower"))
l1['Lower'].split_row(Layout(name="Left"),Layout(name="Right"))
print(l1)
