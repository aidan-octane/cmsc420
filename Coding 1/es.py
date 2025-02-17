# Extensible Stack
# Basically a stack but works by pre-allocating space.
# When we overflow the stack we allocate to a new length
# and copy the old contents over.

from __future__ import annotations
from typing import List
import json

# The Extensible Stack class.
# DO NOT MODIFY!
class EStack():
    def  __init__(self,
                  m : int,
                  b : int):
        self.m               = m
        self.b               = b
        self.allocatedlength = 1
        self.currentpointer  = 0
        self.data            = [None]

    # DO NOT MODIFY!
    def esdump(self) -> str:
        return json.dumps(self.data)

    # Push an integer onto the stack.
    # This should put something at index currentpointer.
    # If we overflow the stack then create a new stack
    # of length m * stacklength + b.
    # Copy the data over and then push.

    def espush(self,x:int):
        if self.currentpointer < len(self.data):
            # Add x to data array
            self.data[self.currentpointer] = x
            self.currentpointer = self.currentpointer + 1
        else:
            # Create new stack
            # print("Reallocating to size " + str((len(self.data) * self.m) + self.b))
            new_data = [None] * ((len(self.data) * self.m) + self.b)
            for i in range (0, self.currentpointer):
                new_data[i] = self.data[i]
            self.data = new_data
            # Copy data over
            self.data[self.currentpointer] = x
            self.currentpointer = self.currentpointer + 1


    # Pop an integer off the stack quietly,
    # meaning just do it and don't return anything.

    def espop_quiet(self):
        # Pop off stack
        self.currentpointer = self.currentpointer - 1
        self.data[self.currentpointer] = None

    # Pop an integer off the stack and return it.

    def espop(self):
        # Pop off stack + return popped value
        self.currentpointer = self.currentpointer - 1
        r = self.data[self.currentpointer]
        self.data[self.currentpointer] = None
        return r