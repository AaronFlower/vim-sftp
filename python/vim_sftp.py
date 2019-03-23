import os
import vim
from os.path import dirname, isfile
import commentjson as json
import paramiko

SftpCache = {}

def _load_config():
    '''
        Find the sftp-config.json 文件
    '''
    config_file_str = 'sftp-config.json'
    file_name = vim.current.buffer.name
    cur_dir = dirname(file_name)
    config_file = ''

    while cur_dir:
        config_file = cur_dir + '/' + config_file_str
        if isfile(config_file):
            break

        if cur_dir == '/' :
            return None
        cur_dir = dirname(cur_dir)

    try:
        with open(config_file) as file:
            config = json.load(file)
            return config_file, config
    except json.JSONLibraryException as e:
        print("Parse sftp-config.json file failed.")
        print(e.__class__, e)
        return None

def connect(config):
    '''
    根据 config 信息建立连接并缓存起来。
    '''
    # get host key, if we know one
    try:
        host_keys = paramiko.util.load_host_keys(
            os.path.expanduser("~/.ssh/known_hosts")
        )
    except IOError:
        try:
            host_keys = paramiko.util.load_host_keys(
                os.path.expanduser("~/ssh/known_hosts")
            )
        except IOError:
            print("*** Unable to open host keys file")
            host_keys = {}

    host = config.get("host")
    user = config.get("user")
    port = config.get("port")
    password = config.get("password")
    remote_path = config.get("remote_path")

    hostkeytype = None
    hostkey = None
    if host in host_keys:
        hostkeytype = host_keys[host].keys()[0]
        hostkey = host_keys[host][hostkeytype]
        print("Using host key of type %s " % hostkeytype)

    # now, connect and use paramiko Transport to negotiate SSH2
    # accross the connection.
    try:
        t = paramiko.Transport((host, int(port)))
        t.connect(
            hostkey,
            user,
            password,
            # gss_host=socket.getfqdn(host),
            # gss_auth=UseGSSAPI,
            # gss_kex=DoGSSAPIKeyExchange,
        )
        sftp = paramiko.SFTPClient.from_transport(t)
        SftpCache[config.get('config_file')] = {
            'conn': sftp,
            'remote_path': remote_path
        }
        # create observer
        vim.command("echom 'connection succeed!'")

    except Exception as e:
        print("*** Caught exception: %s:%s " % (e.__class__, e))

def sftp_put():
    file_name = vim.current.buffer.name
    config_file, config = _load_config()
    config['config_file'] = config_file

    if SftpCache.get(config_file) == None:
        connect(config)
    else:
        print('already connected')
        print(SftpCache.get(config_file))

    sftp = SftpCache.get(config_file)
    config_dir = dirname(config_file)
    remote_file = sftp['remote_path'] + file_name[len(config_dir):]
    print(file_name)
    print(remote_file)
    sftp['conn'].put(file_name, remote_file)
    vim.command("echom 'upload succeed!'")

    return None

def sftp_clear():
    if SftpCache:
        vim.command("echom 'clear the sftp connection'")
        for _, item in SftpCache.items():
            print("close item:", item)
            item.get('conn').close()
        vim.command("sleep 300m")
    return None
