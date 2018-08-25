# __init__.py
# Sophia Fondell
# sfondell@bu.edu
# CS 108: Final Project - bingeList
# URL: TBD

# From Python official documentation:
# The __init__.py files are required to make Python treat the directories as 
# containing packages; this is done to prevent directories with a common name, 
# such as string, from unintentionally hiding valid modules that occur later on 
# the module search path

# The list of module names that should be imported when from package import * is encountered
__all__ = ["backend", "render"]