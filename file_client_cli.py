import socket
import json
import base64
import logging

server_address = ('localhost', 6666)


def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message {command_str[:10]}")
        sock.sendall(command_str.encode())
        data_received = ""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False


def remote_list():
    command_str = f"LIST"
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Failed")
        return False


def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile, 'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Failed")
        return False


def remote_upload(filename=""):
    try:
        fp = open(f"{filename}", 'rb')
        filecontent = base64.b64encode(fp.read()).decode()
        command_str = f"UPLOAD {filename} {filecontent}"
        hasil = send_command(command_str)
        if hasil['status'] == 'OK':
            print(hasil['data'])
            return True
        else:
            print("Failed")
            print(hasil['data'])
            print(hasil['err'])
            return False
    except FileNotFoundError:
        print(f"File {filename} is not found")
        return False


def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print(hasil['data'])
        return True
    else:
        print("Failed")
        print(hasil['data'])
        print(hasil['err'])
        return False


if __name__ == '__main__':
    server_address = ('172.16.16.101', 6666)

    remote_list()
    remote_get('donalbebek.jpg')

    remote_list()
    remote_upload('shinchan.jpg')
    remote_upload('shinchan-hapus.jpg')
    remote_upload('teks.txt')
    remote_upload('teks-hapus.txt')  

    remote_list() 
    remote_delete('shinchan-hapus.jpg')
    remote_delete('teks-hapus.txt')

    remote_list()