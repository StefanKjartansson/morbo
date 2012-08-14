_, name = File.split File.expand_path File.dirname __FILE__

Vagrant::Config.run do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.network :hostonly, "33.33.33.10"
  config.vm.forward_port 8000, 8000
  if RUBY_PLATFORM =~ /mswin(32|64)/
    config.vm.share_folder("v-root", "/home/vagrant/apps/" + name, 
        ".")
  else
    config.vm.share_folder("v-root", "/home/vagrant/apps/" + name, 
        ".", :nfs => true)
  end
end
