from copy import deepcopy
import requests
import yaml
from ping3 import ping
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

request_proxy = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
list_url = "https://api.github.com/repos/hello-earth/cloudflare-better-ip/contents/cloudflare?ref=main"
base_url = "https://raw.githubusercontent.com/hello-earth/cloudflare-better-ip/main/cloudflare/"
regions = ["HK", "JP", "KR"]
delay_threshold = 0.1

yaml_path_git = '../vlworker.yaml'

def get_ips():
    logger.info("get_ips...")
    response = requests.get(list_url, proxies=request_proxy, verify=False)
    files = [f["name"] for f in response.json()]
    ips = []
    for file in files:
        full_url = base_url + file
        logger.info(full_url)
        response = requests.get(full_url, proxies=request_proxy, verify=False)
        lines =  response.text.split("\n")
        for line in lines:
            if ":443" in line:
                for region in regions:
                    if region in line:
                        logger.info(line)
                        ip = line.split(":443")[0]
                        delays = []
                        for i in range(10):
                            delay = ping(ip, timeout=delay_threshold)
                            if not delay:
                                break
                            delays.append(delay)
                        logger.info("delays:")
                        logger.info(delays)
                        if len(delays) == 10:
                            ips.append((ip, region))
                        break
    return ips


if __name__ == "__main__":
    logger.info("Starting...")

    ips = get_ips()
    logger.info("all_ips:" + str(len(ips)))
    logger.info(ips)

    logger.info("read basic yaml...")
    with open("basic.yaml") as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
    proxy_temp = yaml_data['proxies'][0]

    logger.info("generate new yaml data...")
    for i in range(len(ips)):
        (ip, region) = ips[i]
        proxy_data = deepcopy(proxy_temp)
        proxy_data['name'] = "vl_" + str(i) + "_" + region
        proxy_data['server'] = ip
        yaml_data['proxies'].append(proxy_data)
        yaml_data['proxy-groups'][0]['proxies'].append(proxy_data['name'])
        yaml_data['proxy-groups'][1]['proxies'].append(proxy_data['name'])

    logger.info("write yaml file...")
    with open(yaml_path_git, 'w') as f:
        yaml.dump(yaml_data, f, allow_unicode=True, encoding='utf-8')

    logger.info("Finished.")



