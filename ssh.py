#!/usr/bin/python3

import paramiko
from scp import SCPClient

def create_ssh_client(server, username, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username=username, password=password, timeout=10)
    return client

def execute_commands_and_save_output(ssh_client, commands, remote_output_file):
    try:
        with ssh_client.open_sftp() as sftp:
            with sftp.file(remote_output_file, 'w') as remote_file:
                for command in commands:
                    stdin, stdout, stderr = ssh_client.exec_command(command)
                    output = stdout.read().decode('utf-8')
                    remote_file.write(f"Command: {command}\n")
                    remote_file.write(output)
                    remote_file.write("\n")
                    print(f"Executed: {command}")
    except Exception as e:
        print(f"Error: {e}")

def download_file(ssh_client, remote_file, local_file):
    with SCPClient(ssh_client.get_transport()) as scp:
        scp.get(remote_file, local_file)

if __name__ == "__main__":
    server = "000.00.00.00"
    username = "soot"
    password = "1"

    commands = [
        'dmidecode -t 0',
        'ls -l',
        'uname -a'
    ]
    
    remote_output_file = "/root/command_output.txt"
    local_output_file = "/root/command_output.txt"

    ssh_client = create_ssh_client(server, username, password)

    print("Executing commands on remote server and saving output to file...")
    execute_commands_and_save_output(ssh_client, commands, remote_output_file)
    print("Commands executed and output saved successfully.")

    print("Downloading output file from remote server to local machine...")
    download_file(ssh_client, remote_output_file, local_output_file)
    print("File downloaded successfully.")

    ssh_client.close()
