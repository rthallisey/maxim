TripleO overcloud upgrades and updates
======================================

Generate the inventory file for your overcloud
----------------------------------------------

Generate the inventory file using the ``ansible/generate-inventory.yml``
playbook. This playbook can be run any number of times to update the inventory
of the overcloud.

::

   ansible-playbook -i 'undercloud,' -c local ansible/generate-inventory.yml

The inventory file will contain a list of the overcloud servers divided into
Ansible groups by their role defined by the operator.

::

   [undercloud]
   localhost  ansible_connection=local

   [controller]
   192.0.2.5
   192.0.2.6
   192.0.2.7

   [compute]
   192.0.2.8

   [controller:vars]
   ansible_ssh_user=heat-admin
   ansible_become=true
   ansible_become_user=root
   ansible_become_method=sudo

   [compute:vars]
   ansible_ssh_user=heat-admin
   ansible_become=true
   ansible_become_user=root
   ansible_become_method=sudo

Managing the Upgrade
--------------------

The operator will use ``ansible/upgrade_vars.yml`` to drive the upgrade. Edit
this file to change what services will be included in the upgrade play by adding
or removing services from ``tripleo_services``.

::

       tripleo_services:
         - keystone
         - glance

Running an Upgrade
------------------

The operator can run a rolling upgrade or the traditional all-at-once
upgrade.  The rolling upgrade will perform the upgrade tasks one service
at a time on a percentage of the services.  The all-at-once approach will
stop all services, update the packages, db_sync, and restart all the services.

Run a rolling upgrade on the services specified in ``tripleo_services``::

   ansible-playbook -i /etc/tripleo/upgrade_inventory -e @ansible/upgrade_vars.yml rolling.yml

Run an all-at-once upgrade::

   ansible-playbook -i /etc/tripleo/upgrade_inventory -e @ansible/upgrade_vars.yml all-at-once.yml

Running a Minor Update
----------------------

If the operator wants to update, set ``update_services`` in
``ansible/upgrade_vars.yml`` to yes and run either the ``rolling.yml`` or
the ``all-at-once.yml`` playbook from above.

::

  update_services: yes
