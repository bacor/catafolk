# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# License: 
import unittest
from catafolk.transformer import *

class TestTransformers(unittest.TestCase):

    def test_rename(self):
        T = Transformer()
        T.add_operation(rename, inputs=['a1', 'b1'], outputs=['a2', 'b2'])
        out = T({'a1': 2, 'b1': 4})
        self.assertDictEqual(out, {'a2': 2, 'b2': 4})

        T = Transformer()
        T.add_operation(rename, inputs=['a1'], outputs=['a2'])
        out = T({'a1': 2})
        self.assertDictEqual(out, {'a2': 2})

    def test_join(self):
        T = Transformer()
        T.add_operation(join, inputs=['a', 'b', 'c'], outputs=['combined'], params=dict(sep='-'))
        out = T(dict(a='A', b='B', c='C'))
        self.assertDictEqual(out, {'combined': 'A-B-C'})
    
    def test_join_ints(self):
        T = Transformer()
        T.add_operation(join, inputs=['a', 'b', 'c'], outputs=['combined'])
        out = T(dict(a=1, b=2, c=3))
        self.assertDictEqual(out, {'combined': '123'})
    
    def test_lowercase(self):
        T = Transformer()
        T.add_operation(lowercase, inputs=['input'], outputs=['output'])
        out = T({'input': 'HELLO'})
        self.assertDictEqual(out, {'output': 'hello'})

    def test_regex_extract_groups_all(self):
        T = Transformer()
        T.add_operation(regex_extract_groups, 
            inputs=['input'], 
            outputs=['group0','group1', 'group2'],
            params=dict(pattern='(.+)\-(.+)'))
        out = T({'input': 'foo-bar'})
        self.assertDictEqual(out, {'group0': 'foo-bar', 'group1': 'foo', 'group2': 'bar'})

    def test_regex_extract_groups(self):
        T = Transformer()
        T.add_operation(regex_extract_groups, 
            inputs=['input'], 
            outputs=['group1', 'group2'],
            params=dict(pattern='(.+)\-(.+)', extract_groups=[1,2]))
        out = T({'input': 'foo-bar'})
        self.assertDictEqual(out, {'group1': 'foo', 'group2': 'bar'})

    def test_regex_extract_groups_fails(self):
        T = Transformer()
        T.add_operation(regex_extract_groups, 
            inputs=['input'], 
            outputs=['group1', 'group2'],
            params=dict(pattern='(.+)\-(.+)', extract_groups=[1,2]))
        out = T({'input': 'foobar'})
        self.assertDictEqual(out, {'group1': None, 'group2': None})

    def test_default(self):
        T = Transformer()
        T.add_operation(default, inputs=['in1', 'in2'], outputs=['out1', 'out2'],
            params=dict(values=['default1', 'default2']))
        out = T({'in1': 'orig', 'in2': None})
        self.assertDictEqual(out, {'out1': 'orig', 'out2': 'default2'})

    def test_format(self):
        op = ['format', ['input1', 'input2'], 'output', {'pattern': '{}-{}'}]
        T = Transformer([op])
        out = T({'input1': 'foo', 'input2': 'bar'})
        self.assertDictEqual(out, {'output': 'foo-bar'})

    def test_map_values(self):
        values_map = { '(a|b)c': 'Hello', '[^ab]+c': 'world'}
        op = ['map_values', 'input', 'output', {'mapping': values_map} ]
        T = Transformer([op])
        out = T({'input': 'ac'})
        self.assertDictEqual(out, {'output': 'Hello'})
        out = T({'input': 'AA123c'})
        self.assertDictEqual(out, {'output': 'world'})

class DirectTests(unittest.TestCase):
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


