"""
This module defines a certbot plugin to automate the process of completing a
``dns-01`` challenge (`~acme.challenges.DNS01`) by creating, and subsequently
removing, TXT records using the gransy (subreg) api https://subreg.cz/manual/.
"""

from lexicon.providers import gransy
import zope.interface

from certbot import interfaces
from certbot.plugins import dns_common
from certbot.plugins import dns_common_lexicon


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for gransy

    This Authenticator uses the gransy API to fulfill a dns-01 challenge.
    """

    description = ('Obtain certificates using a DNS TXT record (if you are '
                   'using gransy for DNS).')

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):
        super(Authenticator, cls).add_parser_arguments(add)
        add('credentials', help='gransy credentials INI file.')

    def more_info(self):
        return ('This plugin configures a DNS TXT record to respond to a '
                'dns-01 challenge using the gransy API.')

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'gransy credentials INI file',
            {
                'auth_username': 'Specify username for authentication',
                'auth_password': 'Specify password for authentication',
            }
        )

    def _perform(self, domain, validation_name, validation):
        self._get_gransy_client().add_txt_record(
            domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self._get_gransy_client().del_txt_record(
            domain, validation_name, validation)

    def _get_gransy_client(self):
        credentials = self.credentials.conf
        return _GransyLexiconClient(
            credentials('auth_username'),
            credentials('auth_password'))


class _GransyLexiconClient(dns_common_lexicon.LexiconClient):
    """Encapsulates all communication with gransy via Lexicon."""

    def __init__(self, auth_username, auth_password):
        super(_GransyLexiconClient, self).__init__()
        config = dns_common_lexicon.build_lexicon_config('gransy', {}, {
            'auth_username':   auth_username,
            'auth_password':  auth_password,
        })
        self.provider = gransy.Provider(config)

    # called while guessing domain name (going from most specific to tld):
    def _handle_general_error(self, e, domain_name):
        if 'Value in field domainname does not match requirements' in str(e):
            return None
        return super(_GransyLexiconClient, self)._handle_general_error(
            e, domain_name)
