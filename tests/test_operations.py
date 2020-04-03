# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# License: 
import unittest
from catafolk.transformer import *

class TestOperations(unittest.TestCase):
    def test_map_values_regex(self):
        values_map = { '(H|h).llo': 'Hello', 'w.+d': 'world'}
        out = map_values('hello', 'woaooorld', 'foo', mapping=values_map)
        self.assertListEqual(out, ['Hello', 'world', None])

    def test_map_values_literal(self):
        values_map = { 
            'hello': 'Hello',
            'woorld': 'world', 
            (1, 2): '3' 
        }
        out = map_values('hello', 'woaooorld', (1, 2), 'foo', 
                         mapping=values_map, regex=False)
        self.assertListEqual(out, ['Hello', None, '3', None])

    def test_format_pattern(self):
        out = format('hello', pattern="{} world")
        self.assertEqual(out, 'hello world')

        out = format('hello', 'world', pattern="{} {}")
        self.assertEqual(out, 'hello world')

    def test_format_no_pattern(self):
        out = format('{} world', 'hello')
        self.assertEqual(out, 'hello world')

        out = format('{} {}', 'hello', 'world')
        self.assertEqual(out, 'hello world')

    def test_extract_groups_all(self):
        out = extract_groups('foo-bar', pattern='(.+)\-(.+)')
        self.assertListEqual(out, ['foo-bar', 'foo', 'bar'])

    def test_extract_groups(self):
        out = extract_groups('foo-bar', pattern='(.+)\-(.+)', groups=[1,2])
        self.assertListEqual(out, ['foo', 'bar'])


