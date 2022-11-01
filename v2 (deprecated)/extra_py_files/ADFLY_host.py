import sys
sys.path.append('../common_py_files')
BUFFER_SIZE  = 1024 * 100

while True:
    try:
        from cryptography.fernet import Fernet
        import sqlite3
        from PIL import Image
        from turbo_flask import Turbo
        from psutil import virtual_memory
        from psutil import cpu_percent as cpu
        from flask import Flask, render_template, request, redirect, send_from_directory
        from werkzeug.security import check_password_hash
        break
    except Exception as e:
        print(repr(e))
        import pip
        pip.main(['install', 'pillow'])
        pip.main(['install', 'pyautogui'])
        pip.main(['install', 'psutil'])
        pip.main(['install', 'requests'])
        pip.main(['install', 'flask'])
        pip.main(['install', 'pyngrok'])
        pip.main(['install', 'cryptography'])
        pip.main(['install', 'turbo_flask'])
        pip.main(['install','werkzeug'])
        del pip

from os import system as system_caller, getcwd
from os import path
import socket
from random import choice, randrange
from threading import Thread
from time import ctime, sleep, time

server_start_time = time()

my_u_name = 'bhaskar'

parent, _ = path.split(path.split(getcwd())[0])
read_only_location = path.join(parent, 'read only')

parent, _ = path.split(getcwd())
images_location = path.join(parent, 'req_imgs/Windows')

parent, _ = path.split(getcwd())
common_py_files_location = path.join(parent, 'common_py_files')

OLD_USER_CONNECTION_PORT = 59999
HOST_MAIN_WEB_PORT_LIST = list(range(60000, 60000+1))
USER_CONNECTION_PORT_LIST = list(range(59995, 59998+1))

last_one_click_start_data = last_vm_activity = debug_data = ''
old_current_vm_data = []
vm_data_update_connections = last_vm_data = last_host_data = {}

db_connection = sqlite3.connect(f'{read_only_location}/user_data.db', check_same_thread=False)
paragraph_lines = open(f'{read_only_location}/paragraph.txt', 'rb').read().decode().split('.')


def __old_send_to_connection(connection, data_bytes: bytes):
    data_byte_length = len(data_bytes)
    connection.send(str(data_byte_length).encode())
    if connection.recv(1) == b'-':
        connection.send(data_bytes)
    if connection.recv(1) == b'-':
        return


def __old_receive_from_connection(connection):
    length = int(connection.recv(BUFFER_SIZE))
    connection.send(b'-')
    data_bytes = b''
    while len(data_bytes) != length:
        data_bytes += connection.recv(BUFFER_SIZE)
    connection.send(b'-')
    return data_bytes



def __send_to_connection(connection, data_bytes: bytes):
    data_byte_length = len(data_bytes)
    connection.send(f'{data_byte_length}'.zfill(8).encode())
    connection.send(data_bytes)



def __receive_from_connection(connection):
    data_bytes = b''
    length = b''
    for _ in range(10):
        if len(length) != 8:
            length += connection.recv(8 - len(length))
            sleep(0.1)
        else:
            break
    else:
        return b''
    if len(length) == 8:
        length = int(length)
        while len(data_bytes) != length:
            data_bytes += connection.recv(length - len(data_bytes))
        return data_bytes
    else:
        return b''

    
def __try_closing_connection(connection):
    for _ in range(10):
        sleep(0.1)
        try:
            connection.close()
        except :
            pass

        
def debug_host(text: str):
    if 'Connection' in text:
        return
    print(text)
    with open('debugging/host.txt', 'a') as file:
        file.write(f'[{ctime()}] : {text}\n')


def generate_random_string(_min, _max):
    string = ''
    for _ in range(randrange(_min, _max)):
        string += chr(randrange(97, 122))
    return string


        
python_files = {}
windows_img_files = {}
text_files = {}


