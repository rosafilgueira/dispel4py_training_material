# dispel4py_training_material
This repository is dedicated to store different training material that we have presented at different events. It contains presentations, as well several dispel4py workflows

# dispel4py
dispel4py is a free and open-source Python library for describing abstract stream-based workflows for distributed data-intensive applications. It enables users to focus on their scientific methods, avoiding distracting details and retaining flexibility over the computing infrastructure they use. It delivers mappings to diverse computing infrastructures, including cloud technologies, HPC architectures and specialised data-intensive machines, to move seamlessly into production with large-scale data loads. The dispel4py system maps workflows dynamically onto multiple enactment systems, such as MPI, STORM and Multiprocessing, without users having to modify their workflows.

# Installation

Visit the [dispel4py GitHub repository](https://github.com/dispel4py/dispel4py), which contains the instructions for installing it. 

# Material

This reporitory contains:

- [dispel4py-tutorial](https://github.com/rosafilgueira/dispel4py_training_material/tree/master/dispel4py-tutorial): Two presentations [Basic](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/dispel4py-tutorial/dispel4py_Basic.pdf) and [Advanced](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/dispel4py-tutorial/dispel4py_Advanced.pdf) for understanding how to work with dispel4py.  This directory also contains two dispel4py workflows:

	- My first dispel4py workflow [python](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/dispel4py-tutorial/dispel4py_example_EvenOdd/My_First_dispel4py_Workflow.py) / [notebook](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/dispel4py-tutorial/dispel4py_example_EvenOdd/My%20First%20dispel4py%20Workflow.ipynb) for checking that dispel4py installation works correctly. It also gives an introduction about how to write dispel4py PEs, how to connect them together, and how to execute a dispel4py workflow. Definitly is the first workflow that you should try.

	- The second dispel4py workflow, 'EvenOddworklow' presented as a [python](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/dispel4py-tutorial/dispel4py_example_EvenOdd/EvenOddworkflow.py) / [notebook](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/dispel4py-tutorial/dispel4py_example_EvenOdd/EvenOddworkflow.ipynb), gives you more insides of dispel4py, since it has more advance features than the previous one. For more complex workflows, you should go to [dispel4py_workflow_collection](https://github.com/rosafilgueira/dispel4py_training_material/tree/master/dispel4py_workflow_collection) directory.  

- [dispel4py_workflow_collection](https://github.com/rosafilgueira/dispel4py_training_material/tree/master/dispel4py_workflow_collection): This directory contains a set of dispel4py 'benchmark' workflows (Mycompression_exercise, My_First_dispel4py_Workflow, Testing_dispel4py, WordCount). Instructions and descriptions of the benchmarks workflow are included in the python scripts and notebooks. This directory also have two simplified
real applications: Sentiment Twitter Analysis (analysis_sentiment) and Internal Galaxies Extintion (int_ext_graph). Instructions for executing the real workflows are also included (ReadmeTwitter.txt and ReadmeAstroWF.txt). More explanation about the real applications can be found at the [eScience2015 Slides](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/eScience2015_dispel4py.pdf).

- Conferences presentations: [EGU-2015 Slides](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/EGU2015_OpenSource_dispel4py.pdf), [eScience2015 Slides](https://github.com/rosafilgueira/dispel4py_training_material/blob/master/eScience2015_dispel4py.pdf) and [AGU2015 Slides] (Slides: https://github.com/rosafilgueira/dispel4py_training_material/blob/master/AGU2015_IN34A_dispel4py.pdf). More information can be foud at: https://www.computer.org/csdl/proceedings/e-science/2015/9325/00/9325a454-abs.html. 


