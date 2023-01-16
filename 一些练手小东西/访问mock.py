# encoding: utf-8
import requests
import time
import threading


def show_time(func):  # 装饰函数
    def inner(*args):
        begin_time = time.time()
        res = func(*args)
        end_time = time.time()
        run_tile = end_time - begin_time
        print(f'测试用例运行时间：{run_tile:.0f}s')
        return res
    return inner

HOST = 'http://127.0.0.1:9999'


def create_order():
    url = f'{HOST}/api/order/create/'
    json = {
        "user_id": "LiTaiAng",
        "goods_id": "20230101",
        "num": 1,
        "amount": 200.6
    }
    res = requests.post(url=url, json=json)
    return res.json()


# 30秒内，每5秒访问一次
# 频率    5s一次
# 超时机制   timeout
@show_time
def query_order(params, interval=5, timeout=30):
    """
    :param data: id
    :param interval: 频率
    :param timeout: 超时时间
    :return:
    """
    url = f'{HOST}/api/order/get_result/'
    start_time = time.time()
    end_time = start_time + timeout
    count = 0
    while time.time() < end_time:
        res = requests.get(url=url, params=params)
        count += 1
        if res.text:
            print(f'第{count}次请求，请求成功，返回：{res.json()}')
            res.json()
            break
        else:
            print(f'第{count}次请求，请求失败! 请稍后再试')
        time.sleep(interval)
    return res



def Thread_query_order(params):
    t1 = threading.Thread(target=query_order, args=(params,))
    t1.daemon = True
    t1.start()


if __name__ == '__main__':
    id_data = create_order()
    data = {
        'fwe': 'few'
    }
    Thread_query_order(data)
    for r in range(20):
        time.sleep(1)
        print(f'{r}')



