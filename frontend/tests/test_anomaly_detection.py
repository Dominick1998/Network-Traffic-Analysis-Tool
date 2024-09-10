import unittest
from backend.anomaly_detection import detect_anomalies

class AnomalyDetectionTests(unittest.TestCase):
    """
    A set of tests for the anomaly detection function.
    """

    def test_detect_anomalies(self):
        """
        Test that anomalies are correctly detected.
        """
        traffic_data = [
            {'length': 500},
            {'length': 600},
            {'length': 700},
            {'length': 1200},  # This should be considered an anomaly
            {'length': 1500}   # This should also be considered an anomaly
        ]

        anomalies = detect_anomalies(traffic_data)
        self.assertEqual(len(anomalies), 2)  # There should be 2 anomalies detected
        self.assertEqual(anomalies[0]['length'], 1200)
        self.assertEqual(anomalies[1]['length'], 1500)

if __name__ == '__main__':
    unittest.main()
