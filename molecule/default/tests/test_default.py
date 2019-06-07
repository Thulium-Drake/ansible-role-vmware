import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_ad_user(host):
    users = [{'name': 'dom1usr', 'uid': 380801102, 'group': 'dom1_lnx_admins'},
             {'name': 'dom2usr', 'uid': 742801101, 'group': 'dom2_lnx_admins'}]
    for user in users:
        testuser = host.user(user['name'])

        # Test if the domain users/groups are present
        assert testuser.name == user['name']
        assert user['group'] in testuser.groups
        assert testuser.uid == user['uid']

        # Test if the user can run sudo
        with host.sudo():
            assert host.check_output('whoami') == 'root'
