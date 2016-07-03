import pycub.code as code
import pycub.ops as operator

class Expression(object):
  def __init__(self):
    pass

  # accepts the current block, returns the block the expression will end in
  def gen(self, block):
    raise NotImplementedError("expressions must implement gen")

  def capture(self):
    # TODO: ParseError or something
    raise Exception("cannot capture this expression")

class CallNode(Expression):
  def __init__(self, callee, args):
    self.callee = callee
    self.args = args

  def gen(self, block):
    raise NotImplementedError("TODO: implement me")

class FunctionNode(Expression):
  def __init__(self, fn):
    self.function = fn

################################################################################
## literal nodes
################################################################################

class LiteralNode(Expression):
  def __init__(self, literal_type, value):
    self.literal_type = literal_type
    self.value = value

  def gen(self, block):
    block.addOp(code.Operation(operator.O_LITERAL, self.literal_type, [self.value]))
    return block

################################################################################
## binary nodes
################################################################################

def binary_factory(operator, operandType, resultType):
  return lambda left, right: BinaryNode(operator, operandType, resultType, left, right)

class BinaryNode(Expression):
  def __init__(self, operator, operandType, resultType, left, right):
    self.operator = operator
    self.operandType = operandType
    self.resultType = resultType
    self.left = left
    self.right = right

  def gen(self, block):
    block = self.left.gen(block)
    if not self.operandType(block.lastOp().resultType):
      # TODO: better analysis errors
      raise TypeError("string expected")
    binding = code.Binding()
    block.bind(code.Binding(), block.lastOp())
    block = self.right.gen(block)
    if not self.operandType(block.getLastOp().resultType):
      # TODO: better analysis errors
      raise TypeError("string expected")
    left = block.unbind(binding)
    right = block.lastOp
    block.addOp(code.Operation(self.operator, self.resultType, [left, right]))
    return block

# TODO: type casting
# StrConcatNode = binary_factory(operator.O_STR_CONCAT, types.isStr, lambda l, r: types.T_STRING)
# AShiftNode = binary_factory(operator.O_ASHIFT, types.isInt, None)
# LShiftNode = binary_factory(operator.O_LSHIFT, types.isInt, None)
# RShiftNode = binary_factory(operator.O_RSHIFT, types.isInt, None)
# BAndNode = binary_factory(operator.O_BAND, types.isNum, None)
# BOrNode = binary_factory(operator.O_BOR, types.isNum, None)
# BXOrNode = binary_factory(operator.O_BXOR, types.isNum, None)
# AddNode = binary_factory(operator.O_ADD, types.isNum)
# DivNode = binary_factory(operator.O_DIV, types.isNum)
# ModNode = binary_factory(operator.O_MOD, types.isNum)
# MulNode = binary_factory(operator.O_MUL, types.isNum)
# SubNode = binary_factory(operator.O_SUB, types.isNum)

################################################################################
## getters and setters and associated capture objects
################################################################################

class Capture(object):
  def __init__(self):
    pass

  def get(self):
    raise NotImplementedError("capture objects must implement get")

  def set(self, right):
    raise NotImplementedError("capture objects must implement set")

# just exists as a reference
class BindingNode(Expression):
  def __init__(self):
    pass

  def gen(self, block):
    raise NotImplementedError("TODO: implement me")

class BindNode(Expression):
  def __init__(self, binding, value, body):
    self.binding = binding
    self.value = value
    self.body = body

  def gen(self, block):
    # add the binding to the block, so that subsequent bindings can
    raise NotImplementedError("TODO: implement me")

class SymbolCapture(Capture):
  def __init__(self, symbol):
    self.symbol = symbol

  def get(self):
    return GetSymbolNode(self.symbol)

  def set(self, right):
    return SetSymbolNode(self.symbol, right)

class GetSymbolNode(Expression):
  def __init__(self, symbol):
    self.symbol = symbol

  def capture(self):
    return SymbolCapture(self.symbol)

  def gen(self, block):
    raise NotImplementedError("TODO: implement me")

class SetSymbolNode(Expression):
  def __init__(self, symbol, value):
    self.symbol = symbol
    self.value = value

  def gen(self, block):
    raise NotImplementedError("TODO: implement me")

class FieldCapture(Capture):
  def __init__(self, obj, field):
    self.uref = UniqueRef()
    self.obj = obj # construct expression
    self.field = field

  def get(self):
    return GetFieldNode(self.uref, self.field)

  def set(self, right):
    # the corresponding get might not be part of the right expression - with a
    # normal assign, we want to capture the array value before evaluating the
    # right-hand side
    setter = SetFieldNode(self.uref, self.field, right)
    return BindNode(self.uref, self.obj, setter)

class GetFieldNode(Expression):
  def __init__(self, obj, field):
    self.obj = obj
    self.field = field

  def capture(self):
    return FieldCapture(self.obj, self.field)

  def gen(self, block):
    # add the getter to the block
    raise NotImplementedError("TODO: implement me")

class SetFieldNode(Expression):
  def __init__(self, obj, field, value):
    self.obj = obj
    self.field = field
    self.value = value

  def gen(self, block):
    # add the setter to the block
    raise NotImplementedError("TODO: implement me")

class IndexCapture(Capture):
  def __init__(self, obj, index):
    self.uref = UniqueRef()
    self.obj = obj
    self.index = index

  def get(self):
    return GetIndexNode(self.uref, self.index)

  def set(self, right):
    # the corresponding get might not be part of the right expression - with a
    # normal assign, we want to capture the array value before evaluating the
    # right-hand side
    setter = SetIndexNode(self.uref, self.index, right)
    return BindNode(self.uref, self.obj, setter)

class GetIndexNode(Expression):
  def __init__(self, obj, index):
    self.obj = obj
    self.index = index

  def capture(self):
    return IndexCapture(self.obj, self.index)

  def gen(self, block):
    # add the getter to the block
    raise NotImplementedError("TODO: implement me")

class SetIndexNode(Expression):
  def __init__(self, obj, index, value):
    self.obj = obj
    self.index = index
    self.value = value

  def gen(self, block):
    # add the setter to the block
    raise NotImplementedError("TODO: implement me")







# all binary
# assignOperators = {
#   tokens.L_ASSIGN: None,
#   tokens.L_STR_CONCAT_ASSIGN: binary_factory(operator.O_STR_CONCAT, T_STRING, T_STRING),
#   tokens.L_ASHIFT_ASSIGN: binary_factory(operator.O_ASHIFT, AShiftNode,
#   tokens.L_LSHIFT_ASSIGN: LShiftNode,
#   tokens.L_RSHIFT_ASSIGN: RShiftNode,
#   tokens.L_ADD_ASSIGN: AddNode,
#   tokens.L_BAND_ASSIGN: BAndNode,
#   tokens.L_BOR_ASSIGN: BOrNode,
#   tokens.L_BXOR_ASSIGN: BXOrNode,
#   tokens.L_DIV_ASSIGN: DivNode,
#   tokens.L_MOD_ASSIGN: ModNode,
#   tokens.L_MUL_ASSIGN: MulNode,
#   tokens.L_SUB_ASSIGN: SubNode
# }

# def desugar(node):
#   if node.type in assignOperators:
#     NewNode = assignOperators[node.type]
#     capture = node.left.capture()
#     value = capture.get()
#     if NewNode is not None:
#       value = NewNode(value, node.right)
#     return capture.set(value)
#   return node
