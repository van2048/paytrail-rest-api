# -*- coding: utf-8 -*-
__author__ = 'Abradox'

"""
    Paytrail exception is a normal Python exception. Using an inherited
    class allows catching only Paytrail exceptions with try-catch clause.
"""
class PaytrailException(Exception):
    """PayTrail exception"""

    def __init__(self, code, message):
        self.code = code
        self.message = message
