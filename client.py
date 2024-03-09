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


def receive_file(client_socket, initial_data, file_name):
    folder_name = "content-received"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, file_name)

    with open(file_path, 'wb') as file:
        if ":\n" in initial_data:
            server_info, file_content = initial_data.split(":\n", 1)
            print("Received :", server_info)
            file.write(file_content.encode())
        else:
            print(initial_data)  # Print error message or file not found message

        while True:
            file_data = client_socket.recv(1024)
            if not file_data:
                break
            file.write(file_data)

    print(f"File received and saved as: {file_path}")


def request_file(host, port, file_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(file_name.encode())
    initial_data = client_socket.recv(1024).decode()
    print(initial_data)

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

    request_file(host, port, 'example.txt')
