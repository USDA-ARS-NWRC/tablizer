#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tablizer` package."""

import unittest
from tablizer.tablizer import summarize, store, get_existing_records
import numpy as np
from datetime import datetime
import os

date = datetime(2019,1,1,23,0,0)
value = 'thermal'
database = 'sqlite'
run_name = 'test'
bid = 2
rid = 1
location = os.path.abspath('tests/tablizer_test.db')
array = np.array([[1,1,1,1],[np.nan,2,3,6]])
methods = ['nanmean', 'std', 'nanpercentile']
outcome_methods = ['nanmean', 'std', 'nanpercentile_25', 'nanpercentile_75']

class TestTablizer(unittest.TestCase):
    """Tests for `tablizer` package."""

    @classmethod
    def setUpClass(self):
        """Set up test order."""

        self.test_a_summarize()
        self.test_b_store()
        self.test_c_get_existing_records()
        self.test_d_remove_database()

    @classmethod
    def test_a_summarize(self):
        """Test summarize function values. """

        success = True
        results = summarize(array, date, methods, [25,75], 3)
        self.results = results

        if results['nanmean'].values[0] != 2.143:
            success = False

        if results['nanpercentile_25'].values[0] != 1:
            success = False

        if results['nanpercentile_75'].values[0] != 2.5:
            success = False

        if not np.isnan(results['std'].values[0]):
            success = False

        assert(success)

    @classmethod
    def test_b_store(self):
        """Test store function. """
        store(self.results, value, database, location, run_name, bid, rid, date)
        assert(True)

    @classmethod
    def test_c_get_existing_records(self):
        """Test pulling existing records."""

        success = True
        records = get_existing_records(location, database)

        if records['variable'].values[0] != value:
            success = False

        for function in records['function'].values:
            if function not in outcome_methods:
                success = False

        if records[records['function'] == 'nanmean']['value'].values != 2.143:
            success = False

        if records[records['function'] == 'nanpercentile_25']['value'].values != 1.0:
            success = False

        if records[records['function'] == 'nanpercentile_75']['value'].values != 2.5:
            success = False

        if not np.isnan(records[records['function'] == 'std']['value'].values[0]):
            success = False

        assert(success)

    @classmethod
    def test_d_remove_database(self):
        """Remove database after tests."""

        if os.path.isfile(location):
            os.remove(location)

        assert(True)
