import numpy as np
from PIL import Image
import math
import random
import copy
from settings import VERBOSE, N_COLS, LEVEL_BACK

'''
remove weight
'''

def zero(x, y):
    return x

def one(x, y):
    return y

def five(x, y):
    value = 0
    value += math.cos(2 * math.pi * x / 255.0)
    value += math.sin(2 * math.pi * y / 255.0) 
    value = 255 * abs(value) / 2.0
    return int(value)

def six(x, y):
    value = 0
    value += math.cos(3 * math.pi * x / 255.0)
    value += math.sin(2 * math.pi * y / 255.0)
    value = 255 * abs(value) / 2.0
    return int(value)

def nine(x, y): 
    value = 0
    value += math.cosh(x + y) % 256
    return int(value)

def thirteen(x, y):
    value = 0
    value += 255 * abs(math.tan((x + y) * math.pi / (8.0 * 255)))
    return int(value)

class Function:
    def __init__(self, f, arity):
        self.f = f
        self.arity = arity

    def __call__(self, *args, **kwargs):
        return self.f(*args, **kwargs)



"""
Node in CGP Graph
"""
class Node:
    def __init__(self, max_arity):

        self.i_func = None
        self.i_inputs = [None] * max_arity
        '''
        weight
        '''
        # self.weights = [None] * max_arity
        self.i_output = None
        self.output = None
        self.active = False



"""
(chromosome, genotype, etc) in evolution
"""
class Individual:
    function_set = None
    # weight_range = [-1, 1]
    max_arity = 2
    n_inputs = 2
    n_outputs = 3
    n_cols = N_COLS
    level_back = LEVEL_BACK


    def __init__(self):
        self.nodes = []
        for pos in range(0, self.n_cols):
            self.nodes.append(self._create_random_node(pos))
        for i in range(1, self.n_outputs + 1):
            self.nodes[-i].active = True
        self.fitness = None
        self._active_determined = False

    def _create_random_node(self, pos):
        node = Node(self.max_arity)
        temp_func = random.randint(0, len(self.function_set) - 1)
        node.i_func = random.uniform(temp_func / len(self.function_set), (temp_func + 1)/ len(self.function_set))
        for i in range(self.function_set[math.floor(node.i_func * len(self.function_set))].arity):
            '''
            rethink
            '''
            temp_in = random.randint(max(pos - self.level_back, -self.n_inputs), pos - 1)
            node.i_inputs[i] = random.uniform(temp_in / (pos + self.n_inputs), (temp_in + 1) / (pos + self.n_inputs)) 
            '''
            weight
            '''
            # node.weights[i] = random.uniform(self.weight_range[0], self.weight_range[1])
        node.i_output = pos

        return node


    '''
    determine which nodes are active
    '''
    def _dermine_activate_nodes(self):
        n_active = 0
        for pos in range(len(self.nodes)-1, -1, -1):
            node = self.nodes[pos]
            if node.active:
                n_active += 1
                for i in range(self.function_set[math.floor(node.i_func * len(self.function_set))].arity):
                    i_input = math.floor(node.i_inputs[i] * (pos + self.n_inputs))
                    if i_input >= 0:
                        self.nodes[i_input].active = True
        if VERBOSE:
            print("# active genes:", n_active)


    '''
    compute
    '''
    def eval(self, *args):
        if not self._active_determined:
            self._dermine_activate_nodes()
            self._active_determined = True
        # forward pass: compute
        
        for pos in range(len(self.nodes)):
            node = self.nodes[pos]
            if node.active:
                inputs = []
                for i in range(self.function_set[math.floor(node.i_func * len(self.function_set))].arity):
                    i_function = math.floor(node.i_func * len(self.function_set))
                    i_input = math.floor(node.i_inputs[i] * (pos + self.n_inputs))
                    # w = node.weights[i]
                    if i_input < 0:
                        inputs.append(args[-i_input - 1])
                    else:
                        inputs.append(self.nodes[i_input].output)

                node.output = self.function_set[math.floor(node.i_func * len(self.function_set))](*inputs)
        return [node.output for node in self.nodes[-3:]]


    '''
    mutate
    '''
    def mutate(self, mut_rate = 0.01):
        child = copy.deepcopy(self)
        for pos, node in enumerate(child.nodes):
            if random.random() < mut_rate:
                temp_func = random.choice(range(len(self.function_set)))
                node.i_func = random.uniform(temp_func / len(self.function_set), (temp_func + 1)/ len(self.function_set))
            i_function = math.floor(node.i_func * len(self.function_set))
            arity = self.function_set[i_function].arity
            for i in range(arity):
                if node.i_inputs[i] is None or random.random() < mut_rate:
                    temp_in = random.randint(max(pos - self.level_back, -self.n_inputs), pos - 1)
                    node.i_inputs[i] = random.uniform(temp_in / (pos + self.n_inputs), (temp_in + 1) / (pos + self.n_inputs)) 
                # if node.weights[i] is None or random.uniform(self.weight_range[0], self.weight_range[1])

            node.active = False
        for i in range(1, self.n_outputs + 1):
            child.nodes[-i].active = True
        child.fitness = None
        child._active_determined = False
        return child


 
    '''
    crossover
    '''
    def cross_over(self, parentb, cross_rate = 0.5):
        
        child = Individual()
        for pos, node in enumerate(child.nodes):
            node.i_func = cross_rate * self.nodes[pos].i_func + (1-cross_rate) * parentb.nodes[pos].i_func
            i_function = math.floor(node.i_func * len(self.function_set))
            arity = self.function_set[i_function].arity
            for i in range(arity):
                node.i_inputs[i] = cross_rate * self.nodes[pos].i_inputs[i] + (1-cross_rate) * parentb.nodes[pos].i_inputs[i]
            node.active = False
        for i in range(1, self.n_outputs + 1):
            child.nodes[-i].active = True
        child.fitness = None
        child._active_determined = False
        return child



fs = [Function(zero, 2), Function(one, 2), Function(five, 2), Function(six, 2), Function(nine, 2), Function(thirteen, 2)]
Individual.function_set = fs
Individual.max_arity = max(f.arity for f in fs)


def create_population(n):
    return[Individual() for _ in range(n)]

