import pycub.tokens as tokens

# operators (expression?, # code args)

O_ADD               = 0 # y, 2
# O_ADD_ASSIGN        = 1 # y, n
# O_AND               = 2 # y, n
O_ASHIFT            = 3 # y, 2
# O_ASHIFT_ASSIGN     = 4 # y, n
# O_ASSIGN            = 5 # y, n
O_BAND              = 6 # y, 2
# O_BAND_ASSIGN       = 7 # y, n
O_BITWISE_NOT       = 8 # y, 1
O_BLOCKREF          = 9 # n, 1
O_BOR               = 10 # y, 2
# O_BOR_ASSIGN        = 11 # y, n
O_BXOR              = 12 # y, 2
# O_BXOR_ASSIGN       = 13 # y, n
# O_CALL              = 14 # y, n
# O_DECREMENT         = 15 # y, n
O_DIV               = 16 # y, 2
# O_DIV_ASSIGN        = 17 # y, n
O_DOWNCAST          = 18 # y, 2
O_EQ                = 19 # y, 2
O_FLOAT_EXTEND      = 20 # y, 2
O_FLOAT_TO_SIGNED   = 21 # y, 2
O_FLOAT_TO_UNSIGNED = 22 # y, 2
O_FLOAT_TRUNCATE    = 23 # y, 2
# O_FUNCTION          = 24 # y, n
O_GET_FIELD         = 25 # y, 2
O_GET_INDEX         = 26 # y, 2
O_GET_LENGTH        = 39 # n, 1
O_COPY              = 27 # y, 1
O_GT                = 28 # y, 2
O_GTE               = 29 # y, 2
O_IDENTITY          = 30 # y, 2
# O_INCREMENT         = 31 # y, n
O_INSTANCEOF        = 32 # y, 2
O_LITERAL           = 33 # y, 0
O_LSHIFT            = 34 # y, 2
# O_LSHIFT_ASSIGN     = 35 # y, n
O_LT                = 36 # y, 2
O_LTE               = 37 # y, 2
O_MOD               = 38 # y, 2
# O_MOD_ASSIGN        = 39 # y, n
O_MUL               = 40 # y, 2
# O_MUL_ASSIGN        = 41 # y, n
O_NATIVE            = 41 # n, y
O_NE                = 42 # y, 2
O_NEGATE            = 43 # y, 1
O_NEW               = 44 # y, 1
O_NEW_ARRAY         = 45 # y, 1
O_NOT               = 46 # y, 1
# O_OR                = 47 # y, n
O_REINTERPRET       = 48 # y, 2
O_RSHIFT            = 49 # y, 2
# O_RSHIFT_ASSIGN     = 50 # y, n
O_SET_FIELD         = 51 # y, 3
O_SET_INDEX         = 52 # y, 3
# O_SET_SYMBOL        = 53 # y, n
O_SIGNED_TO_FLOAT   = 54 # y, 2
O_SIGN_EXTEND       = 55 # y, 2
O_STR_CONCAT        = 56 # y, 2
# O_STR_CONCAT_ASSIGN = 57 # y, n
O_SUB               = 58 # y, 2
# O_SUB_ASSIGN        = 59 # y, n
# O_TERNARY           = 60 # y, n
O_TRUNCATE          = 61 # y, 2
O_UNSIGNED_TO_FLOAT = 62 # y, 2
O_UPCAST            = 63 # y, 2
# O_XOR               = 64 # n, 2
O_ZERO_EXTEND       = 65 # y, 2

# operator groups

O_NO_GROUP           = 0

O_CAST               = 1 # y, 2
O_COMPARE            = 2 # y, 2
O_GET                = 3 # y, y
O_LOGIC              = 4 # y, n
O_NUMERIC            = 5 # y, 2
O_NUMERIC_ASSIGN     = 6 # y, n
O_POSTFIX            = 7 # y, n
O_SET                = 8 # y, y
O_SHIFT              = 9 # y, 2
O_SHIFT_ASSIGN       = 10 # y, n

groups = {
  O_DOWNCAST: O_CAST,
  O_UPCAST: O_CAST,
  O_FLOAT_EXTEND: O_CAST,
  O_FLOAT_TRUNCATE: O_CAST,
  O_FLOAT_TO_SIGNED: O_CAST,
  O_FLOAT_TO_UNSIGNED: O_CAST,
  O_SIGNED_TO_FLOAT: O_CAST,
  O_UNSIGNED_TO_FLOAT: O_CAST,
  O_SIGN_EXTEND: O_CAST,
  O_TRUNCATE: O_CAST,
  O_ZERO_EXTEND: O_CAST,
  O_REINTERPRET: O_CAST,

  O_EQ: O_COMPARE,
  O_GT: O_COMPARE,
  O_GTE: O_COMPARE,
  O_LT: O_COMPARE,
  O_LTE: O_COMPARE,
  O_NE: O_COMPARE,

  O_GET_FIELD: O_GET,
  O_GET_INDEX: O_GET,
  O_GET_LENGTH: O_GET,

  # O_AND: O_LOGIC,
  # O_OR: O_LOGIC,
  # O_XOR: O_LOGIC,

  O_ADD: O_NUMERIC,
  O_BAND: O_NUMERIC,
  O_BOR: O_NUMERIC,
  O_BXOR: O_NUMERIC,
  O_DIV: O_NUMERIC,
  O_MOD: O_NUMERIC,
  O_MUL: O_NUMERIC,
  O_SUB: O_NUMERIC,

  # O_ADD_ASSIGN: O_NUMERIC_ASSIGN,
  # O_BAND_ASSIGN: O_NUMERIC_ASSIGN,
  # O_BOR_ASSIGN: O_NUMERIC_ASSIGN,
  # O_BXOR_ASSIGN: O_NUMERIC_ASSIGN,
  # O_DIV_ASSIGN: O_NUMERIC_ASSIGN,
  # O_MOD_ASSIGN: O_NUMERIC_ASSIGN,
  # O_MUL_ASSIGN: O_NUMERIC_ASSIGN,
  # O_SUB_ASSIGN: O_NUMERIC_ASSIGN,

  # O_INCREMENT: O_POSTFIX,
  # O_DECREMENT: O_POSTFIX,

  O_SET_FIELD: O_SET,
  O_SET_INDEX: O_SET,
  # O_SET_SYMBOL: O_SET,

  O_ASHIFT: O_SHIFT,
  O_LSHIFT: O_SHIFT,
  O_RSHIFT: O_SHIFT,

  # O_ASHIFT_ASSIGN: O_SHIFT_ASSIGN,
  # O_LSHIFT_ASSIGN: O_SHIFT_ASSIGN,
  # O_RSHIFT_ASSIGN: O_SHIFT_ASSIGN
}

# by token
operators = {
  tokens.L_ADD: O_ADD,
  tokens.L_ASHIFT: O_ASHIFT,
  tokens.L_BITWISE_AND: O_BAND,
  tokens.L_BITWISE_OR: O_BOR,
  tokens.L_BITWISE_XOR: O_BXOR,
  tokens.L_DIV: O_DIV,
  tokens.L_EQ: O_EQ,
  tokens.L_GT: O_GT,
  tokens.L_GTE: O_GTE,
  tokens.L_LSHIFT: O_LSHIFT,
  tokens.L_LT: O_LT,
  tokens.L_LTE: O_LTE,
  tokens.L_MOD: O_MOD,
  tokens.L_MUL: O_MUL,
  tokens.L_RSHIFT: O_RSHIFT,
  tokens.L_STR_CONCAT: O_STR_CONCAT,
  tokens.L_SUB: O_SUB
}

class OperatorPrecedence(object):
  def __init__(self, precedence, right_assoc=False):
    self.precedence = precedence
    self.right_assoc = right_assoc

precedences = {
  # precedence 0
  tokens.L_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_TERNARY: OperatorPrecedence(0, right_assoc=True),
  tokens.L_STR_CONCAT_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_ASHIFT_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_LSHIFT_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_RSHIFT_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_ADD_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_BITWISE_AND_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_BITWISE_OR_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_BITWISE_XOR_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_DIV_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_MOD_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_MUL_ASSIGN: OperatorPrecedence(0, right_assoc=True),
  tokens.L_SUB_ASSIGN: OperatorPrecedence(0, right_assoc=True),

  # precedence 1
  tokens.L_OR: OperatorPrecedence(1),

  # precedence 2
  tokens.L_XOR: OperatorPrecedence(2),

  # precedence 3
  tokens.L_AND: OperatorPrecedence(3),

  # precedence 4
  tokens.L_BITWISE_OR: OperatorPrecedence(4),

  # precedence 5
  tokens.L_BITWISE_XOR: OperatorPrecedence(5),

  # precedence 6
  tokens.L_BITWISE_AND: OperatorPrecedence(6),

  # precedence 7
  tokens.L_EQ: OperatorPrecedence(7),
  tokens.L_NE: OperatorPrecedence(7),

  # precedence 8
  tokens.L_STR_CONCAT: OperatorPrecedence(8),

  # precedence 9
  tokens.L_GT: OperatorPrecedence(9),
  tokens.L_GTE: OperatorPrecedence(9),
  tokens.L_LT: OperatorPrecedence(9),
  tokens.L_LTE: OperatorPrecedence(9),

  # precedence 10
  tokens.L_ASHIFT: OperatorPrecedence(10),
  tokens.L_LSHIFT: OperatorPrecedence(10),
  tokens.L_RSHIFT: OperatorPrecedence(10),

  # precedence 11
  tokens.L_ADD: OperatorPrecedence(11),
  tokens.L_SUB: OperatorPrecedence(11),

  # precedence 12
  tokens.L_MUL: OperatorPrecedence(12),
  tokens.L_DIV: OperatorPrecedence(12),
  tokens.L_MOD: OperatorPrecedence(12)
}
