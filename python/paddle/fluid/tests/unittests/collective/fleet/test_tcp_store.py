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

import unittest
import paddle
import os


class TestTCPStore(unittest.TestCase):

    def test_tcp_store(self):
        dist_port = int(os.getenv("PADDLE_DIST_UT_PORT", 6170))
        print("get dist_port:", dist_port)
        store = paddle.fluid.core.TCPStore("127.0.0.1", dist_port, True, 1, 1)
        store.add("my", 3)
        ret1 = store.get('my')
        store.add("my", 3)
        ret2 = store.get('my')
        self.assertEqual(ret1[0] + 3, ret2[0])


if __name__ == "__main__":
    unittest.main()
