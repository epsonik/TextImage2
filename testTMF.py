import unittest

import numpy as np

from Obj import ObjData
from SceneDescription import create_prop, tmf, get_mfarg


class TestInitTMF(unittest.TestCase):
    num = 3
    left = [-0.9250, -0.2500, -0.4250]
    right = [-0.7750, 0.2000, -0.0250]
    horiz_len = [0.0750, 0.2250, 0.2000]
    up = [-0.9750, -0.7750, 0]
    down = [-0.9000, -0.6500, 0.2750]
    vert_len = [0.0375, 0.0625, 0.1375]
    size = [0.0028, 0.0141, 0.0275]
    ob_data = ObjData(num, left, right, horiz_len, up, down, vert_len, size)

    def get_expected_out(self):
        return [[0.5000, 0, 0],
                [0.9973, 0.4167, 0.7083],
                [0, 1, 0],
                [0, 0.3333, 0],
                [0, 0, 0],
                [0.8333, 0, 0],
                [0.9918, 1, 0],
                [1, 1, 1],
                [0, 0, 0.4583],
                [0, 0, 0]]

    # def test_tmf_1(self):
    #     expected_out = self.get_expected_out()
    #     prop = create_prop()
    #     i = 7
    #     out = tmf(get_mfarg(self.ob_data, prop[i], 0, 0), prop[i].ftype, prop[i].fthr)
    #     print(out)
    #     np.testing.assert_allclose(expected_out[i], out)

    def test_tmf(self):
        expected_out = self.get_expected_out()
        prop = create_prop()
        f = []
        for i in range(len(prop)):
            out = tmf(get_mfarg(self.ob_data, prop[i], 0, 0), prop[i].ftype, prop[i].fthr)
            f.append(out)
            # np.testing.assert_allclose(expected_out[i], np.around(out, decimals=0))
        print(*f, sep="\n")
