# client.py
import os
import socket


def receive_file(client_socket, file_name):
    folder_name = "content-received"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, file_name)

    with open(file_path, 'wb') as file:
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
    response = client_socket.recv(1024).decode()

    if response.startswith("File content"):
        receive_file(client_socket, file_name)
    else:
        print("Error:", response)

    client_socket.close()


# Example usage:
if __name__ == "__main__":
    host = 'localhost'
    port = 12345

    file_name = input("Enter the file name to search: ")

    request_file(host, port, file_name)
