import paramiko

class SSH:
    """SSH远程连接"""

    def __init__(self, ip, username, password, port=22):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def shell_cmd(self, cmd):
        """执行shell命令"""
        try:
            # 创建SSH对象
            ssh = paramiko.SSHClient()
            # 对远程服务器的连接进行设置         自动添加策略
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            # 创建连接
            ssh.connect(
                self.ip,
                self.port,
                self.username,
                self.password,
                timeout=5
            )
            # 执行shall命令
            # 标准输入 标准输出 错误句柄
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # 获取命令结果
            content = stdout.read().decode('utf-8')
            # 返回的结果会有换行符，通过\n进行分割
            res = content.split(r'\n')
            # 关闭连接
            ssh.close()
            return res
        except Exception as e:
            print('远程执行shell命令失败')
            return False


    def shell_upload(self, localpath, remotepath):
        """上传文件"""
        try:
            # 1.实例化一个transport对象      需要传一个元组对象 ip和端口号
            transport = paramiko.Transport((self.ip, self.port))
            # 2.与远端的服务器建立一个SSH连接
            # 传入用户名密码
            transport.connect(username=self.username, password=self.password)
            # 3.上传文件
            # 使用paramiko中的SFTPClient这个类中的from_transport方法
            # 传入一个传输对象 就是上面实例化的transport对象
            # 会返回一个SFTP对象
            sftp = paramiko.SFTPClient.from_transport(transport)
            # 调用PUT方法实现上传
            # 有两个参数 第一个是本地完整文件路径，第二个是服务器的文件路径
            sftp.put(localpath, remotepath)
            # 4.关闭连接
            transport.close()
            print('文件上传成功，上传至：{}'.format(remotepath))
            return True
        except Exception as e:
            print('文件上传失败')
            return False

    def shell_download(self, localpath, remotepath):
        """下载文件"""
        try:
            # 1.实例化一个transport对象      需要传一个元组对象 ip和端口号
            transport = paramiko.Transport((self.ip, self.port))
            # 2.与远端的服务器建立一个SSH连接
            # 传入用户名密码
            transport.connect(username=self.username, password=self.password)
            # 3.上传文件
            # 使用paramiko中的SFTPClient这个类中的from_transport方法
            # 传入一个传输对象 就是上面实例化的transport对象
            # 会返回一个SFTP对象
            sftp = paramiko.SFTPClient.from_transport(transport)
            # 调用PUT方法实现上传
            # 有两个参数 第一个是本地完整文件路径，第二个是服务器的文件路径
            sftp.get(remotepath, localpath)
            # 4.关闭连接
            transport.close()
            print('文件下载成功，下载至：{}'.format(localpath))
            return True
        except Exception as e:
            print('文件下载 失败')
            return False


