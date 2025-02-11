from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
from os import system
# import pandas as pd
# from tabulate import tabulate

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
url = "http://ventura1.acesphere.com/Derivatives/OIDashboardViewAll_5.aspx?Ind=I&Inst=OPTIDX&OptType=&symbol=NIFTY&ExpDate=2024.09.26&SortExpression=OIDIff&sortdirection=desc&Expind=1"

def main():
    try:
        raw_data = []
        data = []
        driver.get(url)
        sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find('table', {"id" : "ctl00_MainContentHolder_grdvOIDashBoardViewAll"})
            
        for row in content.find_all('tr'):
            cols = row.find_all('th', {"class" : "InGridHeader"})
            raw_data.append([col.text.strip() for col in cols])
            cols = row.find_all('td')
            raw_data.append([col.text.strip() for col in cols])

        data = [[element.replace("\n", "").replace("                                                  ", " ").replace("  ","-") for element in sublist] for sublist in raw_data]
        data = [sublist for sublist in data if sublist]
        data_processed = []
        ce_data = []
        pe_data = []

        for d in data:
            d.pop(4)
            d.pop(6)
            d.pop(8)
            d.pop(8)
            d.pop(8)
            data_processed.append(d)

        ois = []
        for oi in data_processed:
            try:
                ois.append(int(oi[6]))
            except:
                pass

        high_oi = max(ois)
        for coi in data_processed:
            try:
                if high_oi == int(coi[6]):
                    high = int(coi[1][3:8])
            except:
                pass

        for i in data:
            try:
                if int(i[1][3:8]) == high:
                    if i[1][0:2] == "CE":
                        ce_data.append(i)
                    elif i[1][0:2] == "PE":
                        pe_data.append(i)
                elif (int(i[1][3:8]) == high + 50) or (int(i[1][3:8]) == high - 50):
                    if i[1][0:2] == "CE":
                        ce_data.append(i)
                    elif i[1][0:2] == "PE":
                        pe_data.append(i)
                elif (int(i[1][3:8]) == high + 100) or (int(i[1][3:8]) == high - 100):
                    if i[1][0:2] == "CE":
                        ce_data.append(i)
                    elif i[1][0:2] == "PE":
                        pe_data.append(i)
                elif (int(i[1][3:8]) == high + 150) or (int(i[1][3:8]) == high - 150):
                    if i[1][0:2] == "CE":
                        ce_data.append(i)
                    elif i[1][0:2] == "PE":
                        pe_data.append(i)
                elif (int(i[1][3:8]) == high + 200) or (int(i[1][3:8]) == high - 200):
                    if i[1][0:2] == "CE":
                        ce_data.append(i)
                    elif i[1][0:2] == "PE":
                        pe_data.append(i)
            except:
                pass

        ce_data = sorted(ce_data, key=lambda x: int(x[1][3:8]))
        pe_data = sorted(pe_data, key=lambda x: int(x[1][3:8]))
        system("clear")
        header_ce = data_processed[0]
        header_pe = data_processed[0]
        print(f"{header_ce[0]:<10} {header_ce[1]:<10} {header_ce[2]:<10} {header_ce[3]:<10} {header_ce[4]:<10} {header_ce[5]:<10} {header_ce[6]:<10} {header_ce[7]:<10}  |  "
            f"{header_pe[0]:<10} {header_pe[1]:<10} {header_pe[2]:<10} {header_pe[3]:<10} {header_pe[4]:<10} {header_pe[5]:<10} {header_pe[6]:<10} {header_pe[7]:<10}")
        print("-" * 190)
        for ce_row, pe_row in zip(ce_data[1:], pe_data[1:]):
            if int(ce_row[1][3:8]) == high or int(ce_row[1][3:8]) == high:
                print("-" * 190)
            print(f"{ce_row[0]:<10} {ce_row[1]:<10} {ce_row[2]:<10} {ce_row[3]:<10} {ce_row[4]:<10} {ce_row[5]:<10} {ce_row[6]:<10} {ce_row[7]:<10} | "
                f"{pe_row[0]:<10} {pe_row[1]:<10} {pe_row[2]:<10} {ce_row[3]:<10} {ce_row[4]:<10} {ce_row[5]:<10} {ce_row[6]:<10} {ce_row[7]:<10}")
            if int(ce_row[1][3:8]) == high or int(ce_row[1][3:8]) == high:
                print("-" * 190)
        print("-" * 190)
    except:
        driver.quit()

while True:
    main()
    print("Updating every 60 secs...")
    sleep(60)