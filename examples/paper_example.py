# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %% [markdown]
# Read datasets and senses.

# %%
from utils.utils import read_data

data_path = 'datasets/example.csv'
senses_path = 'senses/example.csv'

data, sense_dict = read_data(data_path, senses_path)

print('data:\n', data)
print('\nsense_dict:\n', sense_dict)  # sense->synonym

# %% [markdown]
# Convert sense table to ssets.

# %%
from utils.utils import convert_ssets

ssets = convert_ssets(sense_dict)
print('ssets:\n', ssets)

# %% [markdown]
# Initialize attribute columns here.

# %%
from utils.utils import get_attribute

col_name1 = 'A'
attrs1 = get_attribute(data, col_name1)

col_name2 = 'B'
attrs2 = get_attribute(data, col_name2)

right_col_name = 'C'

print('attrs1:', attrs1)
print('attrs2:', attrs2)

# %% [markdown]
# Compute an initial assignment for every equivalence class $x$.

# %%
import pandas as pd
from algorithms.init_assign import init_assign

initial_senses1 = {}
initial_senses2 = {}

for l in attrs1:
    x = data[data[col_name1] == l][[col_name1, right_col_name]]
    selected_sense = init_assign(x, ssets, sense_dict)
    initial_senses1[l] = selected_sense
    print('x:\n', x)

for l in attrs2:
    x = data[data[col_name2] == l][[col_name2, right_col_name]]
    selected_sense = init_assign(x, ssets, sense_dict)
    initial_senses2[l] = selected_sense
    print('x:\n', x)


# %%
print('initial_senses1:\n', initial_senses1)
print('initial_senses2:\n', initial_senses2)

# %% [markdown]
# Construct the dependency graph $G$.
# 
# Compute the Earth Mover's Distance between overlapping classes ($u_1$, $u_2$) as edge weights.

# %%
from algorithms.dependency_graph import DependencyGraph

G = DependencyGraph(data, initial_senses1, initial_senses2, attrs1, attrs2, sense_dict, right_col_name)
G.display()

# %% [markdown]
# Visit nodes in decreasing order of their $EMD$ values by summing over all corresponding edges.
# 
# Traverse G with BFS and refine the sense for each equivalence class.

# %%
G.BFS()
G.display()

# %% [markdown]
# Data repair algorithm.

# %%
# repair()


