"""
server.py handles client requests for files by first checking if the 
file exists locally. If not, it forwards the request to other servers
defined in other_systems. If found on another server, it saves the file
locally and returns the content to the client.
"""
# server.py
import os
import socket

# Define the IP address and port of the other systems running the server.py script
other_systems = [
    ("172.31.8.60", 12345),
    ("172.31.6.92", 12345),
    ("172.31.2.235", 12345)
]


def save_file(file_name, file_content):
    with open(file_name, 'w') as file:
        file.write(file_content)


def handle_client_request(client_socket, file_name, server_info):
    folder_name = "/home/labuser/Desktop/content-provider/"
    file_path = os.path.join(folder_name, file_name)

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            file_content_with_info = f"File content from server {server_info}:\n{file_content}"
            client_socket.send(file_content_with_info.encode())
    except FileNotFoundError:
        print(
            f"Failed to retrieve file from current node")
        # Forward the file request to other systems if not found locally
        current_system_ip = socket.gethostbyname(socket.gethostname())
        for system_ip, system_port in other_systems:
            if system_ip != current_system_ip:  # Check if the IP address is not equal to the current server's IP address
                try:
                    print(
                        f"Trying to connect to another node: {system_ip}:{system_port}")
                    other_server_socket = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)
                    other_server_socket.connect((system_ip, system_port))
                    print(
                        f"Connection successfull to the node: {system_ip}:{system_port}")
                    other_server_socket.send(file_name.encode())
                    print(
                        f"Initiating search on the node: {system_ip}:{system_port}")
                    file_content = other_server_socket.recv(1024).decode()
                    file_content_with_info = f"File content received from server: {system_ip}:\n{system_port}"
                    client_socket.send(file_content_with_info.encode())
                    print(
                        f"File content received from the node: {system_ip}:{system_port}")
                    # Save the file received from other system locally
                    save_file(file_path, file_content)
                    print(
                        f"File saved locally: {file_path}")
                    other_server_socket.close()
                    return
                except Exception as e:
                    print(
                        f"Failed to retrieve file from the node: {system_ip}:{system_port}: {e}")

        client_socket.send("File not found.".encode())


# Example usage:
if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    port = 12345

    server_info = f"{host}:{port}"  # Server information for identification

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server listening on: ", host, port)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection successfull from node: ", client_address)

        file_name = client_socket.recv(1024).decode()
        handle_client_request(client_socket, file_name, server_info)

        client_socket.close()
