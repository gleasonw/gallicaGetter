from unittest import TestCase
from gallicaGetter.build.dateGrouping import DateGrouping


class TestDateGrouping(TestCase):

    def test_get_all_grouping_for_year(self):
        allGroups = DateGrouping('1900', '1902', 'all')
        self.assertEqual(len(allGroups), 1)

    def test_get_month_grouping_intervals(self):
        monthGroups = DateGrouping('1900', '1901', 'month')
        self.assertEqual(len(monthGroups), 24)
        self.assertTrue(('1900-01-02', '1900-02-01') in monthGroups)
        self.assertTrue(('1900-12-02', '1901-01-01') in monthGroups)
        self.assertTrue(('1901-12-02', '1902-01-01') in monthGroups)

    def test_get_year_grouping_intervals(self):
        yearGroups = DateGrouping('1900', '1902', 'year')
        self.assertEqual(len(yearGroups), 3)
        self.assertTrue(('1900-01-01', '1901-01-01') in yearGroups)
        self.assertTrue(('1901-01-01', '1902-01-01') in yearGroups)

    def test_get_month_grouping_edgy_month(self):
        monthGroups = DateGrouping('1900-12-01', '1901-01-01', 'month')
        self.assertEqual(len(monthGroups), 24)
        self.assertTrue(('1900-12-02', '1901-01-01') in monthGroups)

    def test_get_month_grouping_edgy_month_one_val(self):
        monthGroup = DateGrouping('1900-12', None, 'month')
        self.assertEqual(len(monthGroup), 1)
        self.assertTrue(('1900-12-02', '1901-01-01') in monthGroup)

    def test_get_month_grouping_edgy_month_flopped_val(self):
        monthGroup = DateGrouping(None, '1900-12', 'month')
        self.assertEqual(len(monthGroup), 1)
        self.assertTrue(('1900-12-02', '1901-01-01') in monthGroup)

    def test_one_date_month_grouping(self):
        monthGroup = DateGrouping('1900-12-01', None, 'month')
        self.assertEqual(len(monthGroup), 1)
        self.assertTrue(('1900-12-02', '1901-01-01') in monthGroup)

        floppedMonthGroup = DateGrouping(None, '1900-12-01', 'month')
        self.assertEqual(len(floppedMonthGroup), 1)
        self.assertTrue(('1900-12-02', '1901-01-01') in floppedMonthGroup)

    def test_one_date_year_grouping(self):
        yearGroup = DateGrouping('1900', None, 'year')
        self.assertEqual(len(yearGroup), 1)
        self.assertTrue(('1900-01-01', '1901-01-01') in yearGroup)

        floppedYearGroup = DateGrouping(None, '1900', 'year')
        self.assertEqual(len(floppedYearGroup), 1)
        self.assertTrue(('1900-01-01', '1901-01-01') in floppedYearGroup)

    def test_date_grouping_flopped_orders(self):
        yearGroup = DateGrouping('1905', '1900', 'year')
        self.assertEqual(len(yearGroup), 6)
        self.assertTrue(('1900-01-01', '1901-01-01') in yearGroup)