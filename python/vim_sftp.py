import os
import vim
from os.path import dirname, isfile
import paramiko
import jsonutil as util
import json

SftpCache = {}

def _load_config():
    '''
        Find the sftp config file
    '''
    config_file_str = vim.eval('g:sftp_config_name')
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
        with open(config_file, 'r') as cfile:
            content = cfile.read()
            content = util.remove_comments(content)
            content = util.remove_trailing_commas(content)
            config = json.loads(content)
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
            print("*** Unable to open host keys file ***")
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
        config_file = config.get('config_file')

        SftpCache[config_file] = {
            'conn': sftp,
            'remote_path': remote_path
        }
        # create observer
        vim.command("echom 'connection succeed!'")
        return SftpCache[config_file]

    except Exception as e:
        print("*** Caught exception: %s:%s " % (e.__class__, e))
        return None

def mkdir_p(sftp, remote_directory):
    """Change to this directory, recursively making new folders if needed.
    Returns True if any folders were created."""
    if remote_directory == '/':
        # absolute path so change directory to root
        sftp.chdir('/')
        return
    if remote_directory == '':
        # top-level relative directory must exist
        return
    try:
        sftp.chdir(remote_directory) # sub-directory exists
    except IOError:
        dirname, basename = os.path.split(remote_directory.rstrip('/'))
        mkdir_p(sftp, dirname) # make parent directories
        sftp.mkdir(basename) # sub-directory missing, so created it
        sftp.chdir(basename)
        return True

def sftp_put():
    file_name = vim.current.buffer.name
    config_file, config = _load_config()
    config['config_file'] = config_file
    sftp = SftpCache.get(config_file)

    if sftp == None:
        sftp = connect(config)
    else:
        print('already connected')

    if sftp == None:
        print('SFTP connect failed! ')
        return

    config_dir = dirname(config_file)
    remote_file = sftp['remote_path'] + file_name[len(config_dir):]
    remote_dir =  dirname(remote_file)
    conn = sftp.get('conn')
    try:
        conn.chdir(remote_dir)  # Test if remote_path exists
    except IOError as e:
        print('change dir success')
        mkdir_p(conn, remote_dir)
        conn.chdir(remote_dir)


    print('has change the file')
    try:
        conn.put(file_name, remote_file)
    except Exception:
        vim.command("echom 'upload failed!'")
    print(file_name)
    print(remote_file)
    print(dirname(remote_file))
    # sftp['conn'].put(file_name, remote_file)
    vim.command("echo 'upload succeed!'")

    return None

def sftp_clear():
    if SftpCache:
        vim.command("echom 'clear the sftp connection'")
        for _, item in SftpCache.items():
            item.get('conn').close()
        vim.command("sleep 10m")
    return None
