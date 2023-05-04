# tcp server recv socket data and parse img data info
# 2023-04-26 

import socket
import struct
import time
import numpy as np
import cv2
import os

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.

img_folder = '/home/gmrakari/img/2b_2s'

def _exist_dir():
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

def tcp_server_start():
    # 创建TCP/IP套接字对象
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # 设置socket选项，防止端口被占用
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定服务器地址和端口号
        server_address = ('10.0.0.9', 8000)
        sock.bind(server_address)
        # 监听连接请求
        sock.listen(5)

        while True:
            print('等待客户端连接...')
            connection, client_address = sock.accept()
            current_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
            try:
                print('客户端已连接:', client_address)
                while True:
                    data = b''
                    while len(data) < 480 * 640 * 4 * 2 + 128 * 128 * 4 * 2 + 3 * 4:
                        chunk = connection.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                    if not data:
                        break

                    print(len(data))
                    # 解析数据
                    vis_img_buf_len = 480 * 640 * 4
                    ir_img_buf_len = 480 * 640 * 4
                    vis_s_img_buf_len = 128 * 128 * 4
                    ir_s_img_buf_len = 128 * 128 * 4
                    img_score_len = 3 * 4

                    vis_img_data = data[:vis_img_buf_len]
                    ir_img_data = data[vis_img_buf_len:vis_img_buf_len + ir_img_buf_len]
                    vis_s_img_data = data[vis_img_buf_len + ir_img_buf_len:vis_img_buf_len + ir_img_buf_len + vis_s_img_buf_len]
                    ir_s_img_data = data[vis_img_buf_len + ir_img_buf_len + vis_s_img_buf_len:vis_img_buf_len + ir_img_buf_len + vis_s_img_buf_len + ir_s_img_buf_len]
                    img_scores = data[vis_img_buf_len + ir_img_buf_len + vis_s_img_buf_len + ir_s_img_buf_len:vis_img_buf_len + ir_img_buf_len + vis_s_img_buf_len + ir_s_img_buf_len + img_score_len]
                    prob, score, live_score = struct.unpack('III', img_scores)

                    print('prob:', prob)
                    print('score:', score)
                    print('live_score:', live_score)
                    print(current_time)

                    # 将RGB图像转换为BGR图像
                    vis_img = np.frombuffer(vis_img_data, dtype=np.uint8).reshape((640, 480, 4))
                    vis_img = cv2.cvtColor(vis_img, cv2.COLOR_RGBA2BGR)

                    ir_img = np.frombuffer(ir_img_data, dtype=np.uint8).reshape((640, 480, 4))
                    ir_img = cv2.cvtColor(ir_img, cv2.COLOR_RGBA2BGR)

                    vis_s_img = np.frombuffer(vis_s_img_data, dtype=np.uint8).reshape((128, 128, 4))
                    vis_s_img = cv2.cvtColor(vis_s_img, cv2.COLOR_RGBA2BGR)

                    ir_s_img = np.frombuffer(ir_s_img_data, dtype=np.uint8).reshape((128, 128, 4))
                    ir_s_img = cv2.cvtColor(ir_s_img, cv2.COLOR_RGBA2BGR)

                    # 创建以当前时间命名的文件夹并保存图像
                    img_folder_current = os.path.join(img_folder, current_time)
                    os.makedirs(img_folder_current, exist_ok=True)

                    # 保存图像到本地
                    vis_img_file_name = os.path.join(img_folder_current,
                                                     'vis_b_img_prob:{}_score:{}_live_score:{}.bmp'.format(prob, score, live_score))
                    cv2.imwrite(vis_img_file_name, ir_img)

                    ir_img_file_name = os.path.join(img_folder_current,
                                                    'ir_b_img_prob:{}_score:{}_live_score:{}.bmp'.format(prob, score, live_score))
                    cv2.imwrite(ir_img_file_name, vis_img)

                    vis_img_file_name = os.path.join(img_folder_current,
                                                     'vis_s_img_pro:{}_score:{}_live_score:{}.bmp'.format(prob, score, live_score))
                    cv2.imwrite(vis_img_file_name, ir_s_img)

                    ir_img_file_name = os.path.join(img_folder_current,
                                                    'ir_s_img_prob:{}_score:{}_live_score:{}.bmp'.format(prob, score, live_score))
                    cv2.imwrite(ir_img_file_name, vis_s_img)

            except ConnectionResetError as e:
                print(f'连接重置: {e}')

            finally:
                # 关闭连接
                connection.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    _exist_dir()
    tcp_server_start()
