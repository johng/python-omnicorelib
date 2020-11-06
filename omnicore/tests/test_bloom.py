# Copyright (C) 2013-2014 The python-bitcoinlib developers
#
# This file is part of python-bitcoinlib.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

import omnicore.core
from omnicore.core import x
from omnicore.bloom import *


class Test_MurmurHash3(unittest.TestCase):
    def test(self):
        def T(expected, seed, data):
            self.assertEqual(MurmurHash3(seed, x(data)), expected)

        T(0x00000000, 0x00000000, "")
        T(0x6A396F08, 0xFBA4C795, "")
        T(0x81F16F39, 0xFFFFFFFF, "")

        T(0x514E28B7, 0x00000000, "00")
        T(0xEA3F0B17, 0xFBA4C795, "00")
        T(0xFD6CF10D, 0x00000000, "ff")

        T(0x16C6B7AB, 0x00000000, "0011")
        T(0x8EB51C3D, 0x00000000, "001122")
        T(0xB4471BF8, 0x00000000, "00112233")
        T(0xE2301FA8, 0x00000000, "0011223344")
        T(0xFC2E4A15, 0x00000000, "001122334455")
        T(0xB074502C, 0x00000000, "00112233445566")
        T(0x8034D2A0, 0x00000000, "0011223344556677")
        T(0xB4698DEF, 0x00000000, "001122334455667788")


class Test_CBloomFilter(unittest.TestCase):
    def test_create_insert_serialize(self):
        filter = CBloomFilter(3, 0.01, 0, CBloomFilter.UPDATE_ALL)

        def T(elem):
            """Filter contains elem"""
            elem = x(elem)
            filter.insert(elem)
            self.assertTrue(filter.contains(elem))

        def F(elem):
            """Filter does not contain elem"""
            elem = x(elem)
            self.assertFalse(filter.contains(elem))

        T("99108ad8ed9bb6274d3980bab5a85c048f0950c8")
        F("19108ad8ed9bb6274d3980bab5a85c048f0950c8")
        T("b5a2c786d9ef4658287ced5914b37a1b4aa32eee")
        T("b9300670b4c5366e95b2699e8b18bc75e5f729c5")

        self.assertEqual(filter.serialize(), x("03614e9b050000000000000001"))
        deserialized = CBloomFilter.deserialize(x("03614e9b050000000000000001"))

        self.assertTrue(
            deserialized.contains(x("99108ad8ed9bb6274d3980bab5a85c048f0950c8"))
        )
        self.assertFalse(
            deserialized.contains(x("19108ad8ed9bb6274d3980bab5a85c048f0950c8"))
        )
        self.assertTrue(
            deserialized.contains(x("b5a2c786d9ef4658287ced5914b37a1b4aa32eee"))
        )
        self.assertTrue(
            deserialized.contains(x("b9300670b4c5366e95b2699e8b18bc75e5f729c5"))
        )

    def test_create_insert_serialize_with_tweak(self):
        # Same test as bloom_create_insert_serialize, but we add a nTweak of 100
        filter = CBloomFilter(3, 0.01, 2147483649, CBloomFilter.UPDATE_ALL)

        def T(elem):
            """Filter contains elem"""
            elem = x(elem)
            filter.insert(elem)
            self.assertTrue(filter.contains(elem))

        def F(elem):
            """Filter does not contain elem"""
            elem = x(elem)
            self.assertFalse(filter.contains(elem))

        T("99108ad8ed9bb6274d3980bab5a85c048f0950c8")
        F("19108ad8ed9bb6274d3980bab5a85c048f0950c8")
        T("b5a2c786d9ef4658287ced5914b37a1b4aa32eee")
        T("b9300670b4c5366e95b2699e8b18bc75e5f729c5")

        self.assertEqual(filter.serialize(), x("03ce4299050000000100008001"))

    def test_bloom_create_insert_key(self):
        filter = CBloomFilter(2, 0.001, 0, CBloomFilter.UPDATE_ALL)

        pubkey = x(
            "045B81F0017E2091E2EDCD5EECF10D5BDD120A5514CB3EE65B8447EC18BFC4575C6D5BF415E54E03B1067934A0F0BA76B01C6B9AB227142EE1D543764B69D901E0"
        )
        pubkeyhash = omnicore.core.Hash160(pubkey)

        filter.insert(pubkey)
        filter.insert(pubkeyhash)

        self.assertEqual(filter.serialize(), x("038fc16b080000000000000001"))
