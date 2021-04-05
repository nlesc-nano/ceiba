# What is this repository for?
This recipe installs and configures the **ceiba** app using [ansible](https://www.ansible.com/).

## Step to install the app
1. Install [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) in your computer.
2. Clone [this repo](https://github.com/nlesc-nano/ceiba)
3. Edit the [inventory](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html) file with the address of the server(s) where you want to install the runner.
4. Edit the [playbook](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html) file with the `remote_user` name for the hosts.
5. Make sure that you can ssh to your server(s).
6. Install the runner with the following command:
   ``ansible-playbook -i inventory playbook.yml``

## Note:
The script will ask you for the `Mongodb_password` for the app.

## Backup
To backup the data in the VM a [CEPH datablock](https://doc.hpccloud.surfsara.nl/create-datablocks)
must be created and then a [crontab job](https://crontab.guru/) must be run periodically to backup
the data into the disk. First,
add a new `cron` task:
```bash
sudo crontab -e  # sudo is required to copy the mongo_data folder
```

Then add the time and the task to execute the job

```bash
00 9 * * * rsync -a /root/mongo_data /data
```

The previous command will copy the `mongo_data` folder every day at 9AM to the `/data` folder.

Here we assume that `/home/ubuntu/mongo_data` is the docker volumen where the Mongodb containers stores
the database and `/data` is the directory where the external backup disk has been mounted.


### Supported OS
Currently the recipe only works for **Ubuntu** and **Debian**
