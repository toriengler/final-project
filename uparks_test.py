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
        rides=get_ride_info()
        self.assertEqual(len(rides), 73)
        self.assertFalse(ride1.star, True)

class TestDBSearch(unittest.TestCase):
    def test_db(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        sql = '''
            SELECT *
            FROM Hours
            WHERE Dates="April 1st"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn('April 1st', result_list[0])
        self.assertIn('April 1st', result_list[1])
        self.assertEqual(len(result_list), 2)

        sql = '''
            SELECT COUNT(*)
            FROM Rides
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 73)

        conn.close()
class TestDataProcess(unittest.TestCase):
    def test_add_search(self):
        results = process_address('Address')
        self.assertIn('Hershey Park is located at:',results )
        self.assertEqual(type(results), str)
    def test_hours_results(self):
        results = process_query('Hours date=April 1st')
        self.assertEqual(results[0][0], 'Sunday')
        self.assertEqual(results[0][-1], 'ZooAmerica')
    def test_gauge(self):
        data=rating_gauge('Balloon Flite')
        self.assertEqual(data, True)

if __name__ == '__main__':
    unittest.main()
