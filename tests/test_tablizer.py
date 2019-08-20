#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tablizer` package."""

import unittest
from tablizer.tablizer import calculate
import numpy as np
import math

class TestTablizer(unittest.TestCase):
    """Tests for `tablizer` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_tablizer_calculate(self):
        """Test calculate function."""

        success = True
        array = np.array([[1,1,1,1],[np.nan,2,3,6]])
        methods = ['nanmean','nanmax','std','nanpercentile']
        results = calculate(array, methods, percentiles = [5,95])

        if results['nanpercentile_min'] != 1.0:
            success = False

        if results['nanpercentile_max'] != 5.1:
            success = False

        if results['nanmean'] != 2.143:
            success = False

        if not math.isnan(results['std']):
            success = False

        assert(success)
