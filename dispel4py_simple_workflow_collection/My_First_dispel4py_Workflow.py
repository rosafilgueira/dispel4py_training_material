from dispel4py.base import ProducerPE
from dispel4py.base import IterativePE

class MyFirstPE(IterativePE):

    def __init__(self, divisor):
        IterativePE.__init__(self)
        self.divisor = 5

    def _process(self, data):
        #self.log("data is %s and divisor is %s" % (data, self.divisor))
        if not data % self.divisor == 0:
            return data


class NumberProducer(ProducerPE):
    def __init__(self, start, limit):
        ProducerPE.__init__(self)
        self.start = start
        self.limit = limit
    def _process(self, inputs):
        for i in xrange(self.start, self.limit):
            self.write('output', i)

from dispel4py.workflow_graph import WorkflowGraph

producer = NumberProducer(2, 100)
divide = MyFirstPE(3)

graph = WorkflowGraph()
graph.connect(producer, 'output', divide, 'input')
#dispel4py simple My_First_dispel4py_Workflow.py
