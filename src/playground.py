from collections import defaultdict
import pandas as pd

a = {'xhbb': 3, 'ninied':5}
row = []

row.append(a)
row.append({'xhbb': 3, 'ninied':5})

df = pd.DataFrame(row)    
df.to_excel('Output_files/test.xlsx')
print(df)


