import os
import time
import requests
import base64
import threading
import subprocess

class GoogleDDNSClient:
    def __init__(self):
        self._fn_stdout = "/root/ip_out"
        self.__file_path = "/root/logs.txt"
        self.__username = ""
        self.__password = ""
        self._my_domain = ""
        with open("/Username.txt", "r") as f:
            self.__username = f.readline()
        with open("/Password.txt", "r") as f:
            self.__password = f.readline()
        with open("/domain_name.txt", "r") as f:
            self._my_domain = f.readline()
        print("self.__username:"+self.__username)
        print("self.__password:"+self.__password)
        print("self._my_domain:"+self._my_domain)
        # https://domains.google.com/checkip banned by Chinese GFW
        self._get_ip_website = "https://checkip.amazonaws.com"
        self.__ip = ""

    def _start(self):
        self.__log("_start")
        thread_refresh = threading.Thread(target=self._start, name="t1", args=())
        thread_refresh.start()

    def _start(self):
        while True:
            try:
                self.__post_ip_address()
                time.sleep(600)
            except Exception as e:
                self.__log("_start"+str(e))

    def __post_ip_address(self):
        try:
            self.__ip = self.__get_host_ip()
            self.__log("[my ip] "+self.__ip)
            print("[my ip] "+self.__ip)
            if self.__ip != "":
                _get_static_ip_stdout = open(self._fn_stdout, 'w+')
                # command = "curl -i -H 'Authorization:Basic "+self.__base64()+"' -H 'User-Agent: google-ddns-updater email@yourdomain.com' https://" + \
                #     self.__username+":"+self.__password+"@domains.google.com/nic/update?hostname=" + \
                #     self._my_domain+" -d 'myip="+self.__ip+"' > /dev/null"
                # print(command)
                # process = subprocess.Popen(command, stdout=_get_static_ip_stdout,stderr=_get_static_ip_stdout, universal_newlines=True, shell=True)
                # process.wait()
                url = f"https://{self.__username}:{self.__password}@domains.google.com/nic/update?hostname={self._my_domain}&myip={self.__ip}"
                result = requests.post(url).text.strip()
                print("result="+url)
                print("result="+result)
                self.__log("[posted ip]"+str(self.__ip)+", wait for 10 seconds")
                _get_static_ip_stdout.close()
                time.sleep(10)
                os.remove(self._fn_stdout)
        except Exception as e:
            print("error when updating ip"+str(e))
            self.__log("error when updating ip"+str(e))

    def __get_host_ip(self):
        self.__ip = ""
        try:
            self.__ip = requests.get(self._get_ip_website).text.strip()
            return self.__ip
        except Exception as e:
            print("[__get_host_ip ] "+str(e))
            self.__log("[__get_host_ip ] "+str(e))
            return ""


    def __log(self, result):
        # if os.path.isfile(self.__file_path)==False:
        # with open(self.__file_path,"a+") as f:pass
        # print("key:key"+str(len(content)))
        with open(self.__file_path, "a+") as f:
            f.write(result+"\n")
        if os.path.getsize(self.__file_path) > 1024*128:
            with open(self.__file_path, "r") as f:
                content = f.readlines()
                # print("content:"+str(len(content)))
                os.remove(self.__file_path)

    def __base64(self):
        theString = self.__username+":"+self.__password
        encoded_string = base64.b64encode(theString.encode('ascii'))
        return encoded_string.decode('ascii')


if __name__ == '__main__':
    # os.system("ssr start")
    ss = GoogleDDNSClient()
    ss._start()
