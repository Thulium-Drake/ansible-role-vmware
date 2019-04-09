# VMWare role
This role provides multiple actions for use with VMWare clusters, it currently
features:

* Managing VM powerstates
* Managing VM snapshots

The most documentation can be found in the comment block at the top of each
file. And for an example setup in which you can use this, please check
[vmware-example-setup](https://github.com/Thulium-Drake/ansible/vmware-example-setup).

This module can delegate all required actions to a different machine which can
even be different for each targeted VM. Within this role this host is
referred to as the 'API host'

# Usage
This module requires the use of PyVmomi and the VMWare SDK, please check the
example setup for detailed installation instructions.

This role will attempt to install all the required dependencies itself.

## RedHat based API hosts need additional setup!
When running this role on a RedHat system, it will always try to install the
dependencies (and abort after finishing that). This is due to the fact RedHat
uses SCL for pip (which we need to get PyVMomi and the other modules), and that
needs to be sourced before running any python commands.

This has been implemented as follows:

* Run the role, it will install all required software
* The role will exit with an error
* Copy the suggested inventory line from the error (hint: use stdout_callback = yaml)
* Update the inventory with the above line
* Run the role again, it will work now

I have yet to find a more integrated/elegant solution for this problem.

Please note that changing the Python interpreter might/will break other ansible functionality!

A workaround for that might be to use a 'virtual name' in the inventory:

```
vmware-api-host.example.com ansible_host=rhel.example.com
```

## Powerstate
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

### Required variables:

 * target_action: one of the vmware_ playbooks that came with this role
 * target_group: a comma-separated list of hostgroups that are targeted
 * target_action: one of the states in the supported_states list

## Snap
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

### Required variables:

 * target_action: one of the vmware_ playbooks that came with this role
 * target_group: a comma-separated list of hostgroups that are targeted
 * target_state: one of the actions in the supported_states list

### Optional variables:

 * target_snapshot_name:
   * When creating snapshots: override the name of the snapshot
   * When reverting/deleting snapshots: the target snapshot to delete

