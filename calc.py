class variable:
    def __init__(self, name, degree):
        self.name = name
        self.degree = degree

    def __eq__(self, other):
        return (self.name == other.name) & (self.degree == other.degree)
    def __lt__(self, other):
        return self.name < other.name

class monome_simple:
    def __init__(self, x, i = 1, j = 0):
        self.var = x
        self.nb_simple = i
        self.nb_deriv = j

    def __str__(self):
        s = self.var.name
        return s*self.nb_simple + ("d" + s)*self.nb_deriv
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return [self.var, self.nb_simple, self.nb_deriv] == [other.var, other.nb_simple, other.nb_deriv]
    #return (self.var == other.var) & (self.nb_simple == other.nb_simple) & (self.nb_deriv == other.nb_deriv)
    def __lt__(self, other):
        return [self.var, self.nb_simple, self.nb_deriv] < [other.var, other.nb_simple, other.nb_deriv]
#        return ((self.var < other.var) | ((self.var == other.var) & (self.nb_simple < other.nb_simple)) | ((self.var == other.var) & (self.nb_simple == other.nb_simple) & (self.nb_deriv < other.nb_deriv)))

    def copy(self):
        return monome_simple(self.var, self.nb_simple, self.nb_deriv)

    def len(self):
        return self.nb_deriv + self.nb_simple

    def concat(self, n):
        a = (self.nb_simple + n.nb_simple)%2
        b = self.nb_deriv + n.nb_deriv
       # if (a == 0) and (b == 0):
        #    return monome_simple(e, 0, 0)
       # else :
        return monome_simple(self.var, a, b)

    def is_identity(self):
        a = ((self.nb_deriv == 0) and (self.nb_simple == 0))
#        if a :
#            print("id revealed")
        return a

class monome:
    def __init__(self, l, coeff = 1):
        self.l = [x.copy() for x in l if not x.is_identity()]
        self.coeff = coeff

    def __str__(self):
        s = str(self.coeff)
        for x in self.l:
            s = s + str(x)
        return s
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.l == other.l
    def __lt__(self, other):
        return (self.len() < other.len()) or ((self.len() == other.len()) and (self.l < other.l))

    def copy(self):
        return monome(self.l, self.coeff)

    def pop_first(self):
        return self.l.pop(0)
    def first(self):
        return self.l[0]
    def last(self):
        return self.l[-1]
    def pop_last(self):
        return self.l.pop()
    def append_last(self, x):
        self.l.append(x)

    def mult(self, n):
        if self.l == []:
            m = n.copy()
            m.coeff = (m.coeff * self.coeff)
            return m
        elif n.l == []:
            m = self.copy()
            m.coeff = (m.coeff * n.coeff)
            return m
        elif self.last().var.name == n.first().var.name :
            ls = self.l.copy()
            ln = n.l.copy()
            x = ln.pop(0)
            y = ls.pop()
            mil = y.concat(x)
            l = ls + [mil] + ln
            return monome(l, self.coeff * n.coeff)
        else :
            return monome(self.l + n.l, self.coeff * n.coeff)

    def len(self):
        sum = 0
        for x in self.l:
            sum += x.len()
        return sum

    def trace(self):
        if self.last().var.name == self.first().var.name :
           m = monome(self.l, self.coeff)
           x = m.pop_first()
           y = m.pop_last().concat(x)
           m.append_first(y)
           return m
        else :
            return monome(self.l + n .l, self.coeff * n.coeff)


    def cyclic_permutation(self):
        new = self.copy()
        x = monome([new.pop_first()])
        return new.mult(x)

    def canonical_under_trace(self):
        n = 0
        if not self.l:
            return self.copy()
        else:
            cand = self.cyclic_permutation()
            best = self
            base = self
            base_len = base.len()
            just_changed_base = True
            while (just_changed_base or cand != base) and cand.l:
                print("cand :" + str(cand) +" best : "+ str(best) + " base : " + str(base)+ " bool : " + str(just_changed_base))
                just_changed_base =  False
                if cand < best:
                    best = cand
                    print("best < cand ")
                cand_t = cand.cyclic_permutation()
                #obligé de checker si on a eu de la simplification
                if cand_t.len() < base_len :
                    base = cand_t
                    base_len = base.len()
                    just_changed_base = True
                cand = cand_t
            return best.copy()
    
class polynomial:
    def __init__(self, l):
        ll= [x.copy() for x in l]
        ll = sorted(ll)
        i = 0
        while i+1 < len(ll):
            while (i+1 < len(ll)) and (ll[i] == ll[i+1]):
                ll[i].coeff += ll.pop(i+1).coeff
            if ll[i].coeff ==0:
                ll.pop(i)
            else:
                i +=1
        self.l = ll

    def __str__(self):
        s= ""
        for x in self.l:
            s += str(x)
            s += "+"
        s = s.replace("+-", "-")
        s = s.replace("1e", "e")
        s = s.replace("1x", "x")
        s = s.replace("1d", "d")
        return s[0:-1:1]

    def __repr__(self):
        return str(self)

    def mult(self, other):
        l=[]
        for x in self.l:
            for y in other.l:
                l.append(x.mult(y))
        return polynomial(l)

    def trace(self):
        l = [x.canonical_under_trace() for x in self.l]
        return polynomial(l)
#    def mult(self, other):


x_var = variable("x", 1)
x = monome([monome_simple(x_var, 1, 0)], 1)
dx = monome([monome_simple(x_var, 0, 1)], 1)
e_var = variable("e", 1)
e = monome([monome_simple(e_var, 1, 0)], 1)
print(e)
de = monome([monome_simple(e_var, 0, 1)], 1)
moins = monome([], -1)
y= polynomial([e, x.mult(moins)])
xdxe = x.mult(dx).mult(e)
exdx = e.mult(x).mult(dx)
a = polynomial([xdxe, exdx, de.mult(monome([],-2))])
