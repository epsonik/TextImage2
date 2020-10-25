import unittest

import numpy as np

from Obj import ObjData
from SceneDescription import get_relpos, create_bound_boxes, get_field_size, create_prop, get_properties, get_mfarg, tmf


class TestInit(unittest.TestCase):
    num = 3
    left = [-0.9250, -0.2500, -0.4250]
    right = [-0.7750, 0.2000, -0.0250]
    horiz_len = [0.0750, 0.2250, 0.2000]
    up = [-0.9750, -0.7750, 0]
    down = [-0.9000, -0.6500, 0.2750]
    vert_len = [0.0375, 0.0625, 0.1375]
    size = [0.0028, 0.0141, 0.0275]

    def test_relpos(self):
        obj_data = get_relpos(create_bound_boxes(), get_field_size())
        self.assertEqual(self.num, obj_data.num)

    def test_relpos_left(self):
        obj_data = get_relpos(create_bound_boxes(), get_field_size())
        np.testing.assert_allclose(self.left, np.around(obj_data.left, decimals=3))

    def test_relpos_right(self):
        obj_data = get_relpos(create_bound_boxes(), get_field_size())
        np.testing.assert_allclose(self.right, np.around(obj_data.right, decimals=4))

    def test_relpos_horiz_len(self):
        obj_data = get_relpos(create_bound_boxes(), get_field_size())
        np.testing.assert_allclose(self.horiz_len, np.around(obj_data.horiz_len, decimals=4))

    def test_relpos_up(self):
        obj_data = get_relpos(create_bound_boxes(), get_field_size())
        np.testing.assert_allclose(self.up, np.around(obj_data.up, decimals=4))

    def test_relpos_down(self):
        obj_data = get_relpos(create_bound_boxes(), get_field_size())
        np.testing.assert_allclose(self.down, np.around(obj_data.down, decimals=4))

    def test_relpos_vert_len(self):
        obj_data = get_relpos(create_bound_boxes(), get_field_size())
        np.testing.assert_allclose(self.vert_len, np.around(obj_data.vert_len, decimals=4))

    def test_relpos_size(self):
        obj_data = get_relpos(create_bound_boxes(), get_field_size())
        np.testing.assert_allclose(self.size, np.around(obj_data.size, decimals=4))


class TestInit2(unittest.TestCase):
    obj_prop_expected = [[0.500000000000000, 0, 0],
                         [0.997252747252747, 0.416666666666667, 0.708333333333334],
                         [0, 1, 0],
                         [0, 0.333333333333333, 0],
                         [0, 0, 0],
                         [0.833333333333333, 0, 0], [0.991758241758242, 1, 0],
                         [1, 1, 1],
                         [0, 0, 0.458333333333333],
                         [0, 0, 0]]

    def test_properties(self):
        obj_data = get_relpos(create_bound_boxes(), get_field_size())
        obj_prop = get_properties(obj_data, create_prop())
        for index, item in enumerate(obj_prop):
            np.testing.assert_allclose(self.obj_prop_expected[index], np.around(obj_prop[index], decimals=4))


class TestInitMfarg(unittest.TestCase):
    num = 3
    left = [-0.9250, -0.2500, -0.4250]
    right = [-0.7750, 0.2000, -0.0250]
    horiz_len = [0.0750, 0.2250, 0.2000]
    up = [-0.9750, -0.7750, 0]
    down = [-0.9000, -0.6500, 0.2750]
    vert_len = [0.0375, 0.0625, 0.1375]
    size = [0.0028, 0.0141, 0.0275]
    ob_data = ObjData(num, left, right, horiz_len, up, down, vert_len, size)

    def test_mfarg_0(self):
        prop = create_prop()
        expected_out = [-0.925000000000000, -0.250000000000000, -0.425000000000000]
        out = get_mfarg(self.ob_data, prop[0], 0, 0)
        np.testing.assert_allclose(expected_out, out)

    def test_mfarg_1(self):
        prop = create_prop()
        expected_out = [-0.925000000000000, -0.250000000000000, -0.425000000000000]
        out = get_mfarg(self.ob_data, prop[1], 0, 0)
        np.testing.assert_allclose(expected_out, out)

    def test_mfarg_2(self):
        prop = create_prop()
        expected_out = [-0.850000000000000, -0.0250000000000000, -0.225000000000000]
        out = get_mfarg(self.ob_data, prop[2], 0, 0)
        np.testing.assert_allclose(expected_out, out)

    def test_mfarg_3(self):
        prop = create_prop()
        expected_out = [-0.775000000000000, 0.200000000000000, -0.0250000000000000]
        out = get_mfarg(self.ob_data, prop[3], 0, 0)
        np.testing.assert_allclose(expected_out, out)

    def test_mfarg_4(self):
        prop = create_prop()
        expected_out = [-0.775000000000000, 0.200000000000000, -0.0250000000000000]
        out = get_mfarg(self.ob_data, prop[4], 0, 0)
        np.testing.assert_allclose(expected_out, out)

    def test_mfarg_5(self):
        prop = create_prop()
        expected_out = [-0.975000000000000, -0.775000000000000, 0]
        out = get_mfarg(self.ob_data, prop[5], 0, 0)
        np.testing.assert_allclose(expected_out, out)

    def test_mfarg_6(self):
        prop = create_prop()
        expected_out = [-0.975000000000000, -0.775000000000000, 0]
        out = get_mfarg(self.ob_data, prop[6], 0, 0)
        np.testing.assert_allclose(expected_out, out)

    def test_mfarg_7(self):
        prop = create_prop()
        expected_out = [0]
        out = get_mfarg(self.ob_data, prop[7], 0, 0)
        np.testing.assert_allclose(expected_out, out)

    def test_mfarg_8(self):
        prop = create_prop()
        expected_out = [-0.900000000000000, -0.650000000000000, 0.275000000000000]
        out = get_mfarg(self.ob_data, prop[8], 0, 0)
        np.testing.assert_allclose(expected_out, out)

    def test_mfarg_9(self):
        prop = create_prop()
        expected_out = [-0.900000000000000, -0.650000000000000, 0.275000000000000]
        out = get_mfarg(self.ob_data, prop[9], 0, 0)
        np.testing.assert_allclose(expected_out, out)


    # def test_tmf(self):
    #     expected_out = self.get_expected_out()
    #     prop = create_prop()
    #     f = []
    #     for i in range(len(prop)):
    #         out = tmf(get_mfarg(self.ob_data, prop[i], 0, 0), prop[i].ftype, prop[i].fthr)
    #         f.append(out)
    #         # np.testing.assert_allclose(expected_out[i], np.around(out, decimals=0))
    #     print(*f, sep="\n")
