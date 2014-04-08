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


def start(flow, execution=None):
    # if not execution:
    #     execution = p_utils.create_flow_detail(flow)
    #
    # ...
    #
    # compile() -> ensure_task()
    #
    #  ...
    #
    # schedule(get_next_nodes())
    #
    # ...
    #
    # return execution.uuid
    pass


def stop(execution):
    # execution.state = states.SUSPENDED
    pass


def get_state(execution):
    # return execution.state
    pass


def complete_task(execution, task, result):
    # complete_execution(self, task, result)
    # if running():
    #     schedule(get_next_nodes())
    pass
