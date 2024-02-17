
from PIL import Image, ImageDraw, ImageFont
# import Image, ImageDraw, ImageFont
from random import randint
from os.path import exists
import datetime
from pandas_datareader import data as pdr
import yfinance as yfin
import matplotlib.pyplot as plt

def getPastImage(xsize, ysize, data, label = None, imagepath = None):
    pass

    image = Image.new(mode = "RGB", size = (xsize, ysize), color=(0,0,0,0))
    
    textSize = 25

    # draw axi
    axiThickness = 3
    axiGap = 10
    axiColour = (100, 100, 100)
    for x in range(axiGap, xsize - axiGap):
        for y in range(axiThickness):
            image.putpixel((x, ysize - y - axiGap), axiColour)
    for y in range(axiGap, ysize - axiGap):
        for x in range(axiThickness):
            image.putpixel((x + axiGap, y), axiColour)
    
    if len(data) < 2:
        image.save("image.png" if imagepath is None else imagepath)
        return
    
    # get user data
    balances = data#[randint(10, 100) for _ in range(10)]
    

    bmax = max(balances)
    bmin = min(balances)
    brange = bmax - bmin
    maxSizeY = (ysize - (2 * axiGap))
    
    draw = ImageDraw.Draw(image)

    xpos = axiGap
    xinc = (xsize - (2 * axiGap)) / len(balances)
    
    for i in range(0, len(balances) - 2):
        cBalanceR = (balances[i] - bmin) / brange
        nBalanceR = (balances[i + 1] - bmin) / brange
        draw.line((
                xpos, cBalanceR * maxSizeY,
                xpos + xinc, nBalanceR * maxSizeY
        ))

        xpos += xinc
    
    if label is not None:
        assert exists("font.ttf")
        Font = ImageFont.truetype("font.ttf", textSize)
    
        draw.text(
                (xsize / 2 - len(label), 2),
                label, axiColour,
                font = Font
            )

    image.save("image.png" if imagepath is None else imagepath)




def getPopularGraphs(moneyInvested, tickers):
# hard coded examples
    dates_invested = [datetime.date(2024,1,15), datetime.date(2023,6,19), datetime.date(2024,1,10), datetime.date(2020,7,15)]
    money_invested = [moneyInvested for _ in range(len(tickers) - 1)] #USD


    end_time = datetime.date.today()
    yfin.pdr_override()

    # start_time = date_invested #end_time - datetime.timedelta(days=365)

    data = []

    for index, (ticker, start_time, invested) in enumerate(zip(tickers, dates_invested, money_invested)):
        df = pdr.get_data_yahoo(ticker, start=start_time, end=end_time)
        df.reset_index(inplace=True)
        df.set_index('Date', inplace=True)
        print(df.head())
        # Adjusted Close takes dividends, stock splits and new stock offerings into account
        df['Adj Close'].mul(invested / df['Open'][0]).plot()
        plt.savefig(f'static/image{index + 2}.jpg')
        plt.clf()

        #high low average between time period

        highest = max(df['High'])
        lowest = min(df['Low'])
        avg_high = sum(df['High']) / len(df['High'])
        avg_low = sum(df['Low']) / len(df['Low'])
        avg_adj_close = sum(df['Adj Close']) / len(df['Adj Close'])

        data.append([highest, lowest, avg_high, avg_low, avg_adj_close])

        # return highest, lowest, avg_high, avg_low, avg_adj_close
    return data

#func saves a number of stocks images
# txt all stats




if __name__ == "__main__":
    getPastImage(300, 200, "label")




















# import sqlalchemy as sa

# engine = sa.create_engine("postgresql://doadmin:AVNS_JkvcfAiuwN-gsSf6K0c@app-784b9fa7-3b44-405e-9170-d80f0dd5e72d-do-user-14798294-0.c.db.ondigitalocean.com:25060/defaultdb?sslmode=require")


# with engine.connect() as conn:
#     cur = conn.exec_driver_sql("SELECT * FROM user")
#     print(cur.fetchall())