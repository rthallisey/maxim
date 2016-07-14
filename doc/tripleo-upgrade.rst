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
url to the release of choice.

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

Configuration for an Overcloud Update or Upgrade
================================================

The operator will use ``upgrade-vars.yml`` to drive the upgrade. Edit
this file to change what services will be included in the upgrade play by adding
or removing services from ``openstack_services``.

For additional configuration check out the `tripleo configuration`_ doc.

::

   openstack_services:
     - keystone
     - glance

Overcloud
=========

The operator can run a rolling upgrade or the traditional all-at-once
upgrade.  The rolling upgrade will perform the upgrade tasks one service
at a time on a percentage of the nodes.  The all-at-once approach will
use the same roles, but will handle all operations at one time.

Run a rolling upgrade on the services specified in ``openstack_services``::

   ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml rolling.yml

Run an all-at-once upgrade::

   ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml all-at-once.yml

.. _tripleo configuration: ./tripleo-configuration.rst
