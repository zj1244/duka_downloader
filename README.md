# duka_downloader

dukascopy历史数据下载器，修复了网上其他下载器存在的很多问题，比如夏令时。下载器生成的数据基本和jforex的数据对应上。  
![](pic/1.png)

## 自动调整夏令时时间：
 
夏令时未开始，4小时分割呈现奇数  
![](pic/2.png)

夏令时开始，4小时分割呈现偶数  
![](pic/3.png)

## 基本用法
使用本地的bi5文件，如果没有就保存在本地
```.shell script
#./download_from_dukascopy.py -c 4h eurusd 2020-10-28 2020-11-04 -s e:\data
loading: e:\data\EURUSD\2020\09\28\01h_ticks.bi5
loading: e:\data\EURUSD\2020\09\28\02h_ticks.bi5
loading: e:\data\EURUSD\2020\09\28\03h_ticks.bi5
loading: e:\data\EURUSD\2020\09\28\04h_ticks.bi5
loading: e:\data\EURUSD\2020\09\28\05h_ticks.bi5
loading: e:\data\EURUSD\2020\09\28\06h_ticks.bi5
.............
loading: e:\data\EURUSD\2020\10\05\16h_ticks.bi5
loading: e:\data\EURUSD\2020\10\05\17h_ticks.bi5
loading: e:\data\EURUSD\2020\10\05\18h_ticks.bi5
loading: e:\data\EURUSD\2020\10\05\19h_ticks.bi5
loading: e:\data\EURUSD\2020\10\05\20h_ticks.bi5
loading: e:\data\EURUSD\2020\10\05\21h_ticks.bi5
end...........

```

不是用本地bi5文件
```.shell script
#./download_from_dukascopy.py -c 60min eurusd 2019-10-28 2019-10-30
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/00h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/01h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/02h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/03h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/04h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/05h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/06h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/07h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/08h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/09h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/10h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/11h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/12h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/13h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/14h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/15h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/16h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/17h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/18h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/19h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/20h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/21h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/22h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/28/23h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/00h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/01h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/02h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/03h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/04h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/05h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/06h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/07h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/08h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/09h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/10h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/11h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/12h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/13h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/14h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/15h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/16h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/17h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/18h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/19h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/20h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/21h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/22h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/29/23h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/00h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/01h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/02h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/03h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/04h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/05h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/06h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/07h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/08h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/09h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/10h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/11h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/12h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/13h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/14h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/15h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/16h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/17h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/18h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/19h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/20h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/21h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/22h_ticks.bi5
downloading: https://datafeed.dukascopy.com/datafeed/EURUSD/2019/09/30/23h_ticks.bi5

```