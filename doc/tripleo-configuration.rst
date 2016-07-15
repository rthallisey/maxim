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
