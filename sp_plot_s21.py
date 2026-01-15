import skrf as rf
import matplotlib.pyplot as plt
import numpy as np
import os

# 获取脚本所在目录并切换到该目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# 设置一个美观的绘图风格
plt.style.use('seaborn-v0_8-whitegrid')

try:
    # 1. 加载S2P文件（只需要加载一次）
    gain_set=['1','11']
    network = dict.fromkeys(gain_set)

    #network['wo power']=rf.Network('no_power.s2p')
    #network['0']=rf.Network('0.s2p')
    network['1']=rf.Network('1.s2p')
    network['11']=rf.Network('11.s2p')
    network['111']=rf.Network('111.s2p')
    network['1111']=rf.Network('1111.s2p')
    network['11111']=rf.Network('11111.s2p')
    network['111111']=rf.Network('111111.s2p')
    network['1111111']=rf.Network('1111111.s2p')

    # 2. 定义我们要绘制的S参数列表
    # 每个元组包含: (图表标题, (m, n) 索引)
    plots_to_make = [
        ('S21_focus', (1, 0))
    ]


    # 3. 循环创建、保存并显示每一张图
    for title, (m, n) in plots_to_make:
        print(f"正在生成 {title} 的图表...")
        
        # --- 在循环内部创建新的图和坐标轴 ---
        # 这样可以确保每次都是一张独立的、全新的图
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # 使用scikit-rf的绘图函数，并指定要绘制的S参数
        for g,s in network.items():
            s.plot_s_db(m=m, n=n, ax=ax, label=g)
        
        
        # 自定义图表信息
        ax.set_title(f'S-Parameter Magnitude ({title})')
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude (dB)')
        ax.legend()
        ax.grid(True)
        # 将 y 轴刻度设置为每 1 dB 一个刻度
        try:
            ymin, ymax = ax.get_ylim()
            # 向外取整确保刻度覆盖整个范围
            ymin = np.floor(ymin)
            ymax = np.ceil(ymax)
            ax.set_yticks(np.arange(ymin, ymax + 1, 1))
        except Exception:
            # 如果发生任何问题（例如数据为空），就忽略，让 matplotlib 使用默认刻度
            pass
        
        # 调整布局以防标签被裁剪
        plt.tight_layout()
        
        # 定义保存的文件名
        filename = f'{title}_plot.png'
        
        # --- 保存当前这张图 ---
        # 使用高质量设置（300 DPI）并裁剪掉多余的白边
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"图表已保存到: {filename}")
        
        # --- 显示当前这张图 ---
        # plt.show()会显示图像，并且在窗口关闭后清空画布，为下一张图做准备
        plt.show()

    print("\n所有图表已处理完毕！")

except FileNotFoundError:
    print("错误：未找到'cal_thru.s2p'文件。请确保数据文件与脚本在同一目录下。")
except Exception as e:
    print(f"处理文件时发生错误: {e}")