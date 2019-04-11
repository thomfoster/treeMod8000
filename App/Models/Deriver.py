# For testing instance of
from Cell import Cell

# For printing % output
import sys

def derive(tree, n): # ---------------------------------------------------------
    # Perform n passes over tree
    for i in range(0, n):
        # Print % Complete:
        # sys.stdout.write('\r')
        # sys.stdout.write("Deriving: "+ str(int(100*i/n))+"%")
        new_tree = []
        for element in tree:
            if isinstance(element, Cell):
                new_tree += element.Grow()
            else:
                new_tree += [element]
        tree = new_tree
    return tree
# END DERIVE -------------------------------------------------------------------


def printStructure(tree): # ----------------------------------------------------
    for element in tree:
        if isinstance(element, Cell):
            print(element.id, element.age)
        else:
            print(element)
# END PRINT --------------------------------------------------------------------
