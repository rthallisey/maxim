======================================
TripleO overcloud upgrades and updates
======================================

General Information
===================

The playbooks are designed to be as flexible as possible so that an operator
has the ability to run any single task in a play, a group of tasks, or a group
of tasks for a group of services.

The playbooks can be run for both the Undercloud and the Overcloud and across
multiple releases.

Generate the inventory file for your overcloud
==============================================

Generate the inventory file using the ``generate-inventory.yml``
playbook. This playbook can be run any number of times to update the inventory
of the overcloud.

::

   ansible-playbook -i inventory/undercloud-inventory generate-inventory.yml

The inventory file will be placed in ``/etc/tripleo/upgrade-inventory`` and will
contain a map of the currently deployed overcloud where each server's
address/hostname is added to the Ansible group associated with their defined
role.

::

   [undercloud]
   localhost  ansible_connection=local

   [controller]
   192.0.2.5
   192.0.2.6
   192.0.2.7

   [compute]
   192.0.2.8

Repo Update
===========

In order to get new packages, the operator needs to update repos on all
nodes.  Look in ``upgrade-vars.yml`` for ``delorean_repo_url`` and change the
url to a release of choice.

::

   delorean_repo_url: http://buildlogs.centos.org/centos/7/cloud/x86_64/rdo-trunk-master/delorean.repo

Update the repos on all nodes::

   ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml repo-setup.yml

Undercloud
==========

The undercloud upgrade will follow the same process as the overcloud upgrade,
but with a different inventory file. This inventory file is provided in
``inventory/undercloud-inventory``. Upgrade the undercloud with the following::

  ansible-playbook -i inventory/undercloud-inventory -e @upgrade-vars.yml rolling.yml

Setup for an Overcloud Update or Upgrade
========================================

The operator will use ``upgrade-vars.yml`` to drive the upgrade. Edit
this file to change what services will be included in the upgrade play by adding
or removing services from ``openstack_services``.

::

   openstack_services:
     - keystone
     - glance

Minor Update
------------

If the operator wants to update, set ``update_services`` in
``upgrade-vars.yml`` to yes::

  update_services: yes

Choose Pacemaker managed services
---------------------------------

By default, services will be managed by systemd.  In the future, this
will support things like Docker.

Pacemaker will be  managing services like cinder-volume, rabbitmq, maridb,
ect...  In ``upgrade-vars.yml``, there will be a minimal set of Pacemaker
managed services set as defaults. The operator has a choice as to which services
will be upgraded with Pacemaker since this can vary per release. For example,
Cinder Volumes by default is set to be upgraded with Pacemaker.

::

   # Be careful not to leave and empty list or Ansible will complain
   # Add/remove and services managed by Pacemaker
   pacemaker_managed_services:
     - cinder-volume

.. note:: (Soon to come) Ansible will detect what services are being managed by
Pacemaker in the overcloud by query Heat and it will check against the list
specified in ``pacemaker_managed_services`` to be sure it's correct.

Running an Upgrade
==================

The operator can run a rolling upgrade or the traditional all-at-once
upgrade.  The rolling upgrade will perform the upgrade tasks one service
at a time on a percentage of the services.  The all-at-once approach will
stop all services, update the packages, db_sync, and restart all the services.

Run a rolling upgrade on the services specified in ``openstack_services``::

   ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml rolling.yml

Run an all-at-once upgrade::

   ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml all-at-once.yml

Running an Individual Task
==========================

Every task in the playbook has a ``tag`` associated with it. Specifying a tag
when running a playbook is a way for an operator to run a single task.

All tags use the follow index::

  <service>_<who_manages_the_service>_<action>

  # Task to stop glance-api through systemd
  glance_api_systemd_stop

  # Task sync glance's database
  glance_db_sync

  # All glance pacemaker tasks
  glance_pacemaker_tasks

Once the operator knows the tag(s), an operator can run a playbook only running
tasks with the specified tags or skip any task with the specified tag::

   # Stop, db_sync, and start the Glance API
   ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml all-at-once.yml --tags "glance_db_sync,glance_api_systemd_stop,glance_api_systemd_start"

   # Skip all pacemaker tasks for Cinder
   ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml all-at-once.yml --skip-tags "cinder_pacemaker_tasks"
