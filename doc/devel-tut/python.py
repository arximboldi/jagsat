
"""

PYTHON TUTORIAL
===============

This is just a small and personal introduction,
for reference, please look at the great Python
documentation:

http://docs.python.org/library


1. BASIC SYNTAX
---------------

In Python there is a notion of 'block' like in
Java or C++ or any other language that you might
now.

- Blocks by indentation: Everything *statement* a
  block is in the same level.

Example:

"""

if True:
    print "I'm indented."
    print "We are into the block."
else:
    print "I'm someone else."

"""

Some times you might need to *break lines*:

   - Use \ at the end of the line.
   - Use parentheses around the expression.
   
"""

one_long_expression = (1 + 2 + 3 + 4 + 5 +
                       6 + 7 + 8 + 9)

if one_long_expression or \
   not one_long_expression:
    print "That line was broken"


"""

You can also sequence statements with ';'

"""

print 'hello'; print 'goodbie'

"""

BASIC CONCEPTS
--------------

1. EVERYTHING is an object!

   a) Simple type values.
   b) Classes and types.
   c) Functions.
   d) Modules.

2. EVERYTHING is dynamic!:

   - You just have a script that executes.
   - Assignment is just binding:

             name = object

   - Every name is a binding, that you can modify
   with the binding operator (=).

3. Some notes about the SCOPE:

   - There IS NOT such a thing as BLOCK scope.
   - There IS function level scope.
   - There IS class level scope.
   - There IS module level scope.

"""

name = 1
print "> (module) name:", name
class ScopeTest:
    print "> (class) name:", name        
    def function (self):
        print "> (function) name:", name
a = ScopeTest ()
a.function ()

"""

If we bind something to the name, the name becomes
local.

"""

name = 1
print "> (module) name:", name
class ScopeTest:
    print "> (class) name:", name
    name = 2
    print "< (class) name:", name
    
    def function (self):
        global name
        print "> (function) name:", name
        name = 3
        print "< (function) name:", name
        
print "< (module) name:", name
a = ScopeTest ()
a.function ()


"""

BASIC TYPES
-----------

1. INMUTABLE types:

   - A value can not be changed (but a name can be
     re-binded).
   - Examples:
     a) int:      1, 2, 3...
     b) float:    1.32, .45e2
     c) bool:     True, False
     d) complex:  3+2j
     c) string:   'something', \"something\", ...
     e) tuples:   (a, b, c), (1, 2, 3)
     f) None

"""

i = 2
i += 3

a = 'StrInG'
b = a.lower ()
print a, b

def swap (x, y):
    return x, y
c = swap (a, b)
print c             # not unpacked
print c [1]

z, w = c
print z, w

a, b = swap (a, b)  # unpacking
print a, b


"""

2. MUTABLE types:

   - A value can be modified.
   - Examples:
     a) User objects.
     b) Lists.
     c) Dictionaries.

"""

a = ['1', '2', '3', '4']
a.remove ('3')
print a
del a [2]
print a

a = ['1', '2', '3', '4']
print a [::2]

b = {'hello' : 1,
     'world' : 2 }
b ['world'] = 0
del b ['hello']
print b

class Duck:
    pass
c = Duck ()
c.member = 'new value'
print c.member

"""

OPERATORS
---------

Typical ones, refere to reference. Some notes for
Java or C++ developers:

  - There is operator overloading.
  - There is no ++, -- operator.
  - Conditionals a bit diferent: or, and, ...
  - Operator 'in'
  - Operator [] is very cool.
  - Identity vs equality:

    a) Identity (is) identifies the object. Two
       different objects are always different.
       Like Java ==
       
    b) Equality (==) compares the object
       structure.
       Like Java obj.equals ()

    (Be careful with inmutables)

"""

a = [1, 2, 3]
b = [1, 2, 3]
print a is b
print a == b

a = 'kiitos'
b = 'kiitos'
print a is b
print a == b

"""

CONTROL STRUCTURES
------------------

a) IF:

"""

x = 1
if x == 1:
    print 'one'
elif x == 2:
    print 'two'
else:
    print 'three'

cond = 'one' if x == 1 else 'two'
print cond


"""

b) WHILE:

"""

x = 1
while x < 5:
    print x
    x += 1

"""

c) FOR x IN something:

"""

for x in ['a', 'b', 'c']:
    print x

for x in range (1, 5):
    print x

even_squares = \
    (x*x for x in range (1, 10) if x%2 == 0)

for x in even_squares:
    print x

even_squares_list = \
    [x*x for x in range (1, 10) if x%2 == 0]
print even_squares_list

"""

FUNCTIONS
---------

1. Basics:

   - Syntax: def func (params): ...
   
   - Calling: f (param_1, param_2)

   - Return: return something

   - Default return value: None
     (Every function call is an expression)

"""

def sum2 (param1, param2):
    return param1 + param2
x = sum2 (1, int ('3'))
print x

def empty ():
    pass

x = empty ()
print x

"""

2. Functions are objects:

   - They can be defined anywhere (its just
     binding)
   - They can be binded to any name.
   - They can be anonymous.

"""

def make_sum (n):
    def sum_n (x):
        return x + n
    return sum_n

sum1 = make_sum (1)
sum5 = make_sum (5)

print sum1 (1)
print sum5 (1)

make_sum = lambda n: (lambda x: x + n)

sum9 = make_sum (9)

print sum9 (2)

"""

4. You can use default values for
   parameters.

   NOTE: they are created on DEFINITION time!

"""

