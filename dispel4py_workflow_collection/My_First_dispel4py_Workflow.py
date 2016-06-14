
# coding: utf-8

# # How to create my first dispel4py workflow

# This tutorial is an introduction to dispel4py. We will see how to write dispel4py PEs, how to connect them together to form a workflow and how this workflow is executed in different environments.

# ##How to write a PE
# 
# In this section we are going to implement our first PE.
# 
# First you need to decide what kind of processing the PE will do and what the data units are that it processes. In our example we are implementing a PE that decides if a number is divisible by another number. The PE is configured with this divisor and for each input data item it tests whether the number can be divided by this divisor. It sends the input data item to its output stream if it is not divisible.
# 
# ##Create a PE class
# 
# To start with we create a PE that does only very few things:
# 
# 

# In[1]:

from dispel4py.base import IterativePE

class MyFirstPE(IterativePE):

    def __init__(self, divisor):
        IterativePE.__init__(self)
        self.divisor = divisor


# In this case we extend the base class ``dispel4py.base.IterativePE`` which defines one input and one output, which is exactly what we need. We pass the divisor as an initialisation parameter to the object which stores it.
# 
# ##Implement the processing method
# 
# Now the actual work begins: We have to implement the processing method. This is done by overriding the method of the superclass:

# In[2]:

def _process(self, data):
    None


# We fill in the processing commands, in our case this means that we test if the input data item is divisible by our divisor, and return it if it is not divisible:

# In[3]:

def _process(self, data):
    if not data % self.divisor:
        return data


# The data returned by ``_process`` is written to the output stream of the PE.
# 
# That’s it! Our first PE is complete:

# In[4]:

from dispel4py.base import IterativePE

class MyFirstPE(IterativePE):

    def __init__(self, divisor):
        IterativePE.__init__(self)
        self.divisor = divisor

    def _process(self, data):
        if not data % self.divisor == 0:
            return data


# ##Create a simple workflow
# 
# In this section we are going to create a workflow, using the PE that we implemented in the previous section. There’s a useful PE in the library of dispel4py PEs that just produces a sequence of numbers.
# 
# We can connect this number producer to our PE which is initialised with the divisor 3 in this example:

# In[5]:

from dispel4py.workflow_graph import WorkflowGraph
from dispel4py.examples.graph_testing.testing_PEs import TestProducer

producer = TestProducer()
divide = MyFirstPE(3)

graph = WorkflowGraph()
graph.connect(producer, 'output', divide, 'input')


# This workflow produces integers and tests whether they are divisible by 3. Any numbers that are not divisible by 3 will be written to the unconnected output stream of our first PE.

# ##Execute the workflow
# 
# To run this workflow you can use the sequential simple processor:

# In[6]:

from dispel4py.new.simple_process import process as simple_process
simple_process(graph, {producer: 20})


# The input of this workflow is the number of iterations that the producer PE executes, in our case 20, resulting in the stream of integers from 1 to 20.
# 
# The output of this workflow are the integers in the range from 1 to 20 which are not divisible by 3.
# 
# In the output above, you can see that PEs are assigned an integer ID to uniquely identify them within the graph, as you can use more than one PE of the same kind in a graph. In this graph the producer PE is assigned the ID ``TestProducer0`` which is a combination of its class name and a number, and ``MyFirstPE1`` is the ID of our own PE.

# ##Write a data producer PE
# ###Producing the input
# 
# Next we will create a ProducerPE that creates the input for our first PE. The test producer that we were using above only produces one number per iteration. In our case we would like to create a PE that produces all the numbers from 2 up to a certain limit.
# 
# The implementation looks like this:

# In[7]:

from dispel4py.base import ProducerPE

class NumberProducer(ProducerPE):
    def __init__(self, start, limit):
        ProducerPE.__init__(self)
        self.start = start
        self.limit = limit
    def _process(self):
        for i in xrange(self.start, self.limit):
            self.write('output', i)
            # OR: self.write("ProducerPE.OUTPUT_NAME", i)


# This introduces several new concepts. The ProducerPE is a base class which has no inputs and one output ``ProducerPE.OUTPUT_NAME`` or ``"output"``. We initialise an instance of the NumberProducer PE with the lower and upper bounds for the integers that we want to produce.
# 
# In the implementation of the `_process()` method we iterate over the range of numbers from the lower bound up to (and excluding) the upper bound. Since the processing method generates more than one data item we have to write them one at a time to the output data stream using the ``write()`` method.
# 
# ### Using the producer in the workflow
# 
# Now we hook our own producer into the workflow, replacing the TestProducer from the dispel4py library:

# In[8]:

from dispel4py.workflow_graph import WorkflowGraph

producer = NumberProducer(2, 100)
divide = MyFirstPE(3)

graph = WorkflowGraph()
graph.connect(producer, 'output', divide, 'input')


# Everything else stays the same. We create an instance of the NumberProducer that outputs the range of numbers from 2 to 99 (excluding the upper bound of 100).
# 
# Now execute the new workflow using the simple mapping:

# In[9]:
# Attention: You should to comment the following line, in case you want to run the script in command line by using the dispel4py command, which is explained after. 

simple_process(graph, {producer: 1})


# The output is the list of numbers in the range from 2 to 99 that are not divisible by 3.
# 
# Note that now the producer only execute once as the iterations are handled within the processing method of the PE.

# ## Running the workflow in the command line
# 
# 
#     $ dispel4py simple My_First_dispel4py_Workflow.py
# 
# 
# 

# ##Parallel processing¶
# 
# For this very simple case we can easily parallelise the execution of the workflow. To do this we use the dispel4py multi mapping that executes a workflow in multiple processes using the Python multiprocessing [1] library:
# 
#     $ dispel4py multi My_First_dispel4py_Workflow.py -n 4
#     Processing 1 iteration.
#     Processes: {'MyFirstPE3': [1, 2, 3], 'NumberProducer2': [0]}
#     MyFirstPE3 (rank 1): Processed 33 iterations.
#     NumberProducer2 (rank 0): Processed 1 iteration.
#     MyFirstPE3 (rank 3): Processed 32 iterations.
#     MyFirstPE3 (rank 2): Processed 33 iterations.
# 
# This example executes the workflow using 4 processes. This line:
# 
#     Processes: {'MyFirstPE3': [1, 2, 3], 'NumberProducer2': [0]}
# 
# shows which PE is assigned to which processes. In this case, MyFirstPE is assigned to processes 1, 2 and 3, so there three parallel instances. These instances each process about a third of the data, as you can see from the output of the instances when processing is complete:
# 
#     MyFirstPE3 (rank 1): Processed 33 iterations.
#     MyFirstPE3 (rank 2): Processed 33 iterations.
#     MyFirstPE3 (rank 3): Processed 32 iterations.
# 
# Note that when executing in a parallel environment the output from each PE is not collected as in the simple mapping. You are responsible for collecting this output and printing or storing it.

# ##References
# [1]	https://docs.python.org/2/library/multiprocessing.html

# In[ ]:



