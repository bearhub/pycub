import unittest

import pycub.code as code
import pycub.ops as operator
import pycub.types as types

class TestCode(unittest.TestCase):

  def test_code(self):
    program = code.Program()
    # defaults to exiting
    entry = code.Block()
    entry.ops.append(code.Operation(operator.O_NATIVE, types.T_VOID, ['test_ping']))
    program.add_block(entry)

    called = [0]
    def ping(*args):
      self.assertEqual(len(args), 0)
      called[0] += 1

    program.interp(natives={'test_ping': ping})
    self.assertEqual(called[0], 1)
