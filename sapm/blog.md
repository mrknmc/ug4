# Virtual Machines for development

During my internship at Skyscanner, I encountered what has been the most mysterious bug of my young career. A web scraper that worked fine on my local machine was raising a `cURL 35` error on production servers. The cURL documentation informed me this error is caused by a problem in the SSL/TLS handshake. A search of past bug cases revealed that this error has occurred several times before but since it could not be reproduced it was assumed that the third party is blocking our production IP range.

After more investigation I found that the cause of the error is a cipher mismatch between client and server. This led me to fix the bug but was not the root of the problem. The root of the problem was that our development environment was not an exact copy of the production environment. In production we used the OpenSSL library whereas our Windows machines used Mozilla's NSS library. These libraries use different cipher suites by default and that is why we could not replicate the problem in production. This error could have been avoided had we used a virtual development environment that replicates the production environment.

What is a virtual development environment, you may ask? In a nutshell, you develop your application in a virtual machine (VM) that runs the same OS and has the same dependencies installed as your production server. This way developers may, for example, use a Mac but develop all the code inside the OS that is used in production. Moreover, you could have different environments for different projects and run them all on the same machine.

Usually a virtualisation tool such as VirtualBox or VMware is used to run a VM. But how do you configure the VM to ensure that it is a replica of the production environment? Moreover, how do you ensure that changing or adding a dependency is replicated on machines of all developers? This is where a virtual development environment configuration tool comes in. The most popular such tool (and the one I have experience with) is Vagrant.

To configure a development environment with Vagrant you need to write a **Vagrantfile**. This file, written in a Ruby DSL, describes the configuration of your VM and how it should be provisioned. The two main ways to provision an environment are:

 - Using a shell script.
 - Using a configuration management software such as Chef, Puppet, or Ansible.

For simplicity's sake I will only consider the shell script.

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
apt-get update
apt-get install -y openjdk-7-jdk maven tmux git vim tree

# Install Leiningen
wget https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein
chmod a+x lein
mv lein /usr/bin
/usr/bin/lein

# Make etc directory
mkdir /etc/storm-mc
chown storm:storm /etc/storm-mc

# Make log directory
mkdir /var/log/storm-mc
chown storm:storm /var/log/storm-mc
```



<!-- example of how you would use it -->

<!-- what are the options? -->

