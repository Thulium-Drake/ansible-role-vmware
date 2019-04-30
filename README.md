# Ansible toolkit for VMWare
This role provides multiple actions for use with VMWare clusters, it currently
features:

* Managing VM powerstates
* Managing VM snapshots
* Creating/editing VMs and templates (some restrictions may apply!)

For an example setup in which you can use this, please check
[vmware-example-setup](https://github.com/Thulium-Drake/ansible/tree/master/vmware-example-setup).

This module can delegate all required actions to a different machine which can
even be different for each targeted VM. Within this role this host is
referred to as the 'API host'

# Usage
This module requires the use of PyVmomi and the VMWare SDK, this role will
detect and attempt to install all the required dependencies itself.

For detailed instructions on how to install these dependencies manually, please
check the example setup.

## RedHat based API hosts need additional setup!
When running this role on a RedHat system, it will always try to install the
dependencies (and abort after finishing that). This is due to the fact RedHat
uses SCL for pip (which we need to get PyVMomi and the other modules), and that
needs to be sourced before running any python commands.

This has been implemented as follows:

* Run the role, it will install all required software
* The role will exit with an error
* Update the inventory with a line such as below
* Run the role again, it will work now

I have yet to find a more integrated/elegant solution for this problem.

NOTE: Please note that changing the Python interpreter might/will break other
ansible functionality!

A workaround for that might be to use a 'virtual name' in the inventory:

```
vmware-api-host.example.com ansible_host=rhel.example.com ansible_python_interpreter=/usr/local/bin/ansible_vmware_python
```

## Multiple vSphere clusters? No problem!
The playbook is configured to lookup the vSphere credentials and information
in the hostvars of the targeted VM.  So, configuring for multiple VMware
clusters is as easy as defining these credentials for that specific host/group,
just like any other variable.

When Ansible runs the playbook, it will lookup all of the required information
for that specific targeted VM.

# Powerstate
Supported states are:

 * Poweron a VM using either VMWare tools or the virtual power button
 * Poweroff a VM using either VMWare tools or the virtual power button
 * Reboot/reset a VM using either VMWare tools or the virtual power button

The role will NOT prompt for the required information, it can only be
provided using the playbook used to call it:

```
 - hosts: all
   gather_facts: no
   tasks:
   - import_role:
       name: vmware
     vars:
       target_action: "powerstate"
       target_group: "{{ ansible_limit }}"
       target_state: "powered-on"
     run_once: yes
```

## Required variables:

 * target_action: one of the vmware_ playbooks that came with this role
 * target_group: a comma-separated list of hostgroups that are targeted
 * target_action: one of the states in the supported_states list

# Snap
Supported actions are:

 * Create snapshots (automatically with a datestamp, or with a provided name)
 * Delete given or all snapshots
 * Revert to a given snapshot, this script will NOT give you a list to pick from.

The role will NOT prompt for the required information, it can only be
provided using the playbook used to call it:

```
 - hosts: all
   gather_facts: no
   tasks:
   - import_role:
       name: vmware
     vars:
       target_action: "snap"
       target_group: "{{ ansible_limit }}"
       target_state: "present"
       target_snapshot_name: ansible_snap_stuff
     run_once: yes
```

## Required variables:

 * target_action: one of the vmware_ playbooks that came with this role
 * target_group: a comma-separated list of hostgroups that are targeted
 * target_state: one of the actions in the supported_states list

## Optional variables:

 * target_snapshot_name:
   * When creating snapshots: override the name of the snapshot
   * When reverting/deleting snapshots: the target snapshot to delete

# Provision guest
Supported actions are:

* Creating a new VM based of a template or other VM
* Deleting a VM
* Creating a new template based of a VM

The role will NOT prompt for any information required, it can only
provided using the playbook used to call it. A default hardware profile is
available in the defaults directory.

To create a new VM, follow these steps:

* Create a vars file with the following information:
  * Datastore
  * VM folder
  * Template (make sure it exists)
  * Disk setup and disk controller type
  * Network setup
  * RAM and CPU setup
  * VM hardware version and BIOS type
* Add a new entry into the inventory
* Run the playbook, for example:

```
---
- hosts: new-host.example.com
  gather_facts: no
  tasks:
    - import_role:
        name: vmware
      vars:
        target_action: provision_guest
        target_group: "{{ ansible_play_hosts }}"
        target_state: present
        target_esxi_hostname: esxi.example.com
      run_once: yes
```
