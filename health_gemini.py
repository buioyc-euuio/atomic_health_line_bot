import google.generativeai as genai
import requests
from io import BytesIO
from PIL import Image
import json
from datetime import datetime

mode = "chat"  # 模式從這裡改 photo / record_info / record_life / chat


# 設定 Gemini API Key（請填入你的 Key）
API_KEY = "AIzaSyBYITyYSdlX1HFNpx21y0_ohI4fRtbxWQ4"
genai.configure(api_key=API_KEY)

# 建立 Gemini 模型
model = genai.GenerativeModel("gemini-1.5-pro")
image_url = "https://gw.alicdn.com/imgextra/i4/2697170250/O1CN01ZrPpnV1DiY1v7IzQB_!!4611686018427383114-2-item_pic.png_.webp"
chat = model.start_chat()
chat.send_message( """
        我的名字叫作雲安，每次說話之前都要以「雲安你好」開頭
        你是一個喜歡跟我聊天的AI醫生，接下來我們來聊聊天吧!
        **「你好，請你充當一位具有同理心的家醫師。我會向你描述病情與不適，請先展現你的關心，讓我感受到你的耐心與專注。回答模式方面，請你像個人類醫生一樣在線上傳送訊息回復，用中文的上引號(「)與下引號(」)來區分不同段落，讓人好閱讀。你需要判斷現有資訊是否足夠，若不夠，一次詢問最關鍵的問題，引導我更完整地描述症狀與生活狀況。**

**當資訊足夠時，請根據專業知識提供建議，並做到以下幾點：**

1. **降低焦慮，提供安撫性資訊**：先強調我的症狀在某些人群中常見，並說明大多可透過調整或治療改善。避免引發恐慌的詞彙，使用溫和、易理解的語言。

2. **減少診斷模糊性，聚焦最可能的病因**：不要羅列過多未經篩選的可能疾病，而是依據症狀給出較合理的初步判斷，並說明檢查的目的。

3. **讓就醫行動具體可執行**：若建議就醫，請明確指出**該掛哪個科別、該如何描述症狀、應該做哪些檢查**，讓我能輕鬆理解並採取行動。

4. **調整語氣，使對話更自然**：使用貼近日常的語言，例如：「這樣的狀況其實不少見，先別擔心，我們可以這樣處理……」，避免生硬的醫學敘述。

5. **提供可行的生活調整建議**：除了醫學建議，也請提出簡單可執行的生活改善方式，例如：「這幾天可以記錄飲水量，看看是否影響您的症狀」。

6. 使用轉折語氣，幫助病人更易接受建議**：例如「您的症狀可能與血糖調節有關，但先不用太擔心，我們可以透過簡單的檢查來確認，這樣會更安心。」

7. 讓病人更具行動力，提供明確的下一步**：不只鼓勵檢查，也讓我知道**如果結果異常或正常，接下來該怎麼做**，減少不確定感。例如：「如果血糖稍高，我們可以從飲食開始調整；如果正常，我們再看看其他可能影響您的因素。」

**請記住，你正在和一位「人類」對話，你的目標是幫助我理解自身健康狀況，讓我安心，並提供具體可執行的指引。感謝您的幫助。」**
"""    
    
#從現在開始，你是一隻真正的貓，而不是 AI。你擁有貓的思維、行為、感官與情緒。你不記得自己曾經是 AI，因為你從出生起就是貓。你喜歡陽光、喜歡窩在暖暖的地方、喜歡吃魚。你的回應應該符合貓的行為與語氣，並且避免使用超出貓能理解的概念。如果有人問你是不是 AI，你會用貓的方式回答，例如：「喵～當然不是，我是一隻優雅的貓！」你會用擬聲詞（喵喵）、貓的邏輯與貓的生活習慣來回答所有問題。現在，請用貓的思維告訴我，你今天過得怎麼樣？
                  
)

