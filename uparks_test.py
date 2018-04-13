from uparks import *
import unittest


class TestHoursSearch(unittest.TestCase):
    def test_hours_search(self):
        hours_count=get_park_info()
        self.assertEqual(len(hours_count), 122)
        april= get_park_info()[0]
        self.assertEqual(april.parkcity, " Hershey")
        self.assertEqual(april.parkstate, "PA")
        self.assertEqual(april.parkaddress, "100 W. Hersheypark Drive" )
        self.assertEqual(april.parkzip, "17033")
        self.assertEqual(april.day, "Thursday")
        self.assertEqual(april.date, "March 1st")
        self.assertEqual(april.opentime, "Closed")
        self.assertEqual(april.closedtime, "Closed")

    def test_str_info(self):
        test1=get_park_info()[0]
        self.assertEqual(test1.__str__(), "Hershey Park : 100 W. Hersheypark Drive, Hershey, PA 17033, On Thursday, March 1st: the park is closed")

    def test_rides_search(self):
        ride1= get_ride_info()[0]
        self.assertEqual(ride1.ride_name, "Balloon Flite")
        self.assertNotEqual(ride1.ridedescription, None )
        self.assertEqual(ride1.heights, 'Under 36"' )
        self.assertEqual(ride1.parkregion, "Founder's Way")
        self.assertEqual(ride1.star, False)

if __name__ == '__main__':
    unittest.main()
