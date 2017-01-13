"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later,but that will cause
  problems: the code will get executed twice:

  - When you run `python -m vault_uploader` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``vault_uploader.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``vault_uploader.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import click
import hvac
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


class VaultUploader(object):
    """
    Class for the vault uploader
    """

    def __init__(self, url, token, namespace, env):
        """
        Initialize the VaultUploader class

        Args:
            url: The address of the Vault server
            token: The auth token for Vault
            namespace: The application name
            env: The environment of the application

        Returns:
            The vault_uploader class object
        """
        self.namespace = namespace
        self.env = env
        self.client = hvac.Client(url=url, verify=False, token=token)

    def set(self, container, **kwargs):
        """
        Set the config values in the container

        Args:
            container: container name (ex. datastore)
            **kwargs: key/value pairs of config values

        Returns:

        """
        return self.client.write("{0}/{1}/{2}".format(self.namespace, self.env,
                                                      container), **kwargs)

    def upload(self, filename):
        """
        Parse a config ini file into vault

        Args:
            filename: file to parse

        Returns:

        """
        parser = ConfigParser()
        # parser optionxform=str retains case
        parser.optionxform = str
        parser.read(filename)
        config_dict = dict(parser._sections)
        for key in config_dict:
            config_dict[key] = dict(parser._defaults, **config_dict[key])
            config_dict[key].pop('__name__', None)
            self.set(key, **config_dict[key])


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--vault_server',
              prompt='Server Address',
              help='The Vault server address')
@click.option('--vault_namespace',
              prompt='Application Namespace',
              help='The application namespace in Vault')
@click.option('--vault_env',
              prompt='Application Environment',
              help='The application environment (pilot, prod, etc..)')
@click.option('--vault_token',
              prompt='Vault Token',
              help='Your Vault server token')
def main(filename, vault_server, vault_namespace, vault_env, vault_token):
    """
    Main entrypoint for program

    Args:
        filename: file to load into vault
        vault_server: vault server address
        vault_namespace: application name
        vault_env: application environment (prod, pilot, etc..)
        vault_token: api token for vault
    """
    client = VaultUploader(url=vault_server,
                           token=vault_token,
                           namespace=vault_namespace,
                           env=vault_env)
    client.upload(filename)
