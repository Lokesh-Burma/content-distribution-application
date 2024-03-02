# server.py
import os
import socket

# Define the IP address and port of the other systems running the server.py script
other_systems = [("192.168.1.101", 12346), ("192.168.1.102", 12347)]


def save_file(file_name, file_content):
    with open(file_name, 'w') as file:
        file.write(file_content)


def handle_client_request(client_socket, file_name, server_info):
    folder_name = "content-provider"
    file_path = os.path.join(folder_name, file_name)

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            file_content_with_info = f"File content from server {server_info}:\n{file_content}"
            client_socket.send(file_content_with_info.encode())
    except FileNotFoundError:
        # Forward the file request to other systems if not found locally
        for system_ip, system_port in other_systems:
            try:
                other_server_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                other_server_socket.connect((system_ip, system_port))
                other_server_socket.send(file_name.encode())
                file_content = other_server_socket.recv(1024).decode()
                file_content_with_info = f"File content from server {server_info}:\n{file_content}"
                client_socket.send(file_content_with_info.encode())
                # Save the file received from other system locally
                save_file(file_path, file_content)
                other_server_socket.close()
                return
            except Exception as e:
                print(
                    f"Failed to retrieve file from {system_ip}:{system_port}: {e}")

        client_socket.send("File not found.".encode())


# Example usage:
if __name__ == "__main__":
    host = 'localhost'
    port = 12345

    server_info = f"{host}:{port}"  # Server information for identification

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server listening on port", port)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection from", client_address)

        file_name = client_socket.recv(1024).decode()
        handle_client_request(client_socket, file_name, server_info)

        client_socket.close()
