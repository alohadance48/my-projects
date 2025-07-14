import requests
import time

def main():
    for request in range(1000):
        time.sleep(0.2)
        response = requests.get('https://visited-necessity-navigation-truck.trycloudflare.com/')
        print(response.status_code)


if __name__ == '__main__':
    main()
