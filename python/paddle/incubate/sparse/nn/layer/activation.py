#   Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .. import functional as F
from paddle.nn import Layer

__all__ = []


class ReLU(Layer):
    """
    Sparse ReLU Activation.

    .. math::

        ReLU(x) = max(x, 0)

    Parameters:
        name (str, optional): Name for the operation (optional, default is None).
            For more information, please refer to :ref:`api_guide_Name`.

    Shape:
        - input: Sparse Tensor with any shape.
        - output: Sparse Tensor with the same shape as input.

    Examples:
        .. code-block:: python

            import paddle
            from paddle.fluid.framework import _test_eager_guard
            with _test_eager_guard():
                x = [[0, -1, 0, 2], [0, 0, -3, 0], [4, 5, 0, 0]]
                dense_x = paddle.to_tensor(x, dtype='float32')
                sparse_dim = 2
                sparse_x = dense_x.to_sparse_coo(sparse_dim)
                relu = paddle.incubate.sparse.nn.ReLU()
                out = relu(sparse_x)
                #out.values: [0., 2., 0., 4., 5.]
    """

    def __init__(self, name=None):
        super(ReLU, self).__init__()
        self._name = name

    def forward(self, x):
        return F.relu(x, self._name)

    def extra_repr(self):
        name_str = 'name={}'.format(self._name) if self._name else ''
        return name_str


class Softmax(Layer):
    """
    sparse softmax activation, x must be SparseCsrTensor or SparseCooTensor.

    Note:
        Only support axis=-1 for SparseCsrTensor, which is faster when read data 
        by row (axis=-1).

    From the point of view of dense matrix, for each row :math:`i` and each column :math:`j` 
    in the matrix, we have:

    .. math::

        softmax_ij = \frac{\exp(x_ij - max_j(x_ij))}{\sum_j(exp(x_ij - max_j(x_ij))}

    Parameters:
        axis (int, optional): The axis along which to perform softmax calculations. Only support -1 for SparseCsrTensor.
        name (str, optional): Name for the operation (optional, default is None).
            For more information, please refer to :ref:`api_guide_Name`.

    Shape:
        - input: SparseCooTensor / SparseCsrTensor with any shape.
        - output: Sparse Tensor with the same shape as input.

    Examples:
        .. code-block:: python

            import paddle
            import numpy as np
            from paddle.fluid.framework import _test_eager_guard

            paddle.seed(100)

            with _test_eager_guard():
                mask = np.random.rand(3, 4) < 0.5
                np_x = np.random.rand(3, 4) * mask
                # [[0.         0.         0.96823406 0.19722934]
                #  [0.94373937 0.         0.02060066 0.71456372]
                #  [0.         0.         0.         0.98275049]]

                csr = paddle.to_tensor(np_x).to_sparse_csr()
                # Tensor(shape=[3, 4], dtype=paddle.float64, place=Place(gpu:0), stop_gradient=True, 
                #        crows=[0, 2, 5, 6], 
                #        cols=[2, 3, 0, 2, 3, 3], 
                #        values=[0.96823406, 0.19722934, 0.94373937, 0.02060066, 0.71456372,
                #                0.98275049])

                m = paddle.incubate.sparse.nn.Softmax()
                out = m(csr)
                # Tensor(shape=[3, 4], dtype=paddle.float64, place=Place(gpu:0), stop_gradient=True, 
                #        crows=[0, 2, 5, 6], 
                #        cols=[2, 3, 0, 2, 3, 3], 
                #        values=[0.68373820, 0.31626180, 0.45610887, 0.18119845, 0.36269269,
                #                1.        ])
    """

    def __init__(self, axis=-1, name=None):
        super(Softmax, self).__init__()
        self._axis = axis
        self._name = name

    def forward(self, x):
        return F.softmax(x, self._axis, self._name)

    def extra_repr(self):
        name_str = 'name={}'.format(self._name) if self._name else ''
        return name_str