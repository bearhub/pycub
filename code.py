from numbers import Real as real
from itertools import repeat, islice
from collections import Iterable

import pycub.ops as operator
import pycub.types as types

class Value(object):
  def __init__(self, type, value):
    self.type = type
    self.value = value

def not_implemented(msg):
  raise NotImplementedError(msg)

def autoiter(obj):
  if isinstance(obj, Iterable):
    return obj
  return repeat(obj)

def reqchk(check, fn):
  def r(*args):
    for a in args:
      if not check(a):
        raise TypeError("expected " + check.__name__)
    return fn(*args)
  return r

def require(rtypes, fn):
  def r(*args):
    for arg, rtype in zip(args, autoiter(rtypes)):
      if (isinstance(rtype, bool) and not rtype) or not isinstance(a, rtype):
        raise TypeError("expected " + rtype.__name__)
    return fn(*args)
  return r

def defop(expect, fn):
  def run(*args):
    # get the error out of the way
    if not len(args): fn(*args)
    return Value(args[0].type, types.ctype[args[0].type](fn(*(a.value for a in args))))
  return require(expect, run)

def set_index(a, b, c): a[b] = c

class StructValue(object):
  def __init__(self, fields):
    self.values = [None] * len(fields)

  def get(self, index):
    return self.values[index]

  def set(self, index, value):
    self.values[index] = value

def isNum(value):
  return isinstance(value, Value) and types.isNum(value.type)

def isInt(value):
  return isinstance(value, Value) and types.isInt(value.type)

# def isBool(value):
#   return isinstance(value, Value) and value.type == types.T_BOOL

def isPosInt(value):
  return isInt(value) and value.value.value >= 0

operations = {
  # numeric
  operator.O_NEGATE: defop(isNum, lambda a: -a),
  operator.O_ADD: defop(isNum, lambda a, b: a + b),
  operator.O_SUB: defop(isNum, lambda a, b: a - b),
  operator.O_MUL: defop(isNum, lambda a, b: a * b),
  operator.O_DIV: defop(isNum, lambda a, b: a / b),
  operator.O_MOD: defop(isNum, lambda a, b: a % b),

  # bitwise
  operator.O_BITWISE_NOT: defop(isInt, lambda a: ~a),
  operator.O_ASHIFT: require(isInt, lambda a, b: not_implemented(">>>")),
  operator.O_RSHIFT: defop(isInt, lambda a, b: a >> b),
  operator.O_LSHIFT: defop(isInt, lambda a, b: a << b),
  operator.O_BAND: defop(isInt, lambda a, b: a & b),
  operator.O_BOR: defop(isInt, lambda a, b: a | b),
  operator.O_BXOR: defop(isInt, lambda a, b: a ^ b),

  operator.O_NOT: require(bool, lambda a: not a),

  # operator.O_GET_SYMBOL
  operator.O_COPY: lambda value: value,

  # values of array must be manually initialized
  operator.O_NEW_ARRAY: reqchk(isPosInt, lambda length: [None] * length.value),
  operator.O_GET_LENGTH: require(list, lambda l: len(l)),

  # TODO: casting
  operator.O_DOWNCAST: lambda a, b: not_implemented("cast"),
  operator.O_FLOAT_EXTEND: lambda a, b: not_implemented("cast"),
  operator.O_FLOAT_TO_SIGNED: lambda a, b: not_implemented("cast"),
  operator.O_FLOAT_TO_UNSIGNED: lambda a, b: not_implemented("cast"),
  operator.O_FLOAT_TRUNCATE: lambda a, b: not_implemented("cast"),
  operator.O_REINTERPRET: lambda a, b: not_implemented("cast"),
  operator.O_SIGN_EXTEND: lambda a, b: not_implemented("cast"),
  operator.O_SIGNED_TO_FLOAT: lambda a, b: not_implemented("cast"),
  operator.O_TRUNCATE: lambda a, b: not_implemented("cast"),
  operator.O_UNSIGNED_TO_FLOAT: lambda a, b: not_implemented("cast"),
  operator.O_UPCAST: lambda a, b: not_implemented("cast"),
  operator.O_ZERO_EXTEND: lambda a, b: not_implemented("cast"),

  operator.O_EQ: lambda a, b: (a.value == b.value if isinstance(a, Value) and isinstance(b, Value) else a is b),
  operator.O_GT: require(isNum, lambda a, b: a.value > b.value),
  operator.O_GTE: require(isNum, lambda a, b: a.value >= b.value),
  operator.O_LT: require(isNum, lambda a, b: a.value < b.value),
  operator.O_LTE: require(isNum, lambda a, b: a.value >= b.value),
  operator.O_NE: require(isNum, lambda a, b: not_implemented("deprecated !=")),
  # operator.O_IDENTITY: lambda a, b: a is b,

  operator.O_STR_CONCAT: require(str, lambda a, b: a + b),

  operator.O_GET_FIELD: require((StructValue, int), lambda a, b: a.get(b)),
  operator.O_GET_INDEX: require(((list, str), int), lambda a, b: ord(a[b]) if isinstance(a, str) else a[b]),

  operator.O_SET_FIELD: require((StructValue, int, True), lambda a, b, c: a.set(b, c)),
  operator.O_SET_INDEX: require((list, int, True), set_index)
}

special = {
  operator.O_BLOCKREF: require(int, lambda index: index),
  operator.O_NEW: require(int, lambda index: index),
  operator.O_LITERAL: lambda value: value,
  operator.O_INSTANCEOF: require((StructValue, int), lambda a, b: (a, b))
}

def getvar(vars, var):
  if len(vars) <= var:
    raise RuntimeError("ssa var ref undeclared")
  return vars[var]

class Operation(object):
  def __init__(self, type, resultType, params):
    self.type = type
    self.resultType = resultType
    self.params = params

  def eval(self, block, vars, natives):
    params = self.params

    if self.type == operator.O_NATIVE:
      if len(params) == 0:
        raise RuntimeError("incomplete native call")
      if params[0] not in natives:
        raise RuntimeError("unknown native call")
      args = (getvar(vars, arg) for arg in islice(params, 1, None))
      value = natives[params[0]](*args)
      # TODO: typecheck
      return value

    if self.type in special:
      call = lambda: special[self.type](*params)

      if self.type == operator.O_LITERAL:
        return call()
      if self.type == operator.O_BLOCKREF:
        return block.program.blocks[call()]
      if self.type == operator.O_NEW:
        return block.program.structs[call()].new()
      if self.type == operator.O_INSTANCEOF:
        obj, index = call()
        obj = block.get(obj)
        struct = block.structs[index]
        return struct.hasValue(obj)
      raise RuntimeError("unknown operation")

    args = (getvar(vars, arg) for arg in params)

    if self.type in operations:
      return operations[self.type](*args)

    raise RuntimeError("unknown operation", self.type)

class Block(object):
  def __init__(self, params=None):
    self.termbranch = False
    self.ops = []
    self.program = None
    if params is None:
      self.params = []
    else:
      self.params = params

  def goto(self, target, params):
    self.branch(None, target, None, params)

  def branch(self, cond, first_target, second_target, params):
    self.termbranch = True
    self.termcond = cond
    self.termfirst = first_target
    self.termsecond = second_target
    self.termparams = params

  def interp(self, vars, natives):
    if self.program is None:
      raise RuntimeError("block is detached")
    if len(vars) != len(self.params):
      raise RuntimeError("ssa block param count mismatch")
    for var, op in enumerate(self.ops):
      vars.append(op.eval(self, vars, natives))
    return self.term(vars)

  def term(self, vars):
    # EXIT
    if not self.termbranch: return None, []
    # BRANCH
    if self.termcond is None: cond = True
    else:
      cond = getvar(vars, self.termcond)
      if not isinstance(cond, bool):
        raise RuntimeError("ssa branch requires bool condition")
    target = getvar(vars, self.termfirst if cond else self.termsecond)
    return target, [getvar(vars, index) for index in self.termparams]

class Struct(object):
  def __init__(self, fields):
    self.fields = fields

  def new(self):
    return StructValue(self.fields)

class Program(object):
  def __init__(self):
    self.blocks = []

  def add_block(self, block):
    block.program = self
    index = len(self.blocks)
    self.blocks.append(block)
    return index

  def interp(self, natives=None):
    if natives is None: natives = {}
    block = self.blocks[0]
    vars = []
    while True:
      index, vars = block.interp(vars, natives)
      if index is None: break
      if len(self.blocks) <= index:
        raise RuntimeError("ssa block ref undeclared")
      block = self.blocks[index]
