---
layout: post
title: 'Android - Stocks app'
tags:
  - android
  - finance
  - github
  - java
  - stocks
---
I’ve written and Android app that can be used to view stocks and shares information from a wide variety of different businesses. The user maintains their own stocks portfolio so they only see the latest figures and information for the tickers that they are interested in - be it technology businesses such as Google or Microsoft, or perhaps just the popular financial indicator such as the FTSE or Dow Jones. The portfolio can be added to or removed from at the users convenience.

The full source code for this app is available on my [GitHub account][1].

Also [download the .apk file][2] to install it on your own devices (Froyo and above).

Rather than presenting the information in a big long table, this app aims to give you the basic information about each ticker in a more graphical way. I’ve used colour coded tiles instead of a table which displays red for a ticker that has gone down in price in the current day of trading, or green if it has risen. Other pieces of the most important information is also present in each of the tiles. This includes the market the stock trades in, the current price, the price change, the price change percentage and the market capitalisation value.

Here is the main app display which shows the ticker tiles for each of the stocks currently in the users’ portfolio. As more stocks are added, tiles are added to the bottom. The figures themselves can be updated by tapping the icon in the top rightmost corner. In a way this almost replicates ‘live tiles’ in Windows 8.

![Stocks Main](/images/2013/stocks_main.jpg){: .center-image width="338"}

As I said before the tickers that are monitored on this screen can easily be added to through the use of the ‘+’ icon in the top right hand corner. This brings up the ‘Add ticker’ screen that allows you to search for a given company. In this example I search for ‘Google’ which brings up a list of possible stocks to add to the monitored portfolio. Here I choose the main Google ticker ‘GOOG’. It immediately gets added as another tile on the main screen with the most recent price information. To remove a ticker from the portfolio, hold your finger on the appropriate tile and select ‘ok’ in the confirmation menu that appears. The tile will be immediately removed from the main screen and the figures for the stock will no longer be downloaded unless the ticker is added again through the ‘Add Ticker’ view.

![Stocks Add](/images/2013/stocks_add.jpg){: .center-image width="338"}

![Stocks Added](/images/2013/stocks_added1.jpg){: .center-image width="338"}

To view more detailed information and figures about a particular ticker in your portfolio, simply tap the appropriate tile that contains the relevant ticker. This brings up a new screen containing further financial figures about the stock along with a news feed with items relating to the stock. The news feed is updated constantly with the tickers to present the newest articles. Tapping a news article opens up the article in your web browser. For example here is the display for Yahoo Inc which was accessed by simply touching the Yahoo tile on the main display. As you can see the news feed is presented at the bottom and more detailed figures are at the top including the Day Highs and Low, Years High and Low and Volume figures.

![Stocks Info](/images/2013/stocks_info.jpg){: .center-image width="338"}

When inside the detailed information view for a particular stock, you can also view various charts for the stock which illustrate the price changes over a certain timeframe. Access this by tapping the ‘View Chart’ button. By default a 3 month chart will be shown however you can change the charts timespan by selecting an option from the top of the page. Here is an example showing the 1 month chart for Yahoo -

![Stocks Chart](/images/2013/stocks_chart.jpg){: .center-image width="338"}

Each view in the app is fully compatible with a wide range of screen resolutions in both portrait and landscape. For example when flipped to landscape, the detailed information view for a stock is changed to present the information in a more user friendly manner -

![Stocks Info Landscape](/images/2013/stock_info_landscape.jpg){: .center-image width="561"}

All data in the app is downloaded from the API’s by Yahoo! Finance (free for personal use). The app is also compatible with devices running Android Froyo (version 8) and above. I may do further posts on the internal infrastructure of the app which relies heavily on parsing retrieved XML and JSON data.

Get the full source code from my [GitHub account][1].

[Download the .apk file][2] to install the app on your own devices (Froyo and above).

 [1]: https://github.com/raharrison/Stocks
 [2]: https://ryanharrison.co.uk/apps/stocks/Stocks.apk