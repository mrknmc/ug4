# Virtual Machines for development

## Most Mysterious Bug

During my internship at Skyscanner, I encountered what has been the most mysterious bug of my young career. A web scraper that worked fine on my local machine was raising a `cURL 35` error on production servers. The cURL documentation informed me this error is caused by a problem in the SSL/TLS handshake. A search of past bug cases revealed that this error has occurred several times before but since it could not be reproduced it was assumed that the third party is blocking our production IP range.

After more investigation I found that the cause of the error is a cipher mismatch between the client and the server. This led me to fix the bug but not the root of the problem. The root of the problem was that our development environment was not an exact copy of the production environment. We used the OpenSSL library in production whereas our development Windows machines used Mozilla's NSS library. These libraries use different cipher suites by default which is why we could not replicate the bug. This error could have been avoided had we used a virtual development environment that replicates the production environment.

## Virtual Development Environments to the Rescue

What is a virtual development environment, you may ask? In a nutshell, you develop your application in a virtual machine (VM) that runs the same operating system (OS) and has the same dependencies installed as your production server. This way you may, for example, use a Mac but develop code inside a Linux OS that is used in production. Moreover, even if you have different production environments for different projects you can run their virtual copies on one machine.

Usually a virtualisation tool such as VirtualBox or VMware is used to run a VM. But how do you configure the VM to ensure that it is an exact replica of the production environment? Moreover, how do you ensure that changing or adding a dependency is replicated on machines of all developers? This is where a virtual development environment configuration tool comes in.

The most popular such tool (and the one I have experience with) is Vagrant. Vagrant is essentially a wrapper around a provider such as VirtualBox, VMware, and recently even Docker. Vagrant allows you to configure and log in to your VM by running two simple commands: `vagrant up` and `vagrant ssh`. 

## Get Started Using Vagrant

To specify the configuration you need to create a file called **Vagrantfile**. This file, written in a Ruby DSL, describes the configuration of your VM and how it should be provisioned. The two main ways to provision an environment are:

 - Using a shell script.
 - Using a configuration management software such as Chef, Puppet, or Ansible.

```
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.hostmanager.manage_host = true
  config.hostmanager.enabled = true
  config.vm.synced_folder "~/storm-mc", "/opt/storm-mc"

  config.vm.define "storm" do |storm|
    storm.vm.box = "hashicorp/precise64"
    storm.vm.provision "shell", path: "bootstrap.sh"
  end
end
```

Above is a short excerpt from the Vagrantfile I use for my honours project. As you can see on line **whatever**, I   synchronise the project directory `storm-mc` from the host machine onto the VM. Lines **x to y** say that the VM uses a 64-bit version of Ubuntu 12.04.5 (Precise Pangoline) and I use a script called `bootstrap.sh` to provision the VM.

```
# Make sure necessities are there
apt-get install -y openjdk-7-jdk maven

# Install Leiningen
wget https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein
chmod a+x lein
mv lein /usr/bin
/usr/bin/lein

# Create `storm` user
groupadd storm
useradd --gid storm --home-dir /home/storm --create-home --shell /bin/bash storm
chown -R storm:storm /opt/storm-mc
ln -s /opt/storm-mc/bin/storm-mc /usr/bin/storm-mc

# Make etc and log directory
mkdir /etc/storm-mc
mkdir /var/log/storm-mc
```

Again, above is a short excerpt from the shell script I use to provision the VM for my honours project. This script ensures that project dependencies are installed (the ones available in the package manager as well as the ones built from source), a user called storm is created with the correct permissions, and directories used by the project are created.

Provisioning using a shell script is common for only small projects. More commonly, companies use a configuration management tool. Following is the bootstrap script re-written in the Puppet DSL:

```
package { "openjdk-7-jdk":
  ensure  => present,
}

package { "maven":
  ensure  => present,
}

exec{'retrieve_leiningen':
  command => "wget https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein -O /usr/bin/lein",
  creates => "/usr/bin/lein",
}

exec { 'chown_leiningen':
  command => 'chmod a+x /usr/bin/lein',
  path => '/bin',
  user => 'root'
}

group { 'storm_group':
  name => 'storm',
}

user { 'storm_user':
  name => 'storm',
}
...
```
