# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# License: 
import unittest
import os
import pandas as pd
from catafolk.index import Index
from catafolk.source import *
from catafolk.transformer import Transformer

CUR_DIR = os.path.dirname(__file__)
TEST_DATASETS_DIR = os.path.join(CUR_DIR, 'datasets')
TEST_OPTIONS = {
    'dir': os.path.join(TEST_DATASETS_DIR, '{dataset_id}')
}
TEST_INDEX_PATH = os.path.join(CUR_DIR, 'test_index.csv')

def remove_test_index():
    if os.path.exists(TEST_INDEX_PATH):
        os.remove(TEST_INDEX_PATH)

def get_test_sources():
    entries = [ {'id': f'item{i}', 'foo': 'bar'} for i in range(5)]
    source1 = Source(entries, name='test')

    path = os.path.join(CUR_DIR, 'test_csv_source.csv')
    source2 = CSVSource(path, name='csv', id_field='item_id')

    return source1, source2

class TestIndex(unittest.TestCase):

    def test_initialize(self):
        remove_test_index()
        index = Index(TEST_INDEX_PATH, fields=['id', 'field1', 'field2'])
        df = index.data
        self.assertEqual(len(df.index), 0)
        self.assertListEqual(list(df.columns), ['field1', 'field2'])

    def test_register_sources(self):
        remove_test_index()
        source1, source2 = get_test_sources()
        index = Index(TEST_INDEX_PATH)
        index.register_sources(source1, source2)

        self.assertEqual(len(index._sources), 2)
        self.assertTrue('test' in index._sources)
        self.assertTrue('csv' in index._sources)

    def test_collect(self):
        remove_test_index()
        source1, source2 = get_test_sources()
        index = Index(TEST_INDEX_PATH)
        index.register_sources(source1, source2)
        
        df = index.collect()
        columns = list(df.columns)
        columns = ['test.id', 'test.foo', 'csv.item_id', 'csv.col1', 'csv.col2']
        self.assertListEqual(list(df.columns), columns)
        self.assertEqual(len(df), 10)

    def test_transform(self):
        remove_test_index()
        transformer = Transformer([
            ['join', ['csv.col1', 'csv.col2'], 'joined', { 'sep': '-'}]
        ])
        source1, source2 = get_test_sources()
        index = Index(TEST_INDEX_PATH, transformer=transformer)
        index.register_sources(source1, source2)
        df = index.collect()
        transformed = index.transform(df)
        self.assertEqual(len(transformed), 10)
        self.assertEqual(len(transformed.columns), 7)
        self.assertEqual(transformed.loc['item0','joined'], 'A-foo')
        self.assertEqual(transformed.loc['item6','joined'], 'G')
        self.assertEqual(transformed.loc['item7','joined'], 'foo')
        self.assertEqual(transformed.loc['item8','joined'], '')

    def test_update(self):
        remove_test_index()
        source1, source2 = get_test_sources()
        index = Index(TEST_INDEX_PATH, fields=['test.foo', 'csv.col1'])
        index.register_sources(source1, source2)
        df = index.collect()
        index.update(df)
        self.assertEqual(len(index.data), 10)
        self.assertListEqual(list(index.data.columns), ['test.foo', 'csv.col1'])
    
    def test_save(self):
        remove_test_index()
        source1, source2 = get_test_sources()
        index = Index(TEST_INDEX_PATH, fields=['test.foo', 'csv.col1'])
        index.register_sources(source1, source2)
        df = index.collect()
        index.update(df)
        index.save()

        df2 = pd.read_csv(TEST_INDEX_PATH, index_col='id')
        self.assertEqual(len(df2), 10)
        self.assertListEqual(list(df2.columns), ['test.foo', 'csv.col1'])

    def test_update_with_existing_data(self):
        remove_test_index()
        source1, source2 = get_test_sources()
        index = Index(TEST_INDEX_PATH, fields=['test.foo', 'csv.col1'])
        index.register_sources(source1, source2)
        
        df = index.collect()
        index.update(df)
        index.save()

        new_index = Index(TEST_INDEX_PATH, fields=['test.foo', 'csv.col1', 'source3.bla'])
        entries = [ {'id': f'item{i}', 'bla': i+2} for i in range(5, 15)]
        source3 = Source(entries, name='source3')
        new_index.register_sources(source1, source2, source3)
        df = new_index.collect()
        new_index.update(df)
        new_index.save()
        self.assertEqual(len(new_index.data), 15)
        self.assertEqual(len(new_index.data.columns), 3)
        self.assertEqual(new_index.data.loc['item10', 'source3.bla'], 12)
        self.assertEqual(new_index.data.loc['item14', 'source3.bla'], 16)
        
    def test_make(self):
        remove_test_index()
        source1, source2 = get_test_sources()
        index = Index(TEST_INDEX_PATH, fields=['test.foo', 'csv.col1'])
        index.register_sources(source1, source2)
        index.make()
        
        df = pd.read_csv(TEST_INDEX_PATH, index_col='id')
        self.assertEqual(len(df), 10)
        self.assertListEqual(list(df.columns), ['test.foo', 'csv.col1'])