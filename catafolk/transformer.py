# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Author: Bas Cornelissen
# Copyright © 2020 Bas Cornelissen
# License: 
import re
import json
from graphkit import operation as create_operation
from graphkit import compose
from graphkit.network import DataPlaceholderNode
from .operations import *

def expand_shorthand(shorthand):
    """Expands a shorthand description to a series of full operations,
    described by dictionaries containing the `operation`, a list of `inputs`,
    a list of `outputs`, and finally some optional `params`.
    
    Operation shorthands are of the following general form:

    ```python
    shorthand = [list_of_functions, list_of_inputs, list_of_outputs, list_of_params]
    ```
    
    Importantly, the first element is a *list* of function, which allows you 
    specify a chain of operations. The conversion takes care of generating
    names for the intermediate nodes. For example:
    
    ```
    >>> shorthand = [['split', 'uppercase'], 'my_input', ['part1', 'part2'], [{'sep':'-'}, {}]]
    >>> expand_shorthand(shorthand)
    [
        {
            "operation": "split",
            "inputs": ["my_input"],
            # Automatically named intermediate outputs
            "outputs": ["part1_1_split", "part2_1_split"] 
            "params": {"sep": "-"}
        },
        {
            "operation": "lowercase",
            "inputs": ["part1_1_split", "part2_1_split"],
            "outputs" ["part1", "part2"],
            "params": {}
        }
    ]
    ```

    Note that in this example, we provided function *names* (strings), rather than 
    actual functions; but both are supported.

    The following examples illustrate how the shorthand format can be 
    further simplified.

    ### Single inputs/outputs

    If you pass an element rather than a list, it is converted in a list 
    with one item:

    ```
    >>> shorthand = ['lowercase', 'my_input', 'my_output']
    >>> expand_shorthand(shorthand)
    [{
        'operation': 'lowercase',
        'inputs': ['my_input'],
        'outputs': ['my_output'],
        'params': {}
    }]
    ```

    ### Multiple inputs/outputs

    ```
    >>> shorthand = ['lower', ['input1', 'input2'], ['output1', 'output2']]
    >>> expand_shorthand(shorthand)
    [{
        'operation': 'lower',
        'inputs': ['input1', 'input2']
        'outputs': ['output1', 'output2'],
        'params': {}
    }]
    ```

    ### Chaining operations

    You can specify a chain of operations by passing a list of operations
    as the first element to the shorthand. The conversion automatically
    creates names for the outputs of intermediate operations, but it cannot
    infer the number of outputs. Instead, *it assumes that the number of 
    outputs does not change after the firs operation*. 

    To pass parameters to the operations, add a list containing a parameter 
    dictionary for every operation:

    ```
    >>> shorthand = [['split', 'lower'], 'input1', ['output1', 'output2'], [{'sep': '-'}, {}]
    >>> expand_shorthand(shorthand)
    [
        {
            'operation': 'split',
            'inputs': ['input1'],
            'outputs': ['output1_1_split', 'output2_1_split'],
            'params': {'sep': '-'}
        },
        {
            'operation': 'lower',
            'inputs': ['output1_1_split', 'output2_1_split'],
            'outputs': ['output1', 'output2'],
            'params': {}
        }
    ]
    ```

    Note that intermediate outputs are always named
    `{output_name}_{operation_index}_{operation_name}.

    ### Constants

    You can insert constants in the computation graph using the `constant`
    operation, which has a special shorthand:

    ```
    >>> shorthand = ['constant', 'my_constant', 10]
    >>> expand_shorthand(shorthand)
    [{
        "operation": "constant",
        "inputs": [],
        "outputs": ["my_constant"],
        "params": {"value": 10}
    }]
    ```
    
    Parameters
    ----------
    shorthand : list
        A shorthand description of a transformation
    
    Returns
    -------
    list
        A list of dictionaries with keys `operation`, `inputs`, `outputs` 
        and `params`.
    """
    assert type(shorthand) == list

    # Immediately return when defining a constant
    if len(shorthand) == 3 and shorthand[0] == 'constant':
        return [{
            'operation': 'constant',
            'inputs': [],
            'outputs': [shorthand[1]],
            'params': { 'value': shorthand[2]}
        }]

    # Turn single arguments into argument lists
    for i in range(len(shorthand)):
        if type(shorthand[i]) != list:
            shorthand[i] = [shorthand[i]]

    # Add empty parameters for every transformation
    if len(shorthand) == 3:
        empty_params = [{}] * len(shorthand[0])
        shorthand.append(empty_params)

    # Validate and expand the shorthand 
    assert len(shorthand) == 4
    assert type(shorthand[0]) == list
    assert type(shorthand[1]) == list
    assert type(shorthand[1][0]) == str
    assert type(shorthand[2]) == list
    assert type(shorthand[2][0]) == str
    assert type(shorthand[3]) == list
    assert type(shorthand[3][0]) == dict
    operation_names, chain_inputs, chain_outputs, params = shorthand

    # Build the chain of nodes. If multiple operations are passed
    # this means we have to generate unique ids for intermediate nodes,
    # that are neither inputs nor outputs. The unique ids are based
    # on the output and operation names and of the following form:
    #   {output_name}_{operation_index}_{operation_name}
    # The output size is assumed to stay constant after the first
    # operation the chain
    chain = [chain_inputs]
    for i, op_name in enumerate(operation_names[:-1]):
        intermediates = [f'{out}_{i}_{op_name}' for out in chain_outputs]
        chain.append(intermediates)
    chain.append(chain_outputs)

    # Build dictionaries describing each of the operations in the chain
    operations_dicts = []
    for op, inputs, outputs, param in zip(
        operation_names, chain[:-1], chain[1:], params):
        op_dict = {
            'operation': op,
            'inputs': inputs,
            'outputs': outputs,
            'params': param
        }
        operations_dicts.append(op_dict)

    return operations_dicts

