# encoding: utf-8
import hashlib


def get_md5_psw(psw):
    """
    将密码以md5方式加密
    :param psw: 未加密的密码
    :return: 加密后的结果
    """
    # 实例化
    md5 = hashlib.md5()
    # 调用加密方法
    md5.update(psw.encode('utf-8'))
    return md5.hexdigest()