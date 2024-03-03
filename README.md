# content-distribution-application

This project implements a simple client-server file transfer system using Python sockets.

## Overview

The system allows a client to request a file from a server. The server will check if it has the file locally and send the contents back to the client if found. If not found, the server will attempt to retrieve the file from another configured system before sending it to the client.

The key components are:

- client.py - Sends file request and receives file content
- server.py - Handles file requests and sends back file contents
- content-provider.py - Contains helper functions for handling files

## Usage

To run the system:

1. Generate content provider files:

   ```
   python3 content-provider.py example.txt "sample text to save in the file"
   ```

2. Start the server:

   ```
   python3 server.py
   ```

3. In another terminal, run the client and specify a file name:

   ```
   python3 client.py example.txt
   ```

The client will request file.txt from the server. The server will attempt to find it and send the contents back.

## Configuration

The other_systems list in server.py contains the IP addresses and ports of other servers to try if a file is not found locally. This can be edited to chain multiple systems together.

## Contributing

Contributions to improve the code are welcome! Some ideas:

- Support larger file transfers
- Add authentication between client and server
- Expand configurability of systems

## License

This project is open source and available under the MIT License.

## Contact

Let me know if you have any questions or issues!
