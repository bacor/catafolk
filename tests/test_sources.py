# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# License: 
import unittest
import os
import pandas as pd
from catafolk.source import *
from catafolk.transformer import Transformer

CUR_DIR = os.path.dirname(__file__)
TEST_DATASETS_DIR = os.path.join(CUR_DIR, 'datasets')

class TestSource(unittest.TestCase):
    def test_iterable_source(self):
        entries = [ {'id': i, 'foo': 'bar'} for i in range(10)]
        source = IterableSource(entries, name='test')
        df = source.collect()
        self.assertEqual(len(df), 10)
        self.assertEqual(len(df.columns), 1)
        self.assertTrue((df['foo'] == 'bar').all())
    
    def test_csv_source(self):
        path = os.path.join(CUR_DIR, 'test_csv_source.csv')
        source = CSVSource(path, name='csv', id_field='item_id')
        df = source.collect()
        self.assertEqual(df.index.name, 'id')
        self.assertEqual(len(df), 10)
        self.assertEqual(df.columns[0], 'item_id')
        self.assertEqual(df.columns[1], 'col1')
        self.assertEqual(df.columns[2], 'col2')

    def test_id_transformer(self):
        entries = [ {'item_id': i, 'foo': 'bar'} for i in range(10)]
        transformations = [
            ['format', 'item_id', 'id', {'pattern': 'item-{:0>3}'}]
        ]
        source = IterableSource(entries, name='test', id_field='item_id',
            id_transformations=transformations)
        df = source.collect()
        self.assertEqual(df.index[0], 'item-000')
        self.assertEqual(df.index[1], 'item-001')
        self.assertEqual(df.index[2], 'item-002')
        self.assertEqual(len(df), 10)
        self.assertEqual(len(df.columns), 2)
        self.assertEqual(df.loc['item-000', 'foo'], 'bar')

    def test_file_source(self):
        data_dir = os.path.join(TEST_DATASETS_DIR, 'bronson-child-ballads', 'data')
        source = FileSource(data_dir, '*.krn', name='file')
        print(source)