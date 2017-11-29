# coding:utf-8

"yirimao"

__author__ = 'Raincal'

from multiprocessing import Pool
import os
import requests

if not os.path.exists('yirimao'):
    os.mkdir('yirimao')


def getJSONData(url, data={}):
    try:
        r = requests.post(url, data=data)
        r.raise_for_status()
        return r.json()
    except:
        return {'status': 4000}


def getPageSize(url):
    maxPage = getJSONData(url)['data']['activity']['pageIndexMax']
    return int(maxPage)


def getFileName(url):
    fileName = url.split('/')[-1]
    return fileName


def saveImg(imgUrl, imgPath=''):
    fname = getFileName(imgUrl)
    print(fname)

    if not os.path.exists('yirimao/' + imgPath):
        os.mkdir('yirimao/' + imgPath)

    ipath = 'yirimao/' + imgPath + fname
    if not os.path.exists(ipath):
        r = requests.get(imgUrl)
        with open(ipath, 'wb') as f:
            f.write(r.content)
            print('%s saved.' % fname)


def main(page):
    print('crawing page %d' % page)
    data = {'pageIndex': page}
    json = getJSONData(url, data)

    if json['status'] == 2000:
        if json['data']['catPrizeWallpaper']:
            wpUrl = json['data']['catPrizeWallpaper']['cover']
            saveImg(wpUrl, 'wallpaper/')

        cards = json['data']['activity']['cards']
        for card in cards:
            if card['category']['id'] != 3:
                saveImg(card['imageUrl'])
    elif json['status'] == 4000 and json['data'] is None:
        print('page %d data does not exist!' % page)


if __name__ == '__main__':
    url = 'https://app-api.yirimao.com/v1/activity/activity/newest'
    pages = getPageSize(url)
    print('total pages %d' % pages)
    pool = Pool()
    pool.map(main, range(pages))
    pool.close()
    pool.join()
