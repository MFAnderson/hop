def get_provisioner(provisioner_name):
    return getattr(__import__('hop.providers.{}'.format(provisioner_name)), provisioner_name)


class ProvisionCommand(object):
    def __init__(self, args, hop_config):
        self.args = args
        self.hop_config = hop_config

    def execute(self):
        try:
            provisioner = get_provisioner(self.hop_config['provider']['name'])
        except KeyError as exception:
            print("Error initializing provider. Make sure your configuration is correct")
            print(exception)
            exit(1)
        except ImportError as exception:
            print("Error initializing provider. Make sure your configuration is correct")
            print(exception)
            exit(1)


        print("{} - Provisioning gocd".format(self.args.command))
        provisioner.provision(self.hop_config)
