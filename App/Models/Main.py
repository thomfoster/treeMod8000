import sys, Parser, Deriver, Interpreter, SelfOrg
import Analyser2 as Analyser
from Cell import Cell

def generate_model(filename, overrideParams={}, return_analysis=False, parse=True, spec={}): # ---------
    # PARSE
    Specification = spec
    if parse == True:
        Specification   = Parser.parse('Specifications/'+filename+'.txt', overrideParams)

    vertices = []

    if Specification['self_org'] == False:

        # DERIVE
        n               = Specification['depth']
        axiom           = Specification['axiom']
        tree            = [axiom]
        tree            = Deriver.derive(tree,n)

        # INTERPRET
        vertices        = Interpreter.interpret(tree, return_analysis)

    else:

        # DERIVE AND INTERPRET TOGETHER
        n               = Specification['depth']
        axiom           = Specification['axiom']
        tree            = [axiom]
        num_voxels      = Specification['num_voxels']
        shadow_height   = Specification['shadow_height']
        shadow_width    = Specification['shadow_width']
        decrement_close = Specification['dec_close']
        decrement_far   = Specification['dec_far']

        for i in range(0,n):
            tree = Deriver.derive(tree,1)
            vertices, scale = Interpreter.interpret(tree, return_analysis, return_scale = True)
            voxels          = SelfOrg.calc_light(vertices,
                                                 num_voxels,
                                                 shadow_height,
                                                 shadow_width,
                                                 decrement_close,
                                                 decrement_far)
            SelfOrg.update_cells(tree, voxels, scale)
            print("Interpreted for the "+str(i+1)+"th time.")

        for e in tree:
            if isinstance(e, Cell):
                print(e.can_i_grow)

    # Return points of if being used in rendering, write file
    if return_analysis == True:
        return vertices
    else: #commented for use in metric visualisation
        print("writing to file...")
        with open("data.dat", mode="w") as f:
            f.write(str(len(vertices))+"\n")
            for vertex in vertices:
                for feature in vertex:
                    f.write(str(feature)+"\t")
                f.write("\n")
# END GENERATE_MODEL -----------------------------------------------------------


def generate_self_org_model(filename, overrideParams={}, return_analysis=False):

    # PARSE
    Specification   = Parser.parse('Specifications/'+filename+'.txt',
                                    overrideParams)

    # DERIVE and INTERPRET together
    n               = Specification['depth']
    axiom           = Specification['axiom']
    tree            = [axiom]
    vertices        = []
    for i in range(0,n):
        tree = Deriver.derive(tree,1)
        vertices        = Interpreter.interpret(tree, return_analysis)
        print("Interpreted for the "+str(i+1)+"th time.")

    # IF BEING USED IN MODEL FITTING
    if return_analysis == True:
        return vertices

    # IF BEING USED FOR RENDERING, WRITE TO FILE
    else:
        print("writing to file...")
        with open("data.dat", mode="w") as f:
            f.write(str(len(vertices))+"\n")
            for vertex in vertices:
                for feature in vertex:
                    f.write(str(feature)+"\t")
                f.write("\n")
# END GENERATE_SELF_ORGANISING_MODEL -------------------------------------------


def analyse_model(points): # ---------------------------------------------------
    # In the real world, points wouldn't contain any extra information.
    # Since we're only fitting to our own models, we ensure that
    # The interpreter has labelled the tree with data for our use
    metrics = Analyser.analyse(points)
    return metrics
# END ANALYSE_MODEL ------------------------------------------------------------


def generate_and_analyse(filename, overrideParams, print_metrics=False, spec={}, parse=True): # -----
    # Directly called by PyABC
    tree_data =[]
    if parse == True:
        tree_data = generate_model(filename, overrideParams, return_analysis=True)
    else:
        tree_data = generate_model(filename, overrideParams, return_analysis=True, parse=False, spec=spec)
    metrics   = analyse_model(tree_data)

    if print_metrics == True:
        print('---------------')
        print('Model summary')
        print('---------------')
        print()

        for (k,v) in metrics.items():
            print(k, ':', v)
            print()

    return metrics
# END GENERATE_AND_ANALYSE -----------------------------------------------------


if __name__ == '__main__': # ---------------------------------------------------
    # Called directly by treeMod8000.exe to populate data file
    filename = sys.argv[1]
    generate_model(filename)
# END RENDER -------------------------------------------------------------------
