======================================
TripleO overcloud upgrades and updates
======================================

Minor Update
============

If the operator wants to only update, set ``update_services`` in
``upgrade-vars.yml`` to yes::

  update_services: yes

Pacemaker managed services
==========================

By default, services will be managed by systemd.  In the future, this
will support things like Docker.

Pacemaker will be  managing services like cinder-volume, rabbitmq, maridb,
ect...  In ``upgrade-vars.yml``, there will be a minimal set of Pacemaker
managed services set as defaults. The operator has a choice as to which services
will be managed by Pacemaker since this can vary per release. For example,
Cinder Volumes by default is set to be managed by Pacemaker.

::

   # Be careful not to leave and empty list or Ansible will complain
   # Add/remove and services managed by Pacemaker
   pacemaker_managed_services:
     - cinder-volume

.. note:: (Soon to come) Ansible will detect what services are being managed by
Pacemaker in the overcloud by query Heat and it will check against the list
specified in ``pacemaker_managed_services`` to be sure it's correct.

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
