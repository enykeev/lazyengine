===============================
Lazy Engine Test Suite
===============================

This is a test suite that describes the requirements to the new structural
element, Controller, Mistral team needs to be able to use TaskFlow as workflow
engine for the service.

    Lazy engine should be async and atomic, it should not have its own state, 
    instead it should rely on some kind of global state (db or in-memory, 
    depending on a type of application). It should have at least two methods: 
    run and task_complete. Run method should calculate the first batch of tasks 
    and schedule them for executing (either put them in queue or spawn the 
    threads). Task_complete should mark a certain task to be completed and then 
    schedule the next batch of tasks that became available due to resolution of 
    this one.

    The desired use of lazy engine in Mistral is illustrated `here 
    <http://tinyurl.com/qaeaf7a>`_

    It should supports long running tasks and survive engine process restart
    without loosing the state of the running actions. So it must be passive
    (lazy) and persistent.

    On Mistral side we are using Lazy engine by patching async.run directly to
    the API (or engine queue) and async.task_complete to the worker queue
    result channel (and the API for long running tasks). We are still sharing
    the same graph_analyzer, but instead of relying on loop and Futures, we are
    handling the execution ourselves in a scalable and robust way.

We've outlined the functionality of every method we need by using a fragments
of current TaskFlow engine implementation. What Mistral need is a drop-in
replacement for lazyengine.controller with the solid public API. We are pretty
sure that the same construct may be used as a base for current TaskFlow engine.

Since Tox is trying to run all the tests simultaneously by subprocessing every
test method, we've decided to synchronize them using time.sleep().

To make the Controller more transparent, we've also decided that persistence
level should operate outside of its scope. To make this test complete we would
also need to add ``get_flow_details`` to the backend connection to be able to
retrieve the execution object in another subprocess.

More info on that component can be found in:

- `TaskFlow Integration Summary etherpad
  <https://etherpad.openstack.org/p/taskflow-integration-summary>`_
- `Engine overview and proposal etherpad
  <https://etherpad.openstack.org/p/mistral-engine-overview-and-proposal>`_
- OpenStack mailing list discussions
    - `[openstack-dev] [Mistral] [Taskflow] [all] Mistral + taskflow
      <http://lists.openstack.org/pipermail/openstack-dev/2014-March/029979.html>`_
    - `[openstack-dev] [Mistral] [TaskFlow] Long running actions
      <http://lists.openstack.org/pipermail/openstack-dev/2014-March/030629.html>`_
    - `[openstack-dev] [Mistral] How Mistral handling long running delegate tasks
      <http://lists.openstack.org/pipermail/openstack-dev/2014-March/031236.html>`_
