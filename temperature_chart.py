import matplotlib.pyplot as plt
import numpy as np
import os

def plot_temperature_chart(time, body_temperature, save_path):
    """
    繪製體溫變化圖，並儲存圖片
    :param time: 時間點列表
    :param body_temperature: 體溫數據列表
    :param save_path: 圖片儲存路徑
    """
    time_numeric = np.linspace(6, 6 + 1.5 * (len(time) - 1), len(time))  # 轉換為數值時間

    # 標準體溫範圍
    normal_temp_low = 36.1
    normal_temp_high = 37.2

    # 事件標籤與顏色 (模擬日常活動影響)
    events = ["Wake Up", "Breakfast", "Work", "Break", "Lunch", "Meeting", "Afternoon Work",
              "Tea Break", "Dinner", "Rest", "Evening Activity", "Sleep"]
    event_colors = ["orange", "blue", "gray", "green", "blue", "gray", "gray", "green",
                    "blue", "purple", "red", "black"]

    # 確保事件數量與時間點數量匹配
    if len(events) > len(time):
        events = events[:len(time)]
        event_colors = event_colors[:len(time)]

    # 建立圖表
    plt.figure(figsize=(12, 6))

    # 繪製體溫變化圖
    plt.plot(time_numeric, body_temperature, marker='o', color='darkred', label="Body Temperature")

    # 添加正常體溫範圍區域
    plt.axhspan(normal_temp_low, normal_temp_high, color='lightblue', alpha=0.3, label="Normal Temperature Range")

    # 添加事件柱狀圖
    bar_width = 0.3  # 設定事件顯示的寬度
    for i in range(len(time_numeric)):
        plt.bar(time_numeric[i], max(body_temperature) + 0.2, width=bar_width, color=event_colors[i], alpha=0.3)
        plt.text(time_numeric[i], max(body_temperature) + 0.3, events[i], ha='center', fontsize=10, rotation=30)

    # 設定標題與軸標籤
    plt.title("Body Temperature Fluctuations Throughout the Day", pad=20)
    plt.xlabel("Time of Day")
    plt.ylabel("Body Temperature (°C)")
    plt.xticks(time_numeric, time)
    plt.ylim(35.8, 37.5)  # 限制溫度範圍，以便清楚顯示變化
    plt.legend(loc="upper right")

    # 確保儲存資料夾存在
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 儲存圖片
    plt.savefig(save_path)
    plt.close()

    return save_path  # 回傳圖片儲存路徑
