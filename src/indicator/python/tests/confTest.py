import sys
sys.path.append('..')
import unittest
import conf


class TestConfig(unittest.TestCase):

    def testDataReading(self):
        c = conf.Conf('salseeg')
        self.assertIsNotNone(c)

    def testStoring(self):
        c1 = conf.Conf('salseeg')
        servers = c1.servers
        interval = c1.refreshInterval
        c1.write()

        c2 = conf.Conf('salseeg')
        self.assertEqual(interval, c2.refreshInterval)
        self.assertEqual(servers, c2.servers)


if __name__ == '__main__':
    unittest.main()
