import sys, Parser, Deriver, Interpreter, Analyser

def generate_model(filename, overrideParams={}, return_analysis=False): # ---------
    # PARSE
    Specification   = Parser.parse('Specifications/'+filename+'.txt', overrideParams)

    # DERIVE
    n               = Specification['depth']
    axiom           = Specification['axiom']
    tree            = [axiom]
    tree            = Deriver.derive(tree,n)
    #print("tree of length: "+str(len(tree)))

    # INTERPRET
    vertices        = Interpreter.interpret(tree, return_analysis)
    #print("converted to vertex array of len: " + str(len(vertices)))

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


def generate_and_analyse(filename, overrideParams, print_metrics=False): # -----
    # Directly called by PyABC

    tree_data = generate_model(filename, overrideParams, return_analysis=True)
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
    generate_self_org_model(filename)
# END RENDER -------------------------------------------------------------------