class Transformer():
    _empty_input = '_'

    def __init__(self, operations=[]):
        self.operations = []
        self.graph = None
        self._leafs = None
        self._roots = None
        self._nodes = None
        self.operation_counter = {}
        self.add(operations)

    @property
    def leafs(self):
        """List of names of leaf nodes: outputs of the computation graph"""
        if not self._leafs:
            graph = self.graph.net.graph
            leaf_nodes = [node for node in graph.nodes() 
                if graph.in_degree(node)!=0 and graph.out_degree(node)==0]
            self._leafs = [str(leaf) for leaf in leaf_nodes]
        return self._leafs

    @property
    def roots(self):
        """List of names of root nodes: the inputs to the computation graph"""
        if not self._roots:
            graph = self.graph.net.graph
            root_nodes = [node for node in graph.nodes() 
                if graph.in_degree(node)==0 and graph.out_degree(node)==1]
            self._roots = [str(root) for root in root_nodes]
        return self._roots

    @property
    def nodes(self):
        if not self._nodes:
            self._nodes = []
            graph = self.graph.net.graph
            for node in graph.nodes():
                if isinstance(node, DataPlaceholderNode):
                    self._nodes.append(str(node))
        return self._nodes

    def add_operation(self, operation, inputs, outputs, params={}, name=None):
        if not type(inputs) == list:
            raise ValueError('`inputs` should be a list')
        if not type(outputs) == list:
            raise ValueError('`outputs` should be a list')

        # If operation is a string (function name), look up the actual function
        if type(operation) == str:
            if operation not in globals():
                raise ValueError(f'Unknown operation `{operation}`')
            operation = globals()[operation]
        
        # Cook up a unique name: the function name plus a counter
        if name is None: 
            count = self.operation_counter.get(operation.__name__, 1)
            self.operation_counter[operation.__name__] = count + 1
            name = f'{operation.__name__}_{count}'

        if len(inputs) == 0:
            inputs = [self._empty_input]

        kwargs = dict(name=name, needs=inputs, provides=outputs, params=params)
        op = create_operation(**kwargs)(operation)
        self.operations.append(op)

    def add(self, operations):
        """Add a list of operations to the transformation.

        Operations are defined by (1) a function, the names of (2) the input and 
        (3) output variables, and (4) some optional parameters (see also the 
        method `add_operation`):

        ```python
        my_operation = {
            "function": my_func,  # or "my_func"
            "inputs": ["input1", "input2"],
            "outputs: ["output1", "output2"],
            "params": {"param1": "value1"}
        }
        ```
        
        In many cases this dictionary representation is unnecessary lengthy and one
        can use a shorthand format instead. The shorthand also allows you to chain
        several operations. The following example splits a string `my_input` on 
        a dash, and transform both of the two parts to uppercase:

        ```python
        >>> my_op = [['split', 'uppercase'], 'my_input', ['part1', 'part2'], [{'sep':'-'}, {}]]
        >>> T = Transformation()
        >>> T.add([my_op])
        >>> T({"my_input": "foo-bar"})
        {"part1": "FOO", "part2": "BAR"}
        ```

        For details on the shorthand format, refer to `expand_shorthand`.
        
        Parameters
        ----------
        operations : list
            List of operations; see above for details.
        """
        assert type(operations) == list
        for operation in operations:
            if type(operation) == dict:
                self.add_operation(**operation)
            elif type(operation) == list:
                for operation in expand_shorthand(operation):
                    self.add_operation(**operation)
    
    def load(self, filepath):
        """Loads operations from a JSON file.
        
        The file should contain a list with operation descriptions: either shorthands
        or complete dictionary descriptions.
        
        Parameters
        ----------
        filepath : string
            path to the JSON file
        """
        with open(filepath, 'r') as handle:
            operations = json.load(handle)
            self.add(*operations)

    def compose(self):
        self.graph = compose(name='_computation_graph')(*self.operations)

    def __call__(self, inputs={}, outputs=None, outputs_only=True):
        if self.graph is None: self.compose()
        inputs[self._empty_input] = None

        # TODO: outputs is now ignored. The problem is that it raises
        # an error if an input is now missing, which is very likely...
        #valid_outputs = [n for n in self.nodes if n in outputs]
        transformed = self.graph(inputs)#, outputs=valid_outputs)
        
        if outputs_only:
            return { leaf: transformed.get(leaf, None) for leaf in self.leafs }
        else:
            return transformed

    def plot(self, filename):
        # Fixes a bug in https://github.com/yahoo/graphkit/blob/e70718bbc7b394280c39c1fda381bcebd4c3de8d/graphkit/network.py#L378
        import pydot
        import os
        
        def get_node_name(a):
            if isinstance(a, DataPlaceholderNode):
                return a
            return a.name

        if self.graph is None: self.compose()
        graph = self.graph.net.graph
        g = pydot.Dot(graph_type="digraph", layout="twopi")

        # For styles, see:
        # https://github.com/pydot/pydot/blob/master/pydot.py
        # Colors: https://graphviz.org/doc/info/colors.html
        # https://www.graphviz.org/doc/info/shapes.html
        # https://www.graphviz.org/doc/info/attrs.html
        styles = dict(
            fontsize=9, 
            fontname='helvetica', 
            width=0, 
            height=0, 
            margin='0.1,0.05'
        )

        # draw nodes
        for nx_node in graph.nodes():
            if isinstance(nx_node, DataPlaceholderNode):
                if nx_node in self.roots:
                    index = self.roots.index(nx_node)
                    pos = f'{index},0!'
                    node = pydot.Node(name=nx_node, pos=pos, shape="rect", style="bold", **styles)
                elif nx_node in self.leafs:
                    node = pydot.Node(name=nx_node, shape="rect", style="bold", 
                        color='brown2', fontcolor='brown2', **styles)
                else:
                    node = pydot.Node(name=nx_node, shape="rect", **styles)
            else:
                # Transformation nodes
                node = pydot.Node(name=nx_node.name, shape="rect", 
                    style="rounded", color='grey50', fontcolor='grey50', **styles)
            g.add_node(node)

        # draw edges
        for src, dst in graph.edges():
            src_name = get_node_name(src)
            dst_name = get_node_name(dst)
            edge = pydot.Edge(src=src_name, dst=dst_name, 
                arrowsize=.5,
                minlen=0)
            g.add_edge(edge)

        # Store file
        basename, ext = os.path.splitext(filename)
        if ext.lower() == ".png":
            g.write_png(filename)
        elif ext.lower() == ".dot":
            g.write_dot(filename)
        elif ext.lower() in [".jpg", ".jpeg"]:
            g.write_jpeg(filename)
        elif ext.lower() == ".pdf":
            g.write_pdf(filename)
        elif ext.lower() == ".svg":
            g.write_svg(filename)
 
if __name__ == '__main__':
    with open('datasets/bronson-child-ballads/config.json', 'r') as h:
        config = json.load(h)
    
    T = Transformer(config['transformations'])
    print(T)
    # T.load('../datasets/bron')
#     # T.add(concatenate, inputs=['a', 'b'], outputs=['c'], sep='-')
#     # T.add(split, inputs=['c'], outputs=['part1', 'part2'], sep='-')
#     # T.add(rename, inputs=['part2',], outputs=['Whooo',])
#     T.add()
#     out = T.apply({'a': 'hallo', 'b': 'aap'})
#     print(out)

#     # graph = compose(name="graph")(
#     #     operation(name="concat", needs=["a", "b"], provides="d", params=dict(sep='-'))(concatenate),
#     #     operation(name="split", needs="d", provides=["X", "Y"], params=dict(sep='-'))(split)
    # )

    # Run the graph and request all of the outputs.
    # out = graph({'a': 'hallo', 'b': 'aap'})
    # print(out)
    # concatenate = Concatenate(separator='-')
    # lower = Lowercase()

    