import requests

WEATHER_TRANSLATE = {
    "Sunny": "晴", "Clear": "晴", "Partly cloudy": "多云", "Cloudy": "阴",
    "Overcast": "阴", "Mist": "薄雾", "Fog": "雾", "Freezing fog": "冻雾",
    "Patchy rain possible": "局部有雨", "Patchy snow possible": "局部有雪",
    "Patchy sleet possible": "局部有雨夹雪", "Patchy freezing drizzle possible": "局部有冻毛毛雨",
    "Thundery outbreaks possible": "可能有雷暴", "Blowing snow": "吹雪", "Blizzard": "暴雪",
    "Light drizzle": "毛毛雨", "Freezing drizzle": "冻毛毛雨", "Heavy freezing drizzle": "强冻毛毛雨",
    "Patchy light rain": "局部小雨", "Light rain": "小雨", "Moderate rain at times": "间歇中雨",
    "Moderate rain": "中雨", "Heavy rain at times": "间歇大雨", "Heavy rain": "大雨",
    "Light freezing rain": "小雨夹雪", "Moderate or heavy freezing rain": "中到大雨夹雪",
    "Light sleet": "雨夹雪", "Moderate or heavy sleet": "中到大雨夹雪",
    "Patchy light snow": "局部小雪", "Light snow": "小雪", "Patchy moderate snow": "局部中雪",
    "Moderate snow": "中雪", "Patchy heavy snow": "局部大雪", "Heavy snow": "大雪",
    "Ice pellets": "冰粒", "Light rain shower": "小阵雨", "Moderate or heavy rain shower": "中到大雨阵雨",
    "Torrential rain shower": "暴雨", "Light sleet showers": "小雨夹雪阵",
    "Moderate or heavy sleet showers": "中到大雨夹雪阵", "Light snow showers": "小雪阵",
    "Moderate or heavy snow showers": "中到大雪阵", "Light showers of ice pellets": "小冰粒阵",
    "Moderate or heavy showers of ice pellets": "中到大雨冰粒阵",
    "Patchy light rain with thunder": "局部小雨有雷", "Moderate or heavy rain with thunder": "中到大雨有雷",
    "Patchy light snow with thunder": "局部小雪有雷", "Moderate or heavy snow with thunder": "中到大雪有雷",
    "Unknown": "未知"
}

WIND_DIR_TRANSLATE = {
    "N": "北", "NNE": "东北偏北", "NE": "东北", "ENE": "东北偏东",
    "E": "东", "ESE": "东南偏东", "SE": "东南", "SSE": "东南偏南",
    "S": "南", "SSW": "西南偏南", "SW": "西南", "WSW": "西南偏西",
    "W": "西", "WNW": "西北偏西", "NW": "西北", "NNW": "西北偏北"
}

def get_weather(city):
    base_url = "http://wttr.in"
    try:
        response = requests.get(
            f"{base_url}/{city}?format=j1",
            timeout=10,
            headers={"User-Agent": "curl/7.68.0"}
        )
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            return None, "未找到该城市信息，请检查城市名称是否正确"
        
        nearest_area = data.get("nearest_area", [{}])[0]
        area_name = nearest_area.get("areaName", [{}])[0].get("value", "")
        country = nearest_area.get("country", [{}])[0].get("value", "")
        
        if not area_name:
            return None, "未找到该城市信息，请检查城市名称是否正确"
        
        current = data.get("current_condition", [{}])[0]
        weather_en = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        weather = WEATHER_TRANSLATE.get(weather_en, weather_en)
        temp = current.get("temp_C", "未知")
        feels_like = current.get("FeelsLikeC", "未知")
        wind_speed = current.get("windspeedKmph", "未知")
        wind_dir_en = current.get("winddir16Point", "未知")
        wind_dir = WIND_DIR_TRANSLATE.get(wind_dir_en, wind_dir_en)
        humidity = current.get("humidity", "未知")
        visibility = current.get("visibility", "未知")
        
        result = {
            "city": city,
            "weather": weather,
            "temp": temp,
            "feels_like": feels_like,
            "wind_speed": wind_speed,
            "wind_dir": wind_dir,
            "humidity": humidity,
            "visibility": visibility
        }
        return result, None
        
    except requests.exceptions.ConnectionError:
        return None, "网络连接失败，请检查网络后重试"
    except requests.exceptions.Timeout:
        return None, "请求超时，请稍后再试"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return None, "未找到该城市信息，请检查城市名称是否正确"
        return None, f"请求错误: {e.response.status_code}"
    except Exception as e:
        return None, f"查询失败: {str(e)}"

def display_weather(data):
    print("\n" + "="*40)
    print(f"【{data['city']} 今日天气】".center(38))
    print("="*40)
    print(f"天气状况: {data['weather']}")
    print(f"当前温度: {data['temp']}°C")
    print(f"体感温度: {data['feels_like']}°C")
    print(f"风力风速: {data['wind_dir']} {data['wind_speed']} km/h")
    print(f"相对湿度: {data['humidity']}%")
    print(f"能见度: {data['visibility']} km")
    print("="*40 + "\n")

def main():
    print("="*40)
    print("天气查询工具".center(38))
    print("="*40)
    
    while True:
        city = input("请输入要查询的城市名称 (输入 'quit' 退出): ").strip()
        
        if city.lower() == 'quit':
            print("感谢使用，再见！")
            break
        
        if not city:
            print("错误：城市名称不能为空\n")
            continue
        
        print(f"\n正在查询 {city} 的天气信息...")
        
        result, error = get_weather(city)
        
        if error:
            print(f"错误：{error}\n")
        else:
            display_weather(result)

if __name__ == "__main__":
    main()