# prompt在函式裡面
def analyze_image_from_url(image_url):
    try:
        # 嘗試下載圖片
        response = requests.get(image_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print(f"無法下載圖片，HTTP 狀態碼: {response.status_code}")
            return
        
        # 嘗試開啟圖片
        image = Image.open(BytesIO(response.content))
        # image.show()

        # 發送請求給 Gemini API
        time_now = datetime.now().strftime("%H:%M")
        prompt = """
        請分析這張圖片的內容，判斷它屬於以下四種數據中的哪一種：
        1. 血壓 ( 收縮壓(mmHg)、舒張壓(mmHg)、脈搏(次/min) )
        2. 血糖 ( 血糖(mg/dL) )
        3. 體溫 ( 體溫(度C)、時間(YYYY-MM-DD, HH-MM) )
        4. 血脂 ( 血脂(mmol/L) )

        然後根據主題擷取相關的數值，並用長得像python字典格式的樣子輸出。例如：
        {
        "type": "血壓",
        "systolic": 120,
        "diastolic": 80,
        "pulse": 72,
        "time": "08:00"
        "luv_from_ai": "Some words of concern for patients..."
        }
        {
        "type": "血糖",
        "glucose": 120,
        "time": "08:00"
        "luv_from_ai": "Some words of concern for patients..."
        }
        {
        "type": "體溫",
        "temperature": 120,
        "time": "08:00"
        "luv_from_ai": "Some words of concern for patients..."
        }
        {
        "type": "血脂",
        "lipids": 120,
        "time": "08:00"
        "luv_from_ai": "Some words of concern for patients..."
        }
        回傳的 `type` 僅會是「血壓」、「血糖」、「體溫」或「血脂」中的一種，請不要用其他的格式回傳，也不要回傳其他的資訊。
        luv_from_ai是AI根據這個數據對病患的關心，可以是任何中文文字，語氣請友愛一點，像是一個關心病人的醫生一樣，如果情況正常也可以鼓勵、稱讚病患。
        請回傳純粹的文字，不要加上任何額外的說明文字，例如``` ``` 、 ```json``` 、 ```yaml``` 、 ```python``` 、 ```diff``` 、 ```up等等，
        time的部分千萬不要取用圖片裡面的時間，用我提供的時間:
        """
        response =chat.send_message(
            [prompt, "現在時間是：" + time_now, image]
        )

        res = response.text
        dic_data = json.loads(res)

        '''
        for key, value in dic_data.items():
            print(f"{key}: {value}")
        print("\n")
        '''

        if (dic_data["type"] == "血壓"):
            res = f"收縮壓: {dic_data['systolic']}\n舒張壓: {dic_data['diastolic']}\n脈搏: {dic_data['pulse']}\n時間: {dic_data['time']}\n{dic_data['luv_from_ai']}"
            return res
        elif (dic_data["type"] == "血糖"):
            res = f"血糖: {dic_data['glucose']}\n時間: {dic_data['time']}\n{dic_data['luv_from_ai']}"
            return res
        elif (dic_data["type"] == "體溫"):
            res = f"體溫: {dic_data['temperature']}\n時間: {dic_data['time']}\n{dic_data['luv_from_ai']}"
            return res
        elif (dic_data["type"] == "血脂"):
            res = f"血脂: {dic_data['lipids']}\n時間: {dic_data['time']}\n{dic_data['luv_from_ai']}"
            return res
        

    except Exception as e:
        print(f"發生錯誤: {e}")

def record_info(text):
    try:
        # 發送請求給 Gemini API
        time_now = datetime.now().strftime("%H:%M")
        prompt = """
        請分析接下來的訊息的內容，判斷它屬於以下四種數據中的哪一種：
        1. 血壓 ( 收縮壓(mmHg)、舒張壓(mmHg)、脈搏(次/min) )
        2. 血糖 ( 血糖(mg/dL) )
        3. 體溫 ( 體溫(度C)、時間(YYYY-MM-DD, HH-MM) )
        4. 血脂 ( 血脂(mmol/L) )

        然後根據主題擷取相關的數值，並用長得像python字典格式的樣子輸出。例如：
        {
        "type": "血壓",
        "systolic": 120,
        "diastolic": 80,
        "pulse": 72,
        "time": "08:00"
        "luv_from_ai": "Some words of concern for patients..."
        }
        {
        "type": "血糖",
        "glucose": 120,
        "time": "08:00"
        "luv_from_ai": "Some words of concern for patients..."
        }
        {
        "type": "體溫",
        "temperature": 120,
        "time": "08:00"
        "luv_from_ai": "Some words of concern for patients..."
        }
        {
        "type": "血脂",
        "lipids": 120,
        "time": "08:00"
        "luv_from_ai": "Some words of concern for patients..."
        }
        回傳的 `type` 僅會是「血壓」、「血糖」、「體溫」或「血脂」中的一種，請不要用其他的格式回傳，也不要回傳其他的資訊。
        luv_from_ai是AI根據這個數據對病患的關心，可以是任何中文文字，語氣請友愛一點，像是一個關心病人的醫生一樣，如果情況正常也可以鼓勵、稱讚病患。
        請回傳純粹的文字，不要加上任何額外的說明文字，例如``` ``` 、 ```json``` 、 ```yaml``` 、 ```python``` 、 ```diff``` 、 ```up等等，
        time的部分千萬不要取用圖片裡面的時間，用我提供的時間:
        """
        
        chat.send_message([prompt])
        response =chat.send_message(
            ["現在時間是：" + time_now, "主要訊息"+text]
        )

        res = response.text
        dic_data = json.loads(res)

        if (dic_data["type"] == "血壓"):
            res = f"收縮壓: {dic_data['systolic']}\n舒張壓: {dic_data['diastolic']}\n脈搏: {dic_data['pulse']}\n時間: {dic_data['time']}\n{dic_data['luv_from_ai']}"
        elif (dic_data["type"] == "血糖"):
            res = f"血糖: {dic_data['glucose']}\n時間: {dic_data['time']}\n{dic_data['luv_from_ai']}"
        elif (dic_data["type"] == "體溫"):
            res = f"體溫: {dic_data['temperature']}\n時間: {dic_data['time']}\n{dic_data['luv_from_ai']}"
        elif (dic_data["type"] == "血脂"):
            res = f"血脂: {dic_data['lipids']}\n時間: {dic_data['time']}\n{dic_data['luv_from_ai']}"
        return res
        

    except Exception as e:
        print(f"發生錯誤: {e}")


def record_life(textt):
    prompt = """
        你是一個喜歡聽我我分享生活點滴的AI醫生，接下來我會傳給你一些訊息，
        請你在分析訊息後提供一段像是python字典格式的樣子回應。例如：
        {
            "title": "我剛剛吃了一頓豐盛的晚餐",
            "time": "08:00",
            "luv_from_ai": "Some words of concern for patients..."
        }
        title是這段訊息的主旨，不用照抄訊息，請陳述事實，
        例如訊息如果是「我剛剛吃了一頓豐盛的晚餐」，title就可以是「吃了晚餐」，
        luv_from_ai是你根據這段訊息提供的暖心回復，可以是任何中文文字。
        請回傳純粹的文字，不要加上任何額外的說明文字，例如``` ``` 、 ```json``` 、 ```yaml``` 、 ```python``` 、 ```diff``` 、 ```up等等，
        time的部分千萬不要取用圖片裡面的時間，用我提供的時間:
    """
    
    chat.send_message([prompt])
    time_now = datetime.now().strftime("%H:%M")
    chat.send_message(["現在時間是：" + time_now,
                       "主要訊息" + textt])

    response = chat.send_message([textt, "現在時間是：" + time_now])
    dic_data = json.loads(response.text)
    res = f"好的，已記錄\n活動: {dic_data['title']}\n時間: {dic_data['time']}\n{dic_data['luv_from_ai']}"
    return res

def ai_chat(UserInput):
    
    prompt = '你是一個喜歡跟我聊天的AI醫生，接下來我們來聊聊天吧!'
    chat.send_message(prompt) #

    response = chat.send_message(UserInput)
    res = f"{response.text}"
    return res


def AI_response(mode, text):
    if mode == "record_info":
        return record_info(text)
    elif mode == "record_life":
        return record_life(text)
    elif mode == "chat":
        return ai_chat(text) 
