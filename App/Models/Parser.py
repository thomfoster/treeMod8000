from Cell import Cell, Exp, Lin, Pow, Sig
from Cell import Specification as cell_copy_of_spec_dict # Stores accessible spec data for each cell to use

Specification = cell_copy_of_spec_dict

# DEFINE SOME DEFAULT VALUES FOR WHEN THINGS UNSPECIFIED
Specification['age_limit'] = 1000
Specification['gen_limit'] = 1000
Specification['self_org']  = False

def printSections():
    for s in Specification['sections'].items():
        print(s[0])
        for k, v in s[1].items():
            print('\t', end='')
            print(k, end=' = ')
            print(v)

def parseVariable(l):

    line = l.split(" ")

    if line[0] == "float":
        return float(line[2])

    elif line[0] == "string":
        return line[2]

    elif line[0] == "class":
        if line[2] == "Cell":
            return Cell
        elif line[2] == "Exp":
            return Exp
        elif line[2] == "Lin":
            return Lin
        elif line[2] == "Pow":
            return Pow
        elif line[2] == "Sig":
            return Sig

    else:
        raise Exception("Parse variable error: Undefined type: "+l)

def parseRule(pType, args, agent, rule):

    if pType == "GEOM":
        try:
            Specification["sections"][agent]["rules"].append([pType, [float(args[0])], rule])
        except:
            Specification["sections"][agent]["rules"] = []
            Specification["sections"][agent]["rules"].append([pType, [float(args[0])], rule])

    else:
        raise Exception('Rule type not recognised: ' + pType)


def parse(filepath, overrideParams):

    f = open(filepath, 'r')

    # Contains all information in model specification file
    global Specification
    Specification['defaults'] = {}
    Specification['sections'] = {}

    state = 1
    section = 0

    for l in f:
        line = l[:-1].split(" ")

        if state == 1:

            if line[0] == "START":
                Specification['axiom'] = line[2]
                continue

            elif line[0] == "GENERATION_LIMIT":
                if line[1] == "None":
                    continue
                else:
                    Specification['gen_limit'] = float(line[1])
                continue

            elif line[0] == "AGE_LIMIT":
                if line[1] == "None":
                    continue
                else:
                    Specification['age_limit'] = float(line[1])
                continue

            elif line[0] == "DEPTH":
                Specification['depth'] = int(line[1])

            elif line[0] == "DEFINE":
                Specification['defaults'][line[2]] = parseVariable(l[7:-1])
                continue

            elif line[0] == "SECTION":
                state = 2
                section = line[1]
                Specification["sections"][section] = {}
                continue

            elif line[0] == "THICKNESS":
                Specification['thickness'] = float(line[1])
                continue

            elif line[0] == "SELF_ORG":
                Specification['self_org'] = bool(int(line[1]))
                continue

            elif line[0] == "NUM_VOXELS":
                Specification['num_voxels'] = int(line[1])
                continue

            elif line[0] == "SHADOW_WIDTH":
                Specification['shadow_width'] = int(line[1])
                continue

            elif line[0] == "SHADOW_HEIGHT":
                Specification['shadow_height'] = int(line[1])
                continue

            elif line[0] == "DEC_AT_0":
                Specification['dec_close'] = float(line[1])
                continue

            elif line[0] == "DEC_AT_1":
                Specification['dec_far'] = float(line[1])
                continue

            elif line[0] == "RULE":

                distribution = line[1]
                pType = distribution.split('(')[0]
                args  = distribution.split('(')[1][:-1].split(',')

                agent = line[2]
                rule  = line[4]

                # Generally defined rule
                if agent == 'C':
                    for section in Specification['sections'].keys():
                        Specification['sections'][section]['id'] = section
                        formattedRule = rule.replace('C', section)

                        try:
                            formattedRule = formattedRule.replace('N', Specification['sections'][section]['next'])
                            #print('Used section defined next')
                        except:
                            try:
                                formattedRule = formattedRule.replace('N', Specification['defaults']['next'])
                                #print('Used default defined next')
                            except:
                                next = str(int(section)+1)
                                formattedRule = formattedRule.replace('N', next)
                                Specification['sections'][section]['next'] = next
                                #print('Used automatic next')

                        parseRule(pType, args, section, formattedRule)

                # ?? Add in agent is float check here for the general rule specification

                # Explicitly define rule
                else:
                    parseRule(pType, args, agent, rule)

        elif state == 2:

                if line[0] == "END":
                    state = 1
                    continue

                else:
                    Specification["sections"][section][line[1]] = parseVariable(l[:-1])

    # All lines now read

    # Add id param and defaults to every section
    for section in Specification['sections'].keys():
        Specification['sections'][section]['id'] = section
        for k,v in Specification['defaults'].items():
            try:
                v = Specification['sections'][section][k]
            except:
                Specification['sections'][section][k] = v

    # Override parameters in specification file to those set by PyABC
    for (k,v) in overrideParams.items():

        type = k.split('_')[0]

        if type == 'default':
            key = k.split('_')[1]
            for section in Specification['sections'].keys():
                Specification['sections'][section][key] = v

        elif type == 'rule':
            agent = k.split('_')[1]
            id = k.split('_')[2]
            Specification['sections'][agent]['rules'][int(id)][1] = [v]

        elif type == 'section':
            section = k.split('_')[1]
            key = k.split('_')[2]
            Specification['sections'][section][key] = v

        elif type == 'general':
            key = k.split('_')[1]
            Specification[key] = v

        else:
            raise Exception("Extra parameter key not recognised: "+k)

    # Update axiom width to be starting thickness for turtle
    sec_num_of_axiom = Specification['axiom']
    start_thickness  = Specification['thickness']
    Specification['sections'][sec_num_of_axiom]['width'] = start_thickness
    # Axiom couldn't be constructed until info about it's class parsed...
    # ...So do that now.
    axiomData = Specification['sections'][sec_num_of_axiom]
    axiom = axiomData['constructer'](**axiomData)
    Specification['axiom'] = axiom

    return Specification
