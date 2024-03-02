# content_provider.py
import os
import sys


def generate_text_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


def get_file_info(file_path):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    return file_name, file_size


def main():
    if len(sys.argv) != 3:
        print("Usage: python content_provider.py <file_name> <file_content>")
        return

    file_name = sys.argv[1]
    file_content = sys.argv[2]

    folder_name = "content-provider"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, file_name)

    generate_text_file(file_path, file_content)
    file_name, file_size = get_file_info(file_path)
    print(f"Generated file: {file_name}, Size: {file_size} bytes")


if __name__ == "__main__":
    main()
