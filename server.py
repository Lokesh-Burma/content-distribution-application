"""
server.py handles client requests for files by first checking if the 
file exists locally. If not, it forwards the request to other servers
defined in other_systems. If found on another server, it saves the file
locally and returns the content to the client.
"""
# server.py
import os
import socket
import json

other_systems = [
    ("172.31.7.185", 12345),
    ("172.31.3.78", 12345),
    ("172.31.7.130", 12345)
]


def save_file(file_name, file_content):
    with open(file_name, 'w') as file:
        file.write(file_content)


def handle_client_request(client_socket, data, current_system_ip):
    folder_name = "/home/labuser/Desktop/content-provider"
    file_path = os.path.join(folder_name, data['file_name'])

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            client_socket.send(
                f"File content from server {current_system_ip}:\n{file_content}".encode())
            return  # Exit the function after sending the file content
    except FileNotFoundError:
        print(f"Failed to retrieve file from current node")

        data['file_not_found_in_ip'].append(current_system_ip)

        for ip, port in other_systems:
            if ip != current_system_ip and ip not in data['file_not_found_in_ip']:
                try:
                    print(f"Trying to connect to another node: {ip}:{port}")
                    other_socket = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM)
                    other_socket.connect((ip, port))
                    print(f"Connection successfull to the node: {ip}:{port}")
                    json_data = json.dumps(data)
                    other_socket.send(json_data.encode())
                    print(f"Initiating search on the node: {ip}:{port}")
                    response = other_socket.recv(1024).decode()
                    if ":\n" in response:
                        info, content = response.split(":\n", 1)
                        print("Received :", info)
                        client_socket.send(response.encode())
                        print(
                            f"File content received from the node: {ip}:{port}")
                        save_file(file_path, content)
                        print(f"File saved locally: {file_path}")
                        other_socket.close()
                        return
                    else:
                        print(
                            f"Failed to retrieve file from the node: {ip}:{port}")
                        data['file_not_found_in_ip'].append(ip)
                except Exception as e:
                    print(
                        f"Failed to retrieve file from the node: {ip}:{port}: {e}")
                    data['file_not_found_in_ip'].append(ip)

        client_socket.send("File not found.".encode())


if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server listening on: ", host, port)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection successfull from node: ", client_address)

        data = client_socket.recv(1024).decode()
        data = json.loads(data)
        print("Received :", data)
        handle_client_request(client_socket, data, host)

        client_socket.close()
