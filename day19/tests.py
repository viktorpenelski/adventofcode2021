import unittest

from day19.solution import Point3d, orientations


class Tests(unittest.TestCase):

    def test_distance(self):
        pt1 = Point3d(5, 6, 2)
        pt2 = Point3d(-7, 11, -13)
        self.assertAlmostEqual(19.849433, pt1.distance_to(pt2), places=6)
        self.assertAlmostEqual(19.849433, pt2.distance_to(pt1), places=6)
        self.assertAlmostEqual(0, pt1.distance_to(pt1), delta=0.0001)

    def test_orientations(self):
        pt = Point3d(5, 6, 2)
        pts = []
        for orientation in orientations:
            pts.append(orientation(pt))
        self.assertEqual(24, len(set(pts)))
