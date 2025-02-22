# atomic_health_line_bot
記得要把gemini 的 API 、line channel加到app_colab裡面
54 92 93行

# 發布方法：
ngrok
line webhook網址： "ngrok的網址"+"/callback"

# 檔案說明:
app_colab.py : 主程式
health_gemini.py : import 到主程式裡面，讓主程式可以用gemini

prompt.txt : 給gemini的主要instruction
(利用GAN的概念，和chatgpt一起討論與檢討gemini AI醫生，並用chatgpt生成prompt，教gemini如何當一位有同理心的好醫生)
請見： https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221zbu_UrZD6qT6jBoqd46FDqFWmFlazPUT%22%5D,%22action%22:%22open%22,%22userId%22:%22100049276867188237784%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing

# 未來展望
。處理隱私問題(line 隱私不好，要考慮換平台)(究竟一個人的血壓被發現的會怎樣我覺得我還是不懂嗚嗚嗚)\n
。處理數據的儲存，建立資料庫，用matplotlib畫圖表，並變成圖片回傳\n
。建立提醒鬧鐘與介面、line.push(?) 主動提醒功能\n
。完善小寵物的獎勵機制\n
。新增更多可被記錄的生理數值(如：眼壓)\n
。新增更好的生成有用的摘要，也要能夠分析過往數據(要專業的醫生)，拿去給真人醫生看\n
。市場調查：大家到底需要甚麼\n
。把server丟上雲端\n
。希望能變成產品，或是一個可以被大家用到而且有用APP!!\n  
