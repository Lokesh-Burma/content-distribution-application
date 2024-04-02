import unittest
from client import request_file, receive_file


class TestClient(unittest.TestCase):

    def test_request_file_valid(self):
        # Test with valid host, port, and file name
        host = 'localhost'
        port = 12345
        file_name = 'test.txt'

        # Mock socket and response
        import socket
        socket.socket = unittest.mock.Mock()
        socket.socket().recv.return_value = b'File content'

        request_file(host, port, file_name)

        # Validate socket connection and file request
        socket.socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
        socket.socket().connect.assert_called_with((host, port))
        socket.socket().send.assert_called_with(file_name.encode())

    def test_request_file_error(self):
        # Test with invalid file name
        host = 'localhost'
        port = 12345
        file_name = 'invalid.txt'

        # Mock error response
        import socket
        socket.socket = unittest.mock.Mock()
        socket.socket().recv.return_value = b'Error: File not found'

        request_file(host, port, file_name)

        # Validate error handling
        socket.socket().send.assert_called_with(file_name.encode())
        self.assertRaises(Exception, request_file, host, port, file_name)

    def test_receive_file(self):
        # Test receiving valid file
        import os
        from unittest.mock import mock_open, patch

        file_name = 'test.txt'
        client_socket = unittest.mock.Mock()

        # Mock file data
        client_socket.recv.side_effect = [b'abc', b'def', b'']

        with patch('builtins.open', mock_open()) as mock_file:
            receive_file(client_socket, file_name)

            # Validate file handling
            handle = mock_file()
            self.assertEqual(handle.write.call_count, 2)
            handle.write.assert_has_calls([
                unittest.mock.call(b'abc'),
                unittest.mock.call(b'def')
            ])
            os.path.join.assert_called_with('content-received', file_name)


if __name__ == '__main__':
    unittest.main()
