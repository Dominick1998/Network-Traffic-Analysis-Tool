import unittest
from backend.network_summary import generate_network_summary

class NetworkSummaryTests(unittest.TestCase):
    """
    A set of tests for the network summary generation function.
    """

    def test_generate_network_summary(self):
        """
        Test that the network summary is generated correctly.
        """
        traffic_data = [
            {'source': '192.168.1.1', 'destination': '192.168.1.4', 'length': 500},
            {'source': '192.168.1.1', 'destination': '192.168.1.4', 'length': 600},
            {'source': '192.168.1.2', 'destination': '192.168.1.5', 'length': 700},
            {'source': '192.168.1.3', 'destination': '192.168.1.6', 'length': 800},
        ]

        summary = generate_network_summary(traffic_data)
        self.assertEqual(summary['total_packets'], 4)
        self.assertEqual(round(summary['average_length'], 2), 650.00)
        self.assertEqual(summary['top_sources'][0], ('192.168.1.1', 2))
        self.assertEqual(summary['top_destinations'][0], ('192.168.1.4', 2))

if __name__ == '__main__':
    unittest.main()
