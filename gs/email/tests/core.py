# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from mock import patch
from unittest import TestCase
from gs.email.core import send_email
import gs.email.core


class TestCore(TestCase):
    addrs = ['person@people.example.com', 'member@members.example.com',
             'individual@people.example.com', 'admin@members.example.com', ]

    @patch('gs.email.core.getUtility')
    @patch('gs.email.core.create_emailUtilities')
    def test_no_dest(self, ceuMock, getUtilityMock):
        mailerMock = getUtilityMock()
        send_email('durk@example.com', [], 'This is an email')
        self.assertEqual(0, mailerMock.send.call_count)

    @patch('gs.email.core.getUtility')
    @patch('gs.email.core.create_emailUtilities')
    def test_str_dest(self, ceuMock, getUtilityMock):
        'Test when the destination is a string'
        mailerMock = getUtilityMock()
        send_email('durk@example.com', 'dinsdale@example.com',
                   'This is an email')
        self.assertEqual(1, mailerMock.send.call_count)

    @patch('gs.email.core.getUtility')
    @patch('gs.email.core.create_emailUtilities')
    def test_list_dest(self, ceuMock, getUtilityMock):
        'Test when the destination is a list'
        mailerMock = getUtilityMock()
        send_email('durk@example.com', self.addrs, 'This is an email')
        self.assertEqual(1, mailerMock.send.call_count)

    @patch('gs.email.core.getUtility')
    @patch('gs.email.core.create_emailUtilities')
    def test_batch(self, ceuMock, getUtilityMock):
        'Do we batch the requests'
        gs.email.core.max_batch = 2
        mailerMock = getUtilityMock()
        send_email('durk@example.com', self.addrs, 'This is an email')
        self.assertEqual(2, mailerMock.send.call_count)
        gs.email.core.max_batch = 50
