# ODPHAC

An outlier detection strategy for spatial free path-finding based on hierarchical ant colonies

## Background

Outlier Detection (OD) is of great significance and widely used in various industries. It can not only find outlier objects to ensure industry safety, but also mine new knowledge. Considering the biological pattern of ant colony foraging behavior and inspired by swarm intelligence, we proposed an outlier detection strategy of spatial free path-finding for hierarchical ant colonies: OD Based on Path-finding of Hierarchical Ant Colonies (ODPHAC). 

## Install

Installing **ODPHAC** package with pip command

```sh
pip install ODPHAC
```

## Usage

7 rows to get a quick start.

```python
import ODPHAC
import scipy.io as scio
input_data = scio.loadmat('datasets/glass.mat')
X_train = input_data['X']
y_true = input_data['y']
y_predict_scores = ODPHAC.antModel(X_train, np.shape(X_train)[0], 3, 1, 3,0.5,0.2) 
print(y_predict_scores)
```

## Parameter Details

- Input
  - data: Input Data.
  - k: The k-nearest neighbor of master ants.
  - kap: The k'-nearest neighbor of slave ants.
  - eta: Controlling Ant Life.
  - round: Number of rounds implemented.
  - slave_ant_proportion: Number of slave ants divided by number of instances in data sets.
  - master_ant_proportion: Number of slave ants divided by number of instances in data sets.
- Output
  - pheList: A list of pheromones that store the final pheromones for each point, which is also called *y_predict_scores*  in some places.  The higher the pheromone content, the more isolated the point


## License

The MIT License (MIT) Copyright  2022

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
