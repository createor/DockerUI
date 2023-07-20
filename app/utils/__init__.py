#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from .client import Client
from .verifiyCode import Code
from .pool import Pool

cli = Client().instance()
code = Code().instance()
code.task()
cache_pool = Pool().instance()
