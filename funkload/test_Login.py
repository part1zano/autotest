# -*- coding: iso-8859-15 -*-
"""login FunkLoad test

$Id: $
"""
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload
from funkload.utils import Data
#from funkload.utils import xmlrpc_get_credential

class Login(FunkLoadTestCase):
    """XXX

    This test use a configuration file Login.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')
        # XXX here you can setup the credential access like this
        # credential_host = self.conf_get('credential', 'host')
        # credential_port = self.conf_getInt('credential', 'port')
        # self.login, self.password = xmlrpc_get_credential(credential_host,
        #                                                   credential_port,
        # XXX replace with a valid group
        #                                                   'members')

    def test_login(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------

        # /tmp/tmphSI7dB_funkload/watch0002.request
        # /tmp/tmphSI7dB_funkload/watch0003.request
        # /tmp/tmphSI7dB_funkload/watch0004.request
        self.get(server_url + "/dmedia/css/base.css?v=3",
            description="Get /dmedia/css/base.css")
        # /tmp/tmphSI7dB_funkload/watch0005.request
        self.get(server_url + "/dmedia/js/base.js?v=3",
            description="Get /dmedia/js/base.js")
        # /tmp/tmphSI7dB_funkload/watch0007.request
        # /tmp/tmphSI7dB_funkload/watch0008.request
        # /tmp/tmphSI7dB_funkload/watch0009.request
        # /tmp/tmphSI7dB_funkload/watch0010.request
        # /tmp/tmphSI7dB_funkload/watch0011.request
        # /tmp/tmphSI7dB_funkload/watch0013.request
        # /tmp/tmphSI7dB_funkload/watch0017.request
        self.get(server_url + "/dmedia/css/base.css?v=10003",
            description="Get /dmedia/css/base.css")
        # /tmp/tmphSI7dB_funkload/watch0018.request
        self.get(server_url + "/dmedia/js/base.js?v=10003",
            description="Get /dmedia/js/base.js")
        # /tmp/tmphSI7dB_funkload/watch0019.request
        # /tmp/tmphSI7dB_funkload/watch0021.request
        # /tmp/tmphSI7dB_funkload/watch0022.request
        # /tmp/tmphSI7dB_funkload/watch0023.request
        # /tmp/tmphSI7dB_funkload/watch0024.request
        # /tmp/tmphSI7dB_funkload/watch0025.request
        # /tmp/tmphSI7dB_funkload/watch0053.request
        # /tmp/tmphSI7dB_funkload/watch0054.request
        # /tmp/tmphSI7dB_funkload/watch0064.request
        # /tmp/tmphSI7dB_funkload/watch0065.request
        # /tmp/tmphSI7dB_funkload/watch0066.request
        # /tmp/tmphSI7dB_funkload/watch0067.request
        # /tmp/tmphSI7dB_funkload/watch0068.request
        # /tmp/tmphSI7dB_funkload/watch0070.request
        # /tmp/tmphSI7dB_funkload/watch0071.request
        # /tmp/tmphSI7dB_funkload/watch0077.request
        self.get(server_url + "/2A82/contractors/",
            description="Get /2A82/contractors/")
        # /tmp/tmphSI7dB_funkload/watch0078.request
        self.get(server_url + "/dmedia/css/base.css?v=10003",
            description="Get /dmedia/css/base.css")
        # /tmp/tmphSI7dB_funkload/watch0079.request
        self.get(server_url + "/dmedia/js/base.js?v=10003",
            description="Get /dmedia/js/base.js")
        # /tmp/tmphSI7dB_funkload/watch0086.request
        # /tmp/tmphSI7dB_funkload/watch0093.request
        # /tmp/tmphSI7dB_funkload/watch0094.request
        # /tmp/tmphSI7dB_funkload/watch0095.request
        # /tmp/tmphSI7dB_funkload/watch0096.request
        # /tmp/tmphSI7dB_funkload/watch0101.request
        # /tmp/tmphSI7dB_funkload/watch0103.request
        # /tmp/tmphSI7dB_funkload/watch0107.request
        self.get(server_url + "/search/?q=",
            description="Get /search/")
        # /tmp/tmphSI7dB_funkload/watch0108.request
        self.get(server_url + "/dmedia/css/base.css?v=10003",
            description="Get /dmedia/css/base.css")
        # /tmp/tmphSI7dB_funkload/watch0109.request
        self.get(server_url + "/dmedia/js/base.js?v=10003",
            description="Get /dmedia/js/base.js")
        # /tmp/tmphSI7dB_funkload/watch0112.request
        # /tmp/tmphSI7dB_funkload/watch0117.request
        # /tmp/tmphSI7dB_funkload/watch0118.request
        # /tmp/tmphSI7dB_funkload/watch0119.request
        # /tmp/tmphSI7dB_funkload/watch0120.request
        # /tmp/tmphSI7dB_funkload/watch0133.request
        self.get(server_url + "/logout/",
            description="Get /logout/")
        # /tmp/tmphSI7dB_funkload/watch0135.request
        self.get(server_url + "/dmedia/css/base.css?v=3",
            description="Get /dmedia/css/base.css")
        # /tmp/tmphSI7dB_funkload/watch0136.request
        self.get(server_url + "/dmedia/js/base.js?v=3",
            description="Get /dmedia/js/base.js")

        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")



if __name__ in ('main', '__main__'):
    unittest.main()
