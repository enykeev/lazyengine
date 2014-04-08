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

from lazyengine import controller
from lazyengine import example_utils
from lazyengine.tests import base

from taskflow.openstack.common import uuidutils
from taskflow.patterns import linear_flow as flow
from taskflow.persistence.logbook import FlowDetail as Execution
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
    # Assuming task won't finish when it returns None.
    # TODO(enykeev): Address this assumption in code
    pass


fl = flow.Flow('some').add(
    task.FunctorTask(one, provides='one'),
    task.FunctorTask(two, provides='two'),
    task.FunctorTask(three, provides='three')
)


class TestLazyEngine(base.TestCase):

    # I'm relying on Tox to run all the tests as a separate process at the same
    # time and I'm trying to set an order of execution using time.sleep, though
    # I'm not sure it would act the same way when there will be more than a few
    # tests.
    def test_start_manager1(self):
        execution = Execution(fl.name, manager1uuid)

        controller.start(fl, execution)

        self.assertEqual(controller.get_state(execution), states.RUNNING)

    def test_start_manager2(self):
        execution = Execution(fl.name, manager2uuid)

        controller.start(fl, execution)

        self.assertEqual(controller.get_state(execution), states.RUNNING)

    def test_stop_manager1(self):
        time.sleep(1.5)
        # Isn't it a bit complicated for such a simple task?
        with example_utils.get_backend() as backend:
            conn = backend.get_connection()
            # I don't really see a point of logbook and would prefer to be able
            # to get flow_details directly, though I'm interested to hear TF
            # team on the matter.
            execution = conn.get_flow_details(manager1uuid)

        controller.stop(execution)

        self.assertEqual(controller.get_state(execution), states.SUSPENDING)

    def test_intermediate_results(self):
        time.sleep(3)
        with example_utils.get_backend() as backend:
            conn = backend.get_connection()
            execution1 = conn.get_flow_details(manager1uuid)
            execution2 = conn.get_flow_details(manager2uuid)

        self.assertEqual(controller.get_state(execution1), states.SUSPENDED)
        self.assertEqual(controller.get_state(execution2), states.RUNNING)

    def test_long_running(self):
        time.sleep(4)
        with example_utils.get_backend() as backend:
            conn = backend.get_connection()
            execution = conn.get_flow_details(manager2uuid)

        self.assertEqual(controller.get_state(execution), states.RUNNING)

        # Instead of task name (second arg) we should probably send its id. We
        # need to figure out how to retrieve it for the sake of the test.
        controller.complete_task(execution, 'three', 'three')

        self.assertEqual(controller.get_state(execution), states.SUCCESS)

    def test_results(self):
        time.sleep(5)
        with example_utils.get_backend() as backend:
            conn = backend.get_connection()
            execution1 = conn.get_flow_details(manager1uuid)
            execution2 = conn.get_flow_details(manager2uuid)

        self.assertEqual(controller.get_state(execution1), states.SUSPENDED)
        self.assertEqual(controller.get_state(execution2), states.SUCCESS)
