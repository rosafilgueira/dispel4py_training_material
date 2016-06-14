# coding: utf-8

# ## The data streaming classic: WordCount!!

#  We can not leave this tutorial without a streaming classic example. WordCount example reads a text and counts how often words occur. 

# In[32]:

from dispel4py.core import GenericPE
import os
class SplitLines(GenericPE):

    def __init__(self):
        GenericPE.__init__(self)
        self._add_input("input")
        self._add_output("output")
        
    def _process(self, inputs):
	self.log("!!!SplitLines self.id %s, rankid %s, process.rank %s" % (self.id, os.getpid(), self.rank))	
        for line in inputs["input"].splitlines():
            self.write("output", line)

# In[33]:

from dispel4py.base import IterativePE

class SplitWords(IterativePE):

    def __init__(self):
        IterativePE.__init__(self)
        
    def _process(self, data):
	self.log("!!!SplitWords self.id %s, rankid %s, process.rank %s" % (self.id, os.getpid(), self.rank))	
        for word in data.split(" "):
            self.write("output", (word,1))


# In[34]:

from collections import defaultdict

class CountWords(GenericPE):
    def __init__(self):
        GenericPE.__init__(self)
        self._add_input("input", grouping=[0])
        self._add_output("output")
        self.count=defaultdict(int)
        
    def _process(self, inputs):
	self.log("!!!!CountWords self.id %s, rankid %s, process.rank %s" % (self.id, os.getpid(),self.rank))	
        word, count = inputs['input']
        self.count[word] += count
    
    def _postprocess(self):
        self.write('output', self.count)


# In[35]:

from dispel4py.workflow_graph import WorkflowGraph

split = SplitLines()
#split.name = 'split'
words = SplitWords()
count = CountWords()



graph = WorkflowGraph()
graph.connect(split, 'output', words, 'input')
graph.connect(words, 'output', count, 'input')


# In[36]:

from dispel4py.new.simple_process import process as simple_process
#simple_process(graph, {split: [ {'input' : "Hello Hello algo mas World World"}] })

# Write those lines if your command line if you want to run it from there


