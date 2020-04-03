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

    # def test_empty_input(self):
    #     T = Transformer([
    #         ['set_value', [], 'test', {'value': 2}]
    #     ])
    #     out = T()
    #     print(out)

    # def test_constant(self):
    #     T = Transformer([
    #         ['constant', ]
    #     ])


class TestTransformerBuilding(unittest.TestCase):
    """Test if the methods for building Transformers work appropriately"""
    def test_init(self):
        T = Transformer([
            {
                'operation': 'lowercase',
                'inputs': ['A'],
                'outputs': ['B'],
            },
            {
                'operation': 'uppercase',
                'inputs': ['B'],
                'outputs': ['C'],
            }
        ])
        self.assertEqual(len(T.operations), 2)
    
    def test_add(self):
        T = Transformer()
        T.add([
            {
                'operation': 'lowercase',
                'inputs': ['A'],
                'outputs': ['B'],
            },
            {
                'operation': 'uppercase',
                'inputs': ['B'],
                'outputs': ['C'],
            }
        ])
        self.assertEqual(len(T.operations), 2)
    
    def test_add_list(self):
        T = Transformer()
        T.add([
            ['lowercase', 'A', 'B'],
            [['lowercase', 'uppercase'], 'C', 'D'],
        ])
        self.assertEqual(len(T.operations), 3)

class TestShorthands(unittest.TestCase):

    def test_single_input_output(self):
        shorthand = ['operation', 'A', 'B', { 'param1': 'val1' }]
        T = expand_shorthand(shorthand)
        self.assertEqual(len(T), 1)
        target = {
            'operation': 'operation',
            'inputs': ['A'],
            'outputs': ['B'],
            'params': {'param1': 'val1'}
        }
        self.assertDictEqual(T[0], target)

    def test_multiple_inputs_outputs(self):
        mylist = ['operation', ['A', 'B'], ['X', 'Y'], { 'param1': 'val1' }]
        T = expand_shorthand(mylist)
        self.assertEqual(len(T), 1)
        target = {
            'operation': 'operation',
            'inputs': ['A', 'B'],
            'outputs': ['X', 'Y'],
            'params': {'param1': 'val1'}
        }
        self.assertDictEqual(T[0], target)

    def test_single_input_multiple_outputs(self):
        mylist = ['operation', 'A', ['X', 'Y'], { 'param1': 'val1' }]
        T = expand_shorthand(mylist)
        self.assertEqual(len(T), 1)
        target = {
            'operation': 'operation',
            'inputs': ['A'],
            'outputs': ['X', 'Y'],
            'params': {'param1': 'val1'}
        }
        self.assertDictEqual(T[0], target)

    def test_chain_same_size_no_params(self):
        mylist = [['op1', 'op2'], ['A', 'B'], ['X', 'Y']]
        T = expand_shorthand(mylist)
        self.assertEqual(len(T), 2)
        target1 = {
            'operation': 'op1',
            'inputs': ['A', 'B'],
            'outputs': ['X_0_op1', 'Y_0_op1'],
            'params': {}
        }
        self.assertDictEqual(T[0], target1)
        target2 = {
            'operation': 'op2',
            'inputs': ['X_0_op1', 'Y_0_op1'],
            'outputs': ['X', 'Y'],
            'params': {}
        }
        self.assertDictEqual(T[1], target2)

    def test_chain_different_size_no_params(self):
        mylist = [['op1', 'op2', 'op3'], 'A', ['X', 'Y']]
        T = expand_shorthand(mylist)
        self.assertEqual(len(T), 3)
        target0 = {
            'operation': 'op1',
            'inputs': ['A'],
            'outputs': ['X_0_op1', 'Y_0_op1'],
            'params': {}
        }
        self.assertDictEqual(T[0], target0)
        target1 = {
            'operation': 'op2',
            'inputs': ['X_0_op1', 'Y_0_op1'],
            'outputs': ['X_1_op2', 'Y_1_op2'],
            'params': {}
        }
        self.assertDictEqual(T[1], target1)
        target2 = {
            'operation': 'op3',
            'inputs': ['X_1_op2', 'Y_1_op2'],
            'outputs': ['X', 'Y'],
            'params': {}
        }
        self.assertDictEqual(T[2], target2)

    def test_chain_params(self):
        shorthand = [['op1', 'op2'], ['A', 'B'], ['X', 'Y'], [{'param1': 'val1'}, {}]]
        T = expand_shorthand(shorthand)
        self.assertEqual(len(T), 2)
        target1 = {
            'operation': 'op1',
            'inputs': ['A', 'B'],
            'outputs': ['X_0_op1', 'Y_0_op1'],
            'params': {'param1': 'val1'}
        }
        self.assertDictEqual(T[0], target1)
        target2 = {
            'operation': 'op2',
            'inputs': ['X_0_op1', 'Y_0_op1'],
            'outputs': ['X', 'Y'],
            'params': {}
        }
        self.assertDictEqual(T[1], target2)

    def test_constants(self):
        shorthand = ['constant', 'test', 10]
        operations = expand_shorthand(shorthand)
        target = {
            'operation': 'constant',
            'inputs': [],
            'outputs': ['test'],
            'params': {'value': 10}
        }
        self.assertDictEqual(operations[0], target)


if __name__ == '__main__':
    unittest.main()    