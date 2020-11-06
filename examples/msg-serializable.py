#!/usr/bin/env python3

# Copyright (C) 2014 The python-bitcoinlib developers
#
# This file is part of python-bitcoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

"""Serialize some omnicore datastructures and show them in serialized and repr form."""

import sys

if sys.version_info.major < 3:
    sys.stderr.write("Sorry, Python 3.x required by this example.\n")
    sys.exit(1)

from omnicore import SelectParams
from omnicore.messages import msg_version, msg_tx, msg_block

SelectParams("mainnet")


for c in [msg_version, msg_tx, msg_block]:
    # Instanciate the message with some default values
    msg = c()
    name = c.__name__
    print(name + " repr:")
    print(msg)
    print(name + " serialized:")
    print(msg.to_bytes())
