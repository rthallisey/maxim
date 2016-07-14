======================================
TripleO overcloud upgrades and updates
======================================

Mixing all-at-once and Rolling
==============================

Either playbook can be run at any given point in an upgrade.  If an operator
wants to upgrade a controller all at one time and upgrade compute in a rolling
fashion, use each playbook for each role.

In the example mentioned above, to run a rolling compute upgrade, edit the
inventory file in ``/etc/tripleo/upgrade-inventory`` and comment out the
controller nodes.

::

   [controller]
   #192.0.2.5
   #192.0.2.6
   #192.0.2.7

Run the rolling upgrade for the compute role::

  ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml rolling.yml

Now do the same for the controller node.  Uncomment the controller nodes and
comment out the compute nodes in ``/etc/tripleo/upgrade-inventory`` and run
the all-at-once upgrade::

  ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml all-at-once.yml

Running an Individual Task
==========================

Every task in the playbook has a ``tag`` associated with it. Specifying a tag
when running a playbook is a way for an operator to run a single task.

All tags use the follow index::

  <service>_<what_manages_the_service>_<action>

  # Task to stop glance-api through systemd
  glance_api_systemd_stop

  # Task sync glance's database
  glance_db_sync

  # All glance pacemaker tasks
  glance_pacemaker_tasks

Once the operator knows the tag(s), an operator can run a playbook only running
tasks with the specified tags or skip any task with the specified tag::

   # Stop, db_sync, and start Glance API
   ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml all-at-once.yml --tags "glance_db_sync,glance_api_systemd_stop,glance_api_systemd_start"

   # Skip all pacemaker tasks for Cinder
   ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml all-at-once.yml --skip-tags "cinder_pacemaker_tasks"
