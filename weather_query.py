import requests
import json

API_KEY = "YOUR_API_KEY"  # 请替换为你的和风天气 API Key

def get_location_id(city_name):
    """根据城市名称获取城市ID"""
    url = f"https://geoapi.qweather.com/v2/city/lookup"
    params = {
        "location": city_name,
        "key": API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == "200" and data.get("location"):
            return data["location"][0]["id"]
        elif data.get("code") == "404":
            return None
        else:
            return None
    except requests.RequestException:
        return None

def get_weather(city_id):
    """根据城市ID获取天气信息"""
    url = f"https://devapi.qweather.com/v7/weather/now"
    params = {
        "location": city_id,
        "key": API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("code") == "200":
            return data.get("now")
        else:
            return None
    except requests.RequestException:
        return None

def format_weather_output(city_name, weather_data):
    """格式化输出天气信息"""
    print("\n" + "=" * 40)
    print(f"📍 城市: {city_name}")
    print("=" * 40)
    print(f"🌡️  温度: {weather_data.get('temp', 'N/A')}°C")
    print(f"🌡️  体感温度: {weather_data.get('feelsLike', 'N/A')}°C")
    print(f"☁️  天气状况: {weather_data.get('text', 'N/A')}")
    print(f"💨 风向: {weather_data.get('windDir', 'N/A')}")
    print(f"🌪️  风力: {weather_data.get('windScale', 'N/A')}级")
    print(f"💨 风速: {weather_data.get('windSpeed', 'N/A')} km/h")
    print(f"💧 湿度: {weather_data.get('humidity', 'N/A')}%")
    print(f"👁️  能见度: {weather_data.get('vis', 'N/A')} km")
    print(f"📊 气压: {weather_data.get('pressure', 'N/A')} hPa")
    print("=" * 40 + "\n")

def main():
    print("\n🌤️  天气查询小程序")
    print("-" * 20)
    
    while True:
        city_name = input("\n请输入城市名称（输入 'q' 退出）: ").strip()
        
        if city_name.lower() == 'q':
            print("\n👋 感谢使用，再见！")
            break
        
        if not city_name:
            print("❌ 错误：城市名称不能为空，请重新输入。")
            continue
        
        print(f"\n🔍 正在查询 '{city_name}' 的天气信息...")
        
        # 获取城市ID
        city_id = get_location_id(city_name)
        
        if city_id is None:
            print(f"❌ 错误：未找到城市 '{city_name}'，请检查城市名称是否正确。")
            continue
        
        # 获取天气信息
        weather_data = get_weather(city_id)
        
        if weather_data is None:
            print("❌ 错误：获取天气信息失败，请稍后重试。")
            continue
        
        # 输出天气信息
        format_weather_output(city_name, weather_data)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已终止，再见！")
    except Exception as e:
        print(f"\n❌ 程序发生未知错误: {e}")
