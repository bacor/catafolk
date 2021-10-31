# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# License: 
import unittest
import os
import pandas as pd
from catafolk.dataset import Dataset

CUR_DIR = os.path.dirname(__file__)
TEST_DATASETS_DIR = os.path.join(CUR_DIR, 'datasets')
TEST_OPTIONS = {
    'dir': os.path.join(TEST_DATASETS_DIR, '{dataset_id}')
}

class TestDataset(unittest.TestCase):

    def test_initialize(self):
        dataset = Dataset('bronson-child-ballads', options=TEST_OPTIONS)
        self.assertTrue(True)

    def test_index(self):
        dataset = Dataset('bronson-child-ballads', options=TEST_OPTIONS)
        if os.path.exists(dataset.index_path):
            os.remove(dataset.index_path)
        dataset.make()
        self.assertTrue(os.path.exists(dataset.index_path))