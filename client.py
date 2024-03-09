"""
client.py - Client for requesting and receiving files from a server

This module contains functions for connecting to a server, requesting a file
by name, receiving the file contents over a socket, and saving the file locally.

request_file() handles connecting to the server, sending the request, and calling
receive_file() to save the file after validating the response.

receive_file() handles receiving the file contents over the socket in chunks
and writing them to a local file.
"""

# client.py
import os
import socket
import json


def receive_file(client_socket, initial_data, file_name):
    if not os.path.exists("content-received"):
        os.makedirs("content-received")

    file_path = os.path.join("content-received", file_name)

    with open(file_path, 'wb') as file:
        if ":\n" in initial_data:
            server_info, file_content = initial_data.split(":\n", 1)
            print("Received :", server_info)
            file.write(file_content.encode())
        else:
            print(initial_data)

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)

    print(f"File received and saved as: {file_path}")


def request_file(host, port, file_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    payload = {
        "file_name": file_name,
        "file_not_found_in_ip": []
    }
    payload = json.dumps(payload)
    client_socket.send(payload.encode())
    initial_data = client_socket.recv(1024).decode()

    if initial_data.startswith("File content"):
        receive_file(client_socket, initial_data, file_name)
    else:
        print("Error:", initial_data)

    client_socket.close()


# Example usage:
if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    port = 12345

    file_name = input("Enter the file name to search: ")
    print(f"Initiating search on the current node: {host}:{port}")
    request_file(host, port, file_name)
