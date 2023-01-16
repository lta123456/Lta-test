# encoding: utf-8
# c_id = input()
# if int(c_id[-2:-1]) % 2:
#     print('男')
# else:
#     print('女')

iphone = input()
if iphone.isdigit():
    if len(iphone) == 11:
        s = int(iphone[0:3])
        if s >= 130 and s <= 150:
            print('移动')
        elif s >= 151 and s <= 170:
            print('联通')
        elif s >= 171 and s <= 190:
            print('电信')
        else:
            print('手机号错误')
    else:
        print('手机号位数错误')
else:
    print('手机号格式错误')