def func (para = None, foo = 3, baaar = 2):
    if para is None:
        para = [1, 2]
    return foo

a = func ()
a.append (3)
print func ()

"""

5. We can use keywords for optional parameters:

"""

a = func (foo = ['a', 'b'])
print a


"""

6. Variable number of arguments:

"""

def func (para, *args, **kws):
    print (para, args, kws)

func (1, 2, 3, a = 1, b = 2)

def func (a, b, c = 3):
    print a, b, c

func (*[1, 2], **{'c' : 5})

"""

CLASSES AND OBJECTS
-------------------

1. Syntax:

class ClassName:
    <statement>
    <class member assignment>

Functions make the (self) explicit!

"""

class Duck:
    print 'hello'

    member = 10  # This is part of the class
    
    def quack (self):
        print 'quack'

a = Duck () # Constructor!
b = Duck ()
a.quack ()

print Duck._Duck__member

"""
   - And what about instance variables?
"""

a = Duck ()
a.member = 5  # Creates an instance variable

print a.member
print Duck.member

b = Duck ()
print b.member

"""
   - We use 'a.something = somewhat' to create an
     instance variable. We can do it everywhere.
     Methodology: Do it always in the constructor.

   - There is no 'access restriction', use
     methodology:
"""

class Duck:

    def __init__ (self):
        self.public_member = 10
        self._private_member = 5

    def quack (self):
        print 'quack:', self._private_member

"""

   - Polymorphism: DUCK TYPING!

     a) The attribute is requested in runtime.

     b) The type only matters for inheriting
     features on instance construction time, but
     not on attribute access time.
     
"""

class Duck:
    weight = 5
    def quack (self):
        print 'quack'

class BigDuck:
    weight = 20
    def quack (self):
        print 'QUACK'

def please_quack (duck):
    duck.quack ()

a = Duck ()
b = BigDuck ()

please_quack (a)
please_quack (b)

"""

   - Since Python 2.2 you can inherit form
     (object) to get new-style class which has more
     features. (Discuss later)

   - Python supports multiple inheritance.

   - Syntax:

   class Class (Base1, Base2, ...):
       pass

   - Resolution Method:
       a) Old style: DFS
       b) New style: Complex ;)
   http://www.python.org/download/releases/2.3/mro/

   - Resolve ambiguities:
       Class.method (object)

"""

class SuperDuck (Duck, BigDuck):
    pass

a = SuperDuck ()
a.quack ()

BigDuck.quack (a)

"""
   - Overriding: One can always override(*) both
     methods and attributes in the derived classed. 
"""

class MediumDuck (Duck):
    weight = 10
    def quack (self):
        print "QuAcK"

a = MediumDuck ()
a.quack ()

"""

   - Be careful, there is no 'ad-hoc overloading'
     (C++ like overloading)
   - But can be 'emulated' with default parameters.

"""

class WrongDuck (Duck):
    def quack (self, param=3):
        print ['quack' for _ in range (1, 5)]

a = WrongDuck ()
a.quack (5)
please_quack (a)


"""

  - Be careful: No automatic call to superclass
    constructor.
    
"""

def Base:
    def __init__ (self):
        self._base_attr = 10

def WrongDeriv (Base):
    def __init__ (self):
        self._deriv_attr = 10

def GoodDeriv (Base):
    def __init__ (self):
        Base.__init__ (self)
        self._deriv_attr = 10

"""
  - On new-style classes you can use:
    super (type, [object])

    to get a proxy object that delegates calls to
    parent or sibling classes.
"""

class NewBase (object):
    def __init__ (self):
        self._base_attr = 42

class NewGoodDeriv (NewBase):
    def __init__ (self):
        super (NewGoodDeriv, self).__init__ ()
        self._deriv_attr = 'sth'

a = NewGoodDeriv ()

"""

MODULES
-------

  - Every file.py is a module.

  - Modules are hierarchical. A folder is a module
    if it has a __init__.py file --can be empty.

  - Modules are objects.
  
"""

# example of module
import fib

print fib.fibonacci (10)
print fib.fib10

fib.fib10 = 10   # careful, no constants!
print fib.fib10

# example of module as object
f = fib
print f.fibonacci (10)

# example of hierarchical module
import os.path
print os.path.join ('dir', 'subdir')

"""

Instead of the module, whe can import just
something from it:

"""

from fib import fibonacci
print fibonacci (5)

from os import path
print path.join ('hola')

"""

TIPS FOR JAVA DEVELOPERS
------------------------

1. Do not use getters and setters.

   - Python has 'properties', things that look
     like attributes but are functions.

   - Use a public variable, you can change it
     afterwards into a property.

   - They only work on new-style classes.

"""

class After (object):

    def __init__ (self):
        self.public = 10

class After (object):

    def __init__ (self):
        self._public = 10
        
    def _set_public (self, public):
        self._public = public
        print 'Setting public to ', public

    def _get_public (self):
        print 'Getting public which is ', \
              self._public
        return self._public

    public = property (_get_public, _set_public)

a = After ()
a.public = 10
a.public



"""

NAMING CONVENTIONS
------------------

"""

"""

UNIT TESTING
------------

"""

"""
ADVANCED TOPICS
---------------

- MORE ON FUNCTIONAL CODE
- REFLEXIVITY
- GENERATORS
- METAPROGRAMMING
- DECORATORS
- DESCRIPTORS
- METACLASSES

"""

