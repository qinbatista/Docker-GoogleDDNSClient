import os
import time
import requests
import base64
import threading
import subprocess


class GoogleDDNSClient:
    def __init__(self):
        self.__google_username_v6 = ""
        self.__google_password_v6 = ""
        self.__domain_name_v6 = ""
        self.__google_username_v4 = ""
        self.__google_password_v4 = ""
        self.__domain_name_v4 = ""
        self._get_ip_website = "https://checkip.amazonaws.com"
        self.__file_path = "/root/logs.txt"

    def _start(self):
        self.__log("_start")
        thread_refresh = threading.Thread(target=self._start, name="t1", args=())
        thread_refresh.start()

    def _start(self):
        while True:
            try:
                self._post_ip_to_google_DNS()
                time.sleep(30)
            except Exception as e:
                self.__log("start"+str(e))

    def _post_ip_to_google_DNS(self):
        try:
            this_ipv6 = self.__get_current_ipv6()
            this_ipv4 = self.__get_current_ipv4()
            requests.post(f"https://{self.__google_username_v6}:{self.__google_password_v6}@domains.google.com/nic/update?hostname={self.__domain_name_v6}&myip={this_ipv6}")
            requests.post(f"https://{self.__google_username_v4}:{self.__google_password_v4}@domains.google.com/nic/update?hostname={self.__domain_name_v4}&myip={this_ipv4}")
        except Exception as e:
            self.__log(f"_post_ip_address:{str(e)}")

    def __get_current_ipv6(self):
        try:
            return requests.get("https://api6.ipify.org", timeout=5).text
        except requests.exceptions.ConnectionError as ex:
            return None

    def __get_current_ipv4(self):
        try:
            return requests.get(self._get_ip_website).text.strip()
        except Exception as e:
            self.__log("[get_host_ip ] "+str(e))
            return ""

    def __log(self, result):
        with open(self.__file_path, "a+") as f:
            f.write(result+"\n")
        if os.path.getsize(self.__file_path) > 1024*128:
            with open(self.__file_path, "r") as f:
                content = f.readlines()
                os.remove(self.__file_path)

if __name__ == '__main__':
    ss = GoogleDDNSClient()
    ss._start()
