# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""
test_lazyengine
----------------------------------

Tests for `lazyengine` module.
"""

import logging
import time

from lazyengine.tests import base
from lazyengine import manager

from taskflow.openstack.common import uuidutils
from taskflow.patterns import linear_flow as flow
from taskflow.persistence.logbook import FlowDetail

from taskflow import states
from taskflow import task

LOG = logging.getLogger(__name__)

manager1uuid = uuidutils.generate_uuid()
manager2uuid = uuidutils.generate_uuid()


def one():
    time.sleep(1)
    return 'one'


def two(one):
    time.sleep(1)
    return 'two'


def three(two):
    pass


fl = flow.Flow('some').add(
    task.FunctorTask(one, provides='one'),
    task.FunctorTask(two, provides='two'),
    task.FunctorTask(three, provides='three')
)


class TestLazyEngine(base.TestCase):

    def test_start_manager1(self):
        execution = FlowDetail(fl.name, manager1uuid)
        manager.start(fl, execution)

    def test_start_manager2(self):
        execution = FlowDetail(fl.name, manager2uuid)
        manager.start(fl, execution)

    def test_stop_manager1(self):
        time.sleep(1.5)
        manager.stop(manager1uuid)

    def test_intermediate_results(self):
        time.sleep(3)
        self.assertEqual(manager.get_state(manager1uuid), states.SUSPENDED)
        self.assertEqual(manager.get_state(manager2uuid), states.RUNNING)

    def test_long_running(self):
        time.sleep(4)
        manager.complete_task(manager1uuid, 'three', 'three')

    def test_results(self):
        time.sleep(5)
        self.assertEqual(manager.get_state(manager1uuid), states.SUSPENDED)
        self.assertEqual(manager.get_state(manager2uuid), states.SUCCESS)