def old_accept_connections_from_users():
    global python_files, windows_img_files, text_files
    """
         0:'main_file_check',
         5:'client_uname_check'
         8: user_login_update_check
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', OLD_USER_CONNECTION_PORT))
    sock.listen()

    def acceptor():
        connection, address = sock.accept()
        Thread(target=acceptor).start()
        request_code = 'nothing'
        try:
            request_code = __old_receive_from_connection(connection).strip().decode()
        except:
            pass
        if not request_code:
            return
        try:
            if request_code == '0':
                if ('final_main.py' not in python_files) or (path.getmtime('extra_py_files/final_main.py') != python_files['final_main.py']['version']):
                    python_files['final_main.py'] = {'version': path.getmtime('extra_py_files/final_main.py'), 'file': open('extra_py_files/final_main.py', 'rb').read()}
                __old_send_to_connection(connection, python_files['final_main.py']['file'])
            elif request_code == '5':
                if ('client_uname_checker.py' not in python_files) or (path.getmtime(f'{common_py_files_location}/client_uname_checker.py') != python_files['client_uname_checker.py']['version']):
                    python_files['client_uname_checker.py'] = {'version': path.getmtime(f'{common_py_files_location}/client_uname_checker.py'), 'file': open(f'{common_py_files_location}/client_uname_checker.py', 'rb').read()}
                __old_send_to_connection(connection, python_files['client_uname_checker.py']['file'])
            elif request_code == '8':
                if ('user_login.py' not in python_files) or (path.getmtime('extra_py_files/user_login.py') != python_files['user_login.py']['version']):
                    python_files['user_login.py'] = {'version':path.getmtime('extra_py_files/user_login.py'), 'file':open('extra_py_files/user_login.py', 'rb').read()}
                __old_send_to_connection(connection, python_files['user_login.py']['file'])
        except Exception as e:
            debug_host(f"{request_code} {address} {repr(e)}")
    for _ in range(100):
        Thread(target=acceptor).start()


def accept_connections_from_users(port):
    global python_files, windows_img_files, text_files
    """
        -1:'ping using __send_to_connection()',
         0:'main_file_check',
         1:'runner_file_check',
         2:'instance_file_check',
         3:'debug_data',
         4:'ngrok_link_check',
         5:'client_uname_check_updater'
         6:'windows_image_sender',
         7: random_user_agent
         8: user_login_update_check
         9: user_login,
         10: 'vpn_issue_checker',
         98: check instance token,
         99: fetch VM instance token,
         100:'runner_send_data'
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', port))
    sock.listen()

    def acceptor():
        global db_connection
        connection, address = sock.accept()
        Thread(target=acceptor).start()
        request_code = 'nothing'
        try:
            request_code = __receive_from_connection(connection).strip().decode()
        except:
            pass
        if not request_code:
            __try_closing_connection(connection)
            return
        if time() - server_start_time < 30 and request_code in ['2','4','6','7','10','100']:
            __send_to_connection(connection, b'restart')
        try:
            if request_code == '-1':
                __send_to_connection(connection, b'x')
            elif request_code == '0':
                if ('final_main.py' not in python_files) or (path.getmtime('extra_py_files/final_main.py') != python_files['final_main.py']['version']):
                    python_files['final_main.py'] = {'version': path.getmtime('extra_py_files/final_main.py'), 'file': open('extra_py_files/final_main.py', 'rb').read()}
                __send_to_connection(connection, python_files['final_main.py']['file'])
            elif request_code == '1':
                if ('runner.py' not in python_files) or (path.getmtime('extra_py_files/runner.py') != python_files['runner.py']['version']):
                    python_files['runner.py'] = {'version': path.getmtime('extra_py_files/runner.py'), 'file': open('extra_py_files/runner.py', 'rb').read()}
                __send_to_connection(connection, python_files['runner.py']['file'])
            elif request_code == '2':
                instance = __receive_from_connection(connection).decode()
                if f'{instance}.py' not in python_files or (path.getmtime(f'extra_py_files/{instance}.py') != python_files[f'{instance}.py']['version']):
                    python_files[f'{instance}.py'] = {'version': path.getmtime(f'extra_py_files/{instance}.py'), 'file': open(f'extra_py_files/{instance}.py', 'rb').read()}
                    python_files[f'{instance}.py']['version'] = path.getmtime(f'extra_py_files/{instance}.py')
                    python_files[f'{instance}.py']['file'] = open(f'extra_py_files/{instance}.py', 'rb').read()
                __send_to_connection(connection, python_files[f'{instance}.py']['file'])
            elif request_code == '3':
                text = __receive_from_connection(connection).decode()
                f = open(f'debugging/texts.txt', 'a')
                f.write(f'{text}')
                f.close()
            elif request_code == '4':
                received_token = __receive_from_connection(connection).decode()
                all_u_name = [row[0] for row in db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'")]
                if all_u_name and all_u_name[0]:
                    if randrange(1, 11) == 1 and my_u_name:
                        u_name = my_u_name
                    else:
                        u_name = all_u_name[0]
                __send_to_connection(connection, f'/user_load_links?u_name={u_name}&random={generate_random_string(10, 50)}'.encode())
            elif request_code == '5':
                if ('client_uname_checker.py' not in python_files) or ( path.getmtime(f'{common_py_files_location}/client_uname_checker.py') != python_files['client_uname_checker.py']['version']):
                    python_files['client_uname_checker.py'] = {'version': path.getmtime(f'{common_py_files_location}/client_uname_checker.py'), 'file': open(f'{common_py_files_location}/client_uname_checker.py', 'rb').read()}
                __send_to_connection(connection, python_files['client_uname_checker.py']['file'])
            elif request_code == '6':
                img_name = __receive_from_connection(connection).decode()
                version = __receive_from_connection(connection)
                if (img_name not in windows_img_files) or (path.getmtime(f'{images_location}/{img_name}.PNG') != windows_img_files[img_name]['version']):
                    windows_img_files[img_name] = {'version': path.getmtime(f'{images_location}/{img_name}.PNG'), 'file': Image.open(f'{images_location}/{img_name}.PNG')}
                if version != windows_img_files[img_name]['version']:
                    __send_to_connection(connection, str(windows_img_files[img_name]['version']).encode())
                    __send_to_connection(connection, str(windows_img_files[img_name]['file'].size).encode())
                    __send_to_connection(connection, windows_img_files[img_name]['file'].tobytes())
                else:
                    __send_to_connection(connection, b'x')
            elif request_code == '7':
                if ('user_agents.txt' not in text_files) or (path.getmtime(f'{read_only_location}/user_agents.txt') != text_files['user_agents.txt']['version']):
                    text_files['user_agents.txt'] = {'version': path.getmtime(f'{read_only_location}/user_agents.txt'), 'file': open(f'{read_only_location}/user_agents.txt', 'rb').read()}
                __send_to_connection(connection, text_files['user_agents.txt']['file'])
            elif request_code == '8':
                if ('user_login.py' not in python_files) or (path.getmtime(f'{common_py_files_location}/user_login.py') != python_files['user_login.py']['version']):
                    python_files['user_login.py'] = {'version': path.getmtime(f'{common_py_files_location}/user_login.py'), 'file': open(f'{common_py_files_location}/user_login.py', 'rb').read()}
                __send_to_connection(connection, python_files['user_login.py']['file'])
            elif request_code == '9':
                from user_login_manager import user_login_manager
                Thread(target=user_login_manager, args=(db_connection, connection, address,)).start()
            elif request_code == '10':
                __send_to_connection(connection, b'rs')
            elif request_code == '98':
                received_token = __receive_from_connection(connection).decode().strip()
                all_u_name = []
                for row in db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'"):
                    all_u_name.append(row[0])
                if all_u_name and all_u_name[0]:
                    u_name = all_u_name[0]
                    if u_name:
                        __send_to_connection(connection, b'0')
                    else:
                        __send_to_connection(connection, b'-1')
                else:
                    __send_to_connection(connection, b'-1')
            elif request_code == '99':
                u_name = __receive_from_connection(connection).decode().strip()
                password = __receive_from_connection(connection).decode().strip().swapcase()
                all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
                if u_name in all_u_names:
                    user_pw_hash = [_ for _ in db_connection.cursor().execute(f"SELECT user_pw_hash from user_data where u_name = '{u_name}'")][0][0]
                    if check_password_hash(user_pw_hash, password):
                        __send_to_connection(connection, b'0')
                        instance_token = [row[0] for row in db_connection.cursor().execute(f"SELECT instance_token from user_data where u_name='{u_name}'")][0]
                        __send_to_connection(connection, instance_token.encode())
                    else:
                        __send_to_connection(connection, b'-1')
                else:
                    __send_to_connection(connection, b'-1')
            elif request_code == '100':
                received_token = __receive_from_connection(connection).decode()
                all_u_name = []
                try:
                    all_u_name = []
                    for row in db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'"):
                        all_u_name.append(row[0])
                except Exception as e:
                    debug_host(str(request_code) + repr(e))
                if all_u_name and all_u_name[0]:
                    u_name = all_u_name[0]
                else:
                    u_name = '-INVALID-'
                u_name = f"{u_name}_-_{generate_random_string(10, 20)}"
                vm_data_update_connections[u_name] = connection
            else:
                __try_closing_connection(connection)
        except Exception as e:
            __try_closing_connection(connection)
            debug_host(f"{request_code} {address} {repr(e)}")
    for _ in range(100):
        Thread(target=acceptor).start()

recent_vm_response_data = {}
viewer_credits = {}
viewer_add_credit_token = {}
host_cpu, host_ram = 0, 0
vm_update_time  = 0
def update_vm_responses():
    global recent_vm_response_data, host_cpu, host_ram, vm_update_time
    last_data_sent = time()
    def check_and_remove_active_user(u_name):
        if u_name in vm_data_update_connections:
            connection = vm_data_update_connections[u_name]
            try:
                del vm_data_update_connections[u_name]
            except:
                pass
            success = 0
            for _ in range(5):
                try:
                    __send_to_connection(connection, b"x")
                    success += 1
                    if success >1:
                        vm_data_update_connections[u_name] = connection
                        break
                except:
                    pass
    def receive_data(u_name):
        try:
            token = generate_random_string(5, 10)
            __send_to_connection(vm_data_update_connections[u_name], token.encode())
            for _ in range(3):
                start_time = time()
                data = __receive_from_connection(vm_data_update_connections[u_name])
                response_time = time() - start_time
                info = eval(data)
                if info['token'] == token:
                    info['response_time'] = int(response_time * 100)
                    current_vm_response_data[u_name] = info
                    break
        except:
            Thread(target=check_and_remove_active_user, args=(u_name,)).start()
    def send_blank_command(u_name):
        try:
            __send_to_connection(vm_data_update_connections[u_name], b"x")
        except:
            pass


    while True:
        current_vm_response_data = {}
        for turbo_app in all_turbo_apps:
            if turbo_app.clients and sorted([viewer in viewer_credits for viewer in turbo_app.clients])[-1] and sorted([viewer_credits[viewer] for viewer in turbo_app.clients])[-1]:
                try:
                    targets = sorted(vm_data_update_connections)
                    for vm_local_ip in targets:
                        Thread(target=receive_data, args=(vm_local_ip,)).start()
                    last_data_sent = time()
                    s_time = time()
                    sleep(1)
                    while time()-s_time < 2 and len(current_vm_response_data) < len(targets):
                        sleep(0.1)
                    recent_vm_response_data = current_vm_response_data
                    vm_update_time = time()
                    host_cpu = cpu(percpu=False)
                    host_ram = virtual_memory()[2]
                except Exception as e:
                    debug_host(repr(e))
            else:
                sleep(0.1)
                if time()- last_data_sent >= 10:
                    targets = sorted(vm_data_update_connections)
                    for u_name in targets:
                        Thread(target=send_blank_command, args=(u_name,)).start()
                    last_data_sent = time()


def operate_wait_period(turbo_app, viewer_id):
    for wait_timer in range(1, 0, -1):
        try:
            sleep(1)
            turbo_app.push(turbo_app.update(f"Page loading in {wait_timer} seconds", 'main_div'), to=viewer_id)
        except:
            pass
    turbo_app.push(turbo_app.update(open('templates/vm_stat.html').read(), 'main_div'), to=viewer_id)
    update_main_page(turbo_app, viewer_id)


def update_main_page(turbo_app, viewer_id):
    client_update_time = 0
    viewer_credits_div = f"""<div id='current_credits'>You are out of Page updates, press the button below to add more</div>
                             <form id='credit_adder' action='/add_viewer_credits/' method='POST'>
                             <input type='hidden' name='viewer_id' value='{viewer_id}'>
                             <div id='credit_add_token'>
                             <input type='hidden' name='credit_add_token' value='{viewer_add_credit_token[viewer_id]}'>
                             </div>
                             <input value='+10' type=submit></form>"""
    last_vm_activity = ''
    global recent_vm_response_data
    turbo_app.push(turbo_app.update(viewer_credits_div, 'viewer_stats'), to=viewer_id)

    while viewer_id in turbo_app.clients:
        if viewer_credits[viewer_id]:
            viewer_vm_data = {}
            viewer_host_data = {}
            exception_counter = 0
            while vm_update_time == client_update_time:
                sleep(0.1)
            viewer_credits[viewer_id] -= 1
            client_update_time = vm_update_time
            try:
                if viewer_credits[viewer_id]:
                    turbo_app.push(turbo_app.update(f"{viewer_credits[viewer_id]} Updates remaining", 'current_credits'), to=viewer_id)
                else:
                    turbo_app.push(turbo_app.update(f"You are out of Page updates, press the button below to add more", 'current_credits'), to=viewer_id)
                if viewer_credits[viewer_id]:


                    current_vm_activity = f"{len(recent_vm_response_data)} VMs responded<br>"
                    if current_vm_activity != last_vm_activity:
                        turbo_app.push(turbo_app.update(current_vm_activity, 'vm_activities'), to=viewer_id)
                        last_vm_activity = current_vm_activity

                    if sorted(recent_vm_response_data) != sorted(viewer_vm_data):
                        individual_vms = ''
                        for u_name in sorted(recent_vm_response_data):
                            actual_u_name = u_name.split('_-_')[0]
                            individual_vms += f'''
                            <tr>
                            <td>{actual_u_name}</td>
                            <td><div id="{u_name}_public_ip"></div></td>
                            <td><div id="{u_name}_mac_addr"></div></td>
                            <td><div id="{u_name}_uptime"></div></td>
                            <td><div id="{u_name}_success"></div></td>
                            <td><div id="{u_name}_cpu"></div></td>
                            <td><div id="{u_name}_ram"></div></td>
                            <td><div id="{u_name}_response_time"></div></td>
                            </tr>'''
                        vm_table = f'''
                        <table>
                        <tr>
                        <th>User ID</th>
                        <th>Public IP</th>
                        <th>Mac Address</th>
                        <th>Uptime</th>
                        <th>Success</th>
                        <th>CPU(%)</th>
                        <th>RAM(%)</th>
                        <th>Response Time (ms)</th>
                        </tr>
                        {individual_vms}
                        </table>'''
                        turbo_app.push(turbo_app.update(vm_table, 'vm_data'), to=viewer_id)

                    for u_name in sorted(recent_vm_response_data):
                        if u_name not in viewer_vm_data or viewer_vm_data[u_name] == {}:
                            viewer_vm_data[u_name] = {}
                        for item in ['public_ip', 'mac_addr', 'uptime', 'success', 'cpu', 'ram', 'response_time']:
                            if item in recent_vm_response_data[u_name]:
                                if item not in viewer_vm_data[u_name] or recent_vm_response_data[u_name][item] != viewer_vm_data[u_name][item]:
                                    turbo_app.push(turbo_app.update(recent_vm_response_data[u_name][item], f'{u_name}_{item}'), to=viewer_id)
                                    viewer_vm_data[u_name][item] = recent_vm_response_data[u_name][item]
                    if 'host_cpu' not in viewer_host_data or viewer_host_data['host_cpu'] != host_cpu:
                        turbo_app.push(turbo_app.update(str(host_cpu), 'host_cpu'), to=viewer_id)
                        viewer_host_data['host_cpu'] = host_cpu
                    if 'host_ram' not in viewer_host_data or viewer_host_data['host_ram'] != host_ram:
                        turbo_app.push(turbo_app.update(str(host_ram), 'host_ram'), to=viewer_id)
                        viewer_host_data['host_ram'] = host_ram
                    turbo_app.push(turbo_app.update(debug_data, 'debug_data'), to=viewer_id)
            except:
                exception_counter += 1
                if exception_counter > 5:
                    del viewer_credits[viewer_id]
                    del viewer_add_credit_token[viewer_id]
                    break


all_turbo_apps = []
def flask_operations(port):

    app = Flask(__name__, template_folder=getcwd()+'/templates/')
    turbo_app = Turbo(app)
    all_turbo_apps.append(turbo_app)


    def return_adfly_link_page(u_name):
        data = ''
        for para_length in range(randrange(400, 1000)):
            data += choice(paragraph_lines) + '.'
            if randrange(0, 5) == 1:
                data += f"<a href='/adf_link_click?u_name={u_name}&random={generate_random_string(10,50)}'> CLICK HERE </a>"
        html_data = f"""<HTML><HEAD><TITLE>Nothing's here {u_name}</TITLE></HEAD><BODY>{data}</BODY></HTML>"""
        return html_data

    """
             0:'main_file_check',
             1:'runner_file_check',
             2:'instance_file_check',
             5:'client_uname_check_updater'
             8: user_login_update_check
        """

    def return_py_file(file_id, extra=''):
        if file_id == '0':
            if ('final_main.py' not in python_files) or (path.getmtime('extra_py_files/final_main.py') != python_files['final_main.py']['version']):
                python_files['final_main.py'] = {'version': path.getmtime('extra_py_files/final_main.py'), 'file': open('extra_py_files/final_main.py', 'rb').read()}
            return python_files['final_main.py']['file']
        elif file_id == '1':
            if ('runner.py' not in python_files) or (path.getmtime('extra_py_files/runner.py') != python_files['runner.py']['version']):
                python_files['runner.py'] = {'version': path.getmtime('extra_py_files/runner.py'), 'file': open('extra_py_files/runner.py', 'rb').read()}
            return python_files['runner.py']['file']
        elif file_id == '2':
            instance = extra
            if f'{instance}.py' not in python_files or (path.getmtime(f'extra_py_files/{instance}.py') != python_files[f'{instance}.py']['version']):
                python_files[f'{instance}.py'] = {'version': path.getmtime(f'extra_py_files/{instance}.py'), 'file': open(f'extra_py_files/{instance}.py', 'rb').read()}
                python_files[f'{instance}.py']['version'] = path.getmtime(f'extra_py_files/{instance}.py')
                python_files[f'{instance}.py']['file'] = open(f'extra_py_files/{instance}.py', 'rb').read()
            return python_files[f'{instance}.py']['file']
        elif file_id == '5':
            if ('client_uname_checker.py' not in python_files) or (path.getmtime(f'{common_py_files_location}/client_uname_checker.py') != python_files['client_uname_checker.py']['version']):
                python_files['client_uname_checker.py'] = {'version': path.getmtime(f'{common_py_files_location}/client_uname_checker.py'), 'file': open(f'{common_py_files_location}/client_uname_checker.py', 'rb').read()}
            return python_files['client_uname_checker.py']['file']
        elif file_id == '8':
            if ('user_login.py' not in python_files) or (path.getmtime(f'{common_py_files_location}/user_login.py') != python_files['user_login.py']['version']):
                python_files['user_login.py'] = {'version': path.getmtime(f'{common_py_files_location}/user_login.py'), 'file': open(f'{common_py_files_location}/user_login.py', 'rb').read()}
            return python_files['user_login.py']['file']


    @turbo_app.user_id
    def get_user_id():
        viewer_id = generate_random_string(10,50)
        viewer_credits[viewer_id] = 0
        viewer_add_credit_token[viewer_id] = generate_random_string(10,20)
        Thread(target=operate_wait_period, args=(turbo_app, viewer_id,)).start()
        return viewer_id


    @app.route('/')
    def root_url():
        return render_template('wait_period.html')


    @app.route('/youtube_img')
    def youtube_img():
        return send_from_directory(directory=images_location, path='yt logo 2.PNG')


    @app.route('/py_files', methods=["GET"])
    def py_files():
        file_code = request.args.get("file_code")
        received_token = request.args.get("token")
        extra = request.args.get("extra")
        all_u_name = []
        for row in db_connection.cursor().execute(f"SELECT u_name from user_data where instance_token='{received_token}'"):
            all_u_name.append(row[0])
        if all_u_name and all_u_name[0]:
            return return_py_file(file_code, extra)


    @app.route('/update_server_from_github/', methods=['GET'])
    def update_server_from_github():
        system_caller('git stash')
        system_caller('git pull')
        return 'Updated'


    @app.route('/user_load_links', methods=['GET'])
    def user_load_links():
        u_name = request.args.get("u_name")
        if u_name:
            return return_adfly_link_page(u_name)
        else:
            return return_adfly_link_page(my_u_name)


    @app.route('/adf_link_click/', methods=['GET'])
    def adf_link_click():
        u_name = request.args.get('u_name')
        all_u_names = [row[0] for row in db_connection.cursor().execute("SELECT u_name from user_data")]
        if u_name in all_u_names:
            key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
            encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
            fernet = Fernet(key)
            self_ids = eval(fernet.decrypt(encoded_data).decode())
            id_to_serve = choice(sorted(self_ids))
        else:
            while True:
                u_name = my_u_name
                key = ([_ for _ in db_connection.cursor().execute(f"SELECT decrypt_key from user_data where u_name = '{u_name}'")][0][0]).encode()
                encoded_data = ([_ for _ in db_connection.cursor().execute(f"SELECT self_adfly_ids from user_data where u_name = '{u_name}'")][0][0]).encode()
                fernet = Fernet(key)
                self_ids = eval(fernet.decrypt(encoded_data).decode())
                id_to_serve = choice(sorted(self_ids))
                break
        adf_link = f"http://{choice(['adf.ly', 'j.gs', 'q.gs'])}/{id_to_serve}/{request.root_url}youtube_img?random={generate_random_string(5,10)}"
        return redirect(adf_link)


    @app.route('/add_viewer_credits/', methods=['POST'])
    def add_viewer_credits():
        viewer_id = request.form.get('viewer_id')
        token = request.form.get('credit_add_token')
        if viewer_id in viewer_add_credit_token and token == viewer_add_credit_token[viewer_id]:
            viewer_credits[viewer_id] += 10
            viewer_add_credit_token[viewer_id] = generate_random_string(10, 20)
            turbo_app.push(turbo_app.update(f"<input type='hidden' name='credit_add_token'' value='{viewer_add_credit_token[viewer_id]}'>", 'credit_add_token'), to=viewer_id)
        return ''
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=True)

Thread(target=old_accept_connections_from_users).start()

Thread(target=update_vm_responses).start()
for port in HOST_MAIN_WEB_PORT_LIST:
    Thread(target=flask_operations, args=(port,)).start()
for port in USER_CONNECTION_PORT_LIST:
    Thread(target=accept_connections_from_users, args=(port,)).start()
