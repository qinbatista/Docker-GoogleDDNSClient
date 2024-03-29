import os
import time
import requests
import threading
import subprocess


class GoogleDDNSClient:
    def __init__(self):
        self.__file_path = "/google_ddns_client_logs.txt"
        self.__google_username_v6 = self._get_file_content("GOOGLE_USERNAME_V6").strip()
        self.__google_password_v6 = self._get_file_content("GOOGLE_PASSWORD_V6").strip()
        self.__domain_name_v6 = self._get_file_content("DOMAIN_NAME_V6").strip()
        self.__google_username_v4 = self._get_file_content("GOOGLE_USERNAME_V4").strip()
        self.__google_password_v4 = self._get_file_content("GOOGLE_PASSWORD_V4").strip()
        self.__domain_name_v4 = self._get_file_content("DOMAIN_NAME_V4").strip()
        self._get_ipv4_website = "https://checkip.amazonaws.com"
        self._get_ipv6_website = "https://api6.ipify.org"

    def _get_file_content(self, file_path):
        content = ""
        with open(file_path, "r") as f:
            content = f.read()
        os.remove(file_path)
        self.__log(f"{file_path}:{content}")
        return content

    def _start(self):
        thread_refresh = threading.Thread(target=self._start_thread, name="t1", args=())
        thread_refresh.start()

    def _start_thread(self):
        while True:
            try:
                self.__log(f"sending IP")
                self._post_ip_to_google_DNS()
                self.__log(f"sended IP")
                time.sleep(30)
            except Exception as e:
                self.__log("[Error]_start_thread"+str(e))

    def _post_ip_to_google_DNS(self):
        try:
            # Assuming __get_current_ipv4() and __get_current_ipv6() are methods that return the current IPs
            this_ipv4 = self.__get_current_ipv4()
            this_ipv6 = self.__get_current_ipv6()

            # Update IPv4
            if this_ipv4:
                ipv4_url = f"https://{self.__google_username_v4}:{self.__google_password_v4}@domains.google.com/nic/update?hostname={self.__domain_name_v4}&myip={this_ipv4}"
                ipv4_curl_command = f"curl '{ipv4_url}'"
                ipv4_result = subprocess.run(ipv4_curl_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                self.__log(f"IPv4 CURL Output: {ipv4_result.stdout}")
                if ipv4_result.stderr:
                    self.__log(f"IPv4 CURL Error: {ipv4_result.stderr}")

            # Update IPv6
            if this_ipv6:
                ipv6_url = f"https://{self.__google_username_v6}:{self.__google_password_v6}@domains.google.com/nic/update?hostname={self.__domain_name_v6}&myip={this_ipv6}"
                ipv6_curl_command = f"curl '{ipv6_url}'"
                ipv6_result = subprocess.run(ipv6_curl_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                self.__log(f"IPv6 CURL Output: {ipv6_result.stdout}")
                if ipv6_result.stderr:
                    self.__log(f"IPv6 CURL Error: {ipv6_result.stderr}")

        except subprocess.CalledProcessError as e:
            # Log the error for the failed curl command
            self.__log(f"CURL Command Failed: {e.stderr}")
        except Exception as e:
            # Log any other unexpected errors
            self.__log(f"Unexpected Error: {str(e)}")

    def __get_current_ipv6(self):
        try:
            response = requests.get(self._get_ipv6_website, timeout=5)
            response.raise_for_status()  # Raises an HTTPError for bad HTTP responses
            return response.text.strip()
        except requests.exceptions.HTTPError as errh:
            self.__log(f"[get_host_ipv6] HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            self.__log(f"[get_host_ipv6] Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            self.__log(f"[get_host_ipv6] Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            self.__log(f"[get_host_ipv6] Request Exception: {err}")
        return None

    def __get_current_ipv4(self):
        try:
            response = requests.get(self._get_ipv4_website)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            return response.text.strip()
        except requests.exceptions.HTTPError as errh:
            self.__log(f"[get_host_ip] HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            self.__log(f"[get_host_ip] Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            self.__log(f"[get_host_ip] Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            self.__log(f"[get_host_ip] Request Exception: {err}")
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
