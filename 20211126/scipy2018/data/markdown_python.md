# Markdown and Python Example

This is a regular markdown file. In Jupyter Lab you can open and edit the file in the file editor or in the markdown viewer.

# Including Python

Here is a block of Python code in the markdown file:

```python
a = 10
```

And an even larger example:
```python

%matplotlib inline
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
data = {
    'x': np.random.rand(100),
    'y': np.random.rand(100),
    'color': np.random.rand(100),
    'size': 100*np.random.rand(100)
}
df = pd.DataFrame(data)

style.use('seaborn-whitegrid')
plt.scatter ('x', 'y', c='color', s='size', data = df, cmap=plt.cm.Blues)

```
