from src.csvutils import export_to_csv
from unittest import mock, TestCase

mock_data_frame_count = 0
mock_data_frame_results = []
export_to_csv_params = []


def _mock_data_frame(*args, **kwargs):
    global mock_data_frame_count
    global mock_data_frame_results

    mock_csv = mock_data_frame_results[mock_data_frame_count]
    mock_data_frame_count += 1
    return mock_csv


class MockCsv:
    def to_csv(*args, **kwargs):
        global export_to_csv_params
        export_to_csv_params.append({'args': args, 'kwargs': kwargs})


class TestCsvUtils(TestCase):
    def setUp(self):
        global mock_data_frame_count
        mock_data_frame_count = 0
        global mock_data_frame_results
        mock_data_frame_results = []
        global export_to_csv_params
        export_to_csv_params = []

    @mock.patch('pandas.DataFrame', side_effect=_mock_data_frame)
    def test_export_to_csv(self, mock_data_frame):
        mock_csv = MockCsv()
        global mock_data_frame_results

        mock_data_frame_results = [mock_csv]
        export_to_csv({'User': ['joel'], 'Access Key Age': ['250']}, 'testfile.csv')
        mock_data_frame.assert_called_once_with({'User': ['joel'], 'Access Key Age': ['250']})
        self.assertEqual(export_to_csv_params, [{'args': (mock_csv, 'testfile.csv'), 'kwargs': {'encoding': 'utf-8', 'index': False}}])









