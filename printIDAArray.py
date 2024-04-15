import idc

def print_byte_array():
    # 假设 byte_3DDC0 是数组的名称
    array_name = "byte_3DDC0"
    # 假设数组中的元素个数为 31940
    array_length = 31940
    # 获取数组的起始地址
    array_address = idc.get_name_ea_simple(array_name)
    if array_address != idc.BADADDR:
        # 读取整个数组
        byte_array = idc.get_bytes(array_address, array_length)
        result = [0x0A if x == 0 else x for x in byte_array]
        result1 = ''.join(chr(x) for x in result)
        print(result1)
    else:
        print("数组 {} 未在程序中找到。".format(array_name))
# 执行打印数组的函数
print_byte_array()
