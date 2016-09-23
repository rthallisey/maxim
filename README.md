===================================================
Maxim - Ansible orchestrated upgrades for OpenStack
===================================================

Overview
========
Provide Ansible playbooks for upgrading OpenStack clouds managed by
a deployment tool. The goal is to break down upgrades to their simplest
form so that projects can share upgrade tasks.

Getting Started
===============

Maxim's first upgrade playbook targets tripleo.  Here are the docs to get
started testing a [tripleo upgrade](./doc/tripleo-upgrade.rst)

Missing Pieces (Tripleo)
========================

The upgrade and update for Tripleo require some additional pieces that aren't
implemented yet.

- ~~Inventory generation module~~
- Merge Inventory patch in THT: https://review.openstack.org/#/c/327822/
- ~~Playbooks for all the services~~
- ~~Consumable environment file~~
- ~~Support for pacemaker and systemd~~
- ~~Rolling upgrade/update playbook~~
- ~~All at once upgrade/update playbook~~
- ~~Tags for individual upgrade/update tasks~~
- ~~Database playbook~~
- ~~Repo setup module~~
- Render Puppet Heira data from the undercloud and use Ansible Puppet Apply to
  generate the new config files for services.
- Multiple release playbook support. HA lite arch will require additional
  flexibility to move services from pacemaker to systemd upon upgrading.
- Upgrade/update gating in tripleo based on Maxim.
