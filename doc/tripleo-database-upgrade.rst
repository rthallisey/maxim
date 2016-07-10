=========================
TripleO database upgrades
=========================

General Information
===================

This document is meant to describe the database upgrade workflow in order to
make sure the operator understands what steps being taken and whether or not
they are appropriate for the operators current cloud.

Workflow
========

The database upgrade workflow involves a series of steps that will preseve the
state of the database while upgrading the service and the services that depend
on it.

Backup
------

First, the database will be backed up to the directory denoted by the
``database_backup_dir`` variable. This is defaulted to
``/var/tmp/mysql_upgrade_osp``.

Ansible expects there to be no current directory in place or it will fail
because of the possibility of a backup already being completed. If the operator
did the backup by hand, run the upgrade with ``--skip tags "database_backup"``
to avoid this error.

To backup your database for an active cloud do either of the following::

   ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml all-at-once.yml --tags "database_backup"
   or
   ansible-playbook -i /etc/tripleo/upgrade-inventory -e @upgrade-vars.yml rolling.yml --tags "database_backup"

Stop MariaDB
------------

After the backup is complete, the MariaDB service will be stopped. It will
always be the last service stopped no matter the ordering of services in
``openstack-services``.

Moving /var/lib/mysql and Updating the Package
----------------------------------------------

For additional safely, the directory ``/var/lib/mysql`` will be saved to
``database_back_dir``.  Then, the MariaDB packages will be updated.
