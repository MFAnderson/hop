import docker
import unittest
import hop.providers.local_docker as local_docker
from hop.core import HopConfig

def delete_hop_containers(client):
    for container in client.containers.list(all=True):
        print('found container {}'.format(container.name))
        if container.name.startswith('hoptest'):
            print('deleting {}'.format(container.name))
            if (container.status == 'running'):
                container.kill()
            container.remove()


class TestLocalDockerProvider(unittest.TestCase):

    def setUp(self):
        self.client = docker.from_env()
        delete_hop_containers(self.client)

    def tearDown(self):
        delete_hop_containers(self.client)

    def test_provision_should_not_failed_if_you_run_it_twice(self):
        config = HopConfig({
            'provider': {
                'server': {
                    'name': 'hoptest-server'
                },
                'agents': {
                    'prefix': 'hoptest-agent',
                    'instances': 1
                }
            }
        })

        local_docker.provision(config)
        local_docker.provision(config)

        containers = self.client.containers.list(all=True)
        server = next(c for c in containers if c.name == 'hoptest-server')
        agent = next(c for c in containers if c.name == 'hoptest-agent-0')

        self.assertEquals(server.status, 'running')
        self.assertEquals(agent.status, 'running')


