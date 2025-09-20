import requests
import time

def check_app_status():
    apps = [
        {"name": "Comprehensive Analysis", "url": "http://localhost:8501", "port": 8501},
        {"name": "Data-Driven Insights Dashboard", "url": "http://localhost:8502", "port": 8502}
    ]
    
    print("🔍 Checking Application Status...")
    print("=" * 50)
    
    for app in apps:
        try:
            response = requests.get(app["url"], timeout=5)
            if response.status_code == 200:
                print(f"✅ {app['name']} - RUNNING")
                print(f"   URL: {app['url']}")
                print(f"   Status: {response.status_code}")
            else:
                print(f"⚠️  {app['name']} - RESPONDING (Status: {response.status_code})")
        except requests.exceptions.ConnectionError:
            print(f"❌ {app['name']} - NOT RUNNING")
            print(f"   URL: {app['url']} - Connection failed")
        except requests.exceptions.Timeout:
            print(f"⏱️  {app['name']} - TIMEOUT")
        except Exception as e:
            print(f"❌ {app['name']} - ERROR: {str(e)}")
        print()
    
    print("=" * 50)
    print("📋 Instructions:")
    print("1. Open your web browser")
    print("2. Go to http://localhost:8501 for Comprehensive Analysis")
    print("3. Click the 'DATA-DRIVEN INSIGHTS' button to open the dashboard")
    print("4. Or directly access http://localhost:8502 for the insights dashboard")

if __name__ == "__main__":
    check_app_status()
