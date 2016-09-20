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
started testing a `tripleo upgrade`_.

Missing Pieces (Tripleo)
========================

The upgrade and update for Tripleo require some additional pieces that aren't
implemented yet.

- :strike: `Inventory generation module`
- :strike: `Playbooks for all the services`
- :strike: `Consumable environment file`
- :strike: `Support for pacemaker and systemd`
- :strike: `Rolling upgrade/update playbook`
- :strike: `All at once upgrade/update playbook`
- :strike: `Tags for individual upgrade/update tasks`
- :strike: `Database playbook`
- :strike: `Repo setup module`
- Render Puppet Heira data from the undercloud and use Ansible Puppet Apply to
  generate the new config files for services.
- Multiple release playbook support. HA lite arch will require additional
  flexibility to move services from pacemaker to systemd upon upgrading.
- Upgrade/update gating in tripleo based on Maxim.

.. _tripleo upgrade: ./doc/tripleo-upgrade.rst
