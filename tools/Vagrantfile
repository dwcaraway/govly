# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Add a little extra memory so that grunt/node doesn't hang during concurrent tasks
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024 
  end

  # Every Vagrant virtual environment requires a box to build off of
  # Ubuntu 14.04 minimal box
  config.vm.box = "Official Ubuntu Daily Cloud Image amd64"
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.

  # Enable Berkshelf for Chef. Make sure the plugin is installed!
  # $ vagrant plugin install vagrant-berkshelf --plugin-version '>= 2.0.1'
  config.berkshelf.enabled = true


   config.vm.provision "shell",
	path: "chef-install.sh"
   config.vm.provision :chef_solo do |chef|
     chef.log_level = :debug
     chef.verbose_logging = true
  end
end
