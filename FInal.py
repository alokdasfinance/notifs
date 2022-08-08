import yfinance as yf
import datetime
import pygame
import time
import cgitb
from notify_run import Notify
from stocksymbol import StockSymbol

# api_key = '12dbdc0f-00b8-43f6-bf9e-6d95c8fbe831'
# ss = StockSymbol(api_key)
# stock_tickers = ss.get_symbol_list(market="US", symbols_only=True)
# cgitb.enable()
file2 = open("volumetickers.txt", "r")
volume_tickers = file2.readlines()
#Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
#Columns: [Open, High, Low, Close, Adj Close, Volume]

#Rules :
#If the second hourly candle is a strong bullish candle, then a substantial low on the first candle can be ignored


#7/23
    #['SAM', 'GGAL', 'BBAR', 'TRNS', 'CLBS', 'SPCB']
#7/25
    #['AMD', 'PBR', 'LI', 'SQM', 'AES', 'OLN', 'CWEN', 'CACI',
    #'NEP', 'ZLAB', 'SWN', 'ABCM', 'PNM', 'SIX', 'CPA',
    #'SBRA', 'IAS', 'HL', 'JKS', 'CAMT', 'INT', 'REE', 'NOAH',
    #'DAC', 'GDEN', 'PRO', 'AROC', 'CDE', 'AMR', 'HA', 'CONN',
    #'DESP', 'MUI', 'VUZI', 'VIST', 'NAN', 'ISO', 'RRGB', 'AOUT',
    #'CPSS', 'MTNB', 'PMTS', 'PANL', 'NLTX', 'AMPY', 'GALT', 'SEAC', 'POLA', 'IPNFF']
#7/27
    #['WMT', 'NFLX', 'F', 'FCX', 'CVE']
#7/28
    #['SIGA', 'COST', 'KO', 'WMT']
#7/29
    #['INTC', 'F', 'FCX', 'X', 'TLRY', 'GEVO', 'BTTX', 'TBLT']
final_list = []
# volume_checked_list = []
# volume_reject_list = []
ticker_count = 0
notify = Notify()
push_notification = ''
#notify.send("working")

progress = 0
pygame.init()
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
x = 400
y = 100
display_surface = pygame.display.set_mode((x, y))
pygame.display.set_caption('Progress')
font = pygame.font.Font('freesansbold.ttf', 20)
text = font.render('Starting', True, green, blue)
textRect = text.get_rect(center=(x/4.5, y/2))
#textRect.center = (X // 2, Y // 2)
length = 0
running = True

def average(closing, opening):
    difference = closing - opening
    percent = difference/opening
    percent_difference = percent * 100
    return percent_difference

def time_change(time):
    test = str(time)
    year = time[0:4]
    month = time[4:6]
    day = time[6:8]
    return year, month, day

#Determine and format the next date
previous_date = datetime.datetime.today() - datetime.timedelta(days=1)
formatted_time = previous_date.strftime('%Y%m%d')
previous_year, previous_month, previous_day = time_change(formatted_time)
previous_day_formatted = "" + previous_year + '-' + previous_month + '-' + previous_day + ""

#Determine and format the current date
current_date_formatted = datetime.datetime.today().strftime ('%Y%m%d')
current_year, current_month, current_day = time_change(current_date_formatted)
current_day_formatted = "" + current_year + '-' + current_month + '-' + current_day + ""

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for tickers in volume_tickers:
            opening = []
            closing = []
            percent_change = []
            positive = 0
            negative = 0
            display_surface.fill(white)
            display_surface.blit(text, textRect)

            ticker_count = ticker_count + 1

            #Downloads individual ticker data and compiles hourly opening and closing prices
            stock_data = yf.download(tickers = tickers, period='1d', interval='1h')
            for open_data in stock_data['Open']:
                opening.append(open_data)
            for close_data in stock_data['Close']:
                closing.append(close_data)

            #Takes the average hourly change and adds it to a list
            if len(opening) == len(closing):
                percent_change.append(tickers)
                for i in range(1, len(opening)):
                    percent_difference = average(closing[i], opening[i])
                    percent_change.append(percent_difference)

            #Checks to see if the first hourly candle is green and determines the change in the following candles
            for i in range(1, len(percent_change)):
                if percent_change[i] > 0 and average(closing[0], opening[0]) > 0:
                    positive = positive + 1
                else:
                    negative = negative + 1

            if positive > 2:
                final_list.append(tickers)
                print(final_list)
                #print(average(closing[1], opening[1]))

            progress = str(round(ticker_count/len(volume_tickers) * 100))
            #Updates pygame window with progress
            text = font.render(progress + "% searched. " + str(len(final_list)) + " found", True, black)
            print(progress + "% searched. " + str(len(final_list)) + " found")
            pygame.display.update()
            #Fixes not responding when clicked on problem
            pygame.event.pump()
            #time.sleep(3)
            if progress == 25:
                notify.send("25%")
            elif progress == 50:
                notify.send("50%")
            elif progress == 75:
                notify.send("75%")
            length = length + 1
        print(length)
        if length == len(volume_tickers):
            break
    #Filters through all the positively increasing stocks and checks for volume
#     for resultant in final_list:
#         stock_data = yf.download(resultant, previous_day_formatted, current_day_formatted)
#         if abs(int(stock_data['Volume'])) > 10000000:
#             volume_checked_list.append(resultant)
#         else:
#             volume_reject_list.append(resultant)

    #Compiles volume checked tickers and sends a push notification
for i in range(0, len(final_list)):
    if i == 0:
        push_notification = push_notification + " " + final_list[i]
    else:
        push_notification = push_notification + ", " + final_list[i]

notify.send(push_notification)
print('The final list : ' + str(final_list))
#print('Volume Spread Concerns : ' + str(volume_reject_list))
#print('The final list checked for volume: ' + str(volume_checked_list))
#print(tickers)
