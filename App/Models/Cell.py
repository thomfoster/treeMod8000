# ------------------------------------------------------------------------------
# Cell.py
# ------------------------------------------------------------------------------

# <> Defines classes for l system components

# Provides the object oriented classes for our parametric l-system approach
# A basic element of the l system is of type sym, with the classes lin and exp
# extending this to linear and exponential growing cells.

# ------------------------------------------------------------------------------

from random import random

# Defined here as an alternative to every cell having it's own copy.
Specification = {}

class Cell:
    # Specify autovalues
    def __init__(
        self,
        id,
        constructer,
        age             = 0,
        decay           = 1.0,
        slash           = 0,
        plus            = 0,
        d               = 1.0,
        generation      = 0,
        rules           = [],
        h               = 20,
        w               = 1.0,
        slashr         = 0,
        plusr          = 0,
        tropism         = 0,
        next            = 0,
        width           = 0,
        ):

        self.id         = id
        self.constructer= constructer
        self.age        = age
        self.decay      = decay
        self.slash      = slash
        self.plus       = plus
        self.d          = d
        self.generation = generation
        self.rules      = rules # list of (type, args, string) tuples
        self.done       = False
        self.h          = h
        self.w          = w
        self.slashr    = slashr
        self.plusr     = plusr
        self.tropism    = tropism
        self.next       = next # no default as +1 added during parsing if needed
        self.width      = width

    def Age(self):
        self.age += 1

    def Grow(self):
        self.Age()
        if self.done != True and self.age < Specification['age_limit'] and self.generation < Specification['gen_limit']:
            ret = []
            for r in self.rules:
                ret += self.iterateRule(r)
            if ret == []:
                return [self]
            else:
                return ret
        else:
            return [self]

    def iterateRule(self, r):
        ret = []
        if self.doRule(r):
            type, args, str = r
            for chr in str:
                try:
                    id = float(chr)
                    if chr == '0':
                        x = self.Clone()
                        x.done = True
                        ret.append(x)
                    else:
                        ret.append(self.New(chr))
                except ValueError:
                    if chr == '*':
                        x = self.Clone()
                        ret.append(x)
                    else:
                        ret.append(chr)
        return ret

    def doRule(self, r):
        type, args, str = r
        if type == "GEOM":
            i = random()
            if i < args[0]:
                return True
            return False

    def ValueOf(self, symbol):
        if symbol in ['u', 'n', '>', '<']:
            i = random()
            return self.slash + (i-0.5)*2*2*self.slashr
        elif symbol in ['+', '-']:
            i = random()
            return self.plus + (i-0.5)*2*2*self.plusr
        elif symbol == "D":
            return self.d
        else:
            raise Exception("ValueOf Key Error: symbol not recognised")

    def Decay(self):
        return self.decay

    def Length(self):
        return 0

    def Clone(self):
        return self.constructer(**Specification['sections'][self.id], generation=self.generation, age=self.age)

    def New(self, chr):
        constructer = Specification['sections'][chr]['constructer']
        return constructer(**Specification['sections'][chr], generation=1+self.generation, age=0)

# ------------------------------------------------------------------------------
# CHILD CLASSES
# ------------------------------------------------------------------------------

class Exp(Cell):
    def Length(self):
        return 2**(self.age)

class Lin(Cell):
    def Length(self):
        return float(self.age)

class Pow(Cell):
    def Length(self):
        return self.age**self.h

class Sig(Cell):
    def Length(self):
        max_age = min(Specification['age_limit'], Specification['depth'])
        return self.h*2/(1+(2**(-self.w*(self.age-max_age))))










































#End
