#! /usr/bin/python3

# By Architrixs May 9, 2021
# getFunds.py

import bs4
import requests
import sys

def help():
    sys.stdout.write("""Usage :-
    $ ./getFunds [Arg1: filename.txt] [optional Arg] [Arg2: outputFileName.csv]

    Optional Argument:  -ft   , gets data from https://markets.ft.com
                        -br   , gets data from https://www.boursorama.com default

    $ ./getFunds --help or -h		# Show usage

    Example: $ ./getFunds.py fundcodes.txt -ft funds_ft.csv
             $ ./getFunds.py fundcodes.txt funds_br.csv\n""")
    exit()

def getFunds():
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        output_file_name = sys.argv[-1]
    with open(file_name, 'r') as file:
        fund_codes = file.readlines()
    print("Getting ISIN codes from file...")
    isin_codes=[i.strip() for i in fund_codes]

    if sys.argv[-2] =='-ft':
        url = 'https://markets.ft.com/data/funds/tearsheet/summary?s='
    else:
        url = 'https://www.boursorama.com/bourse/opcvm/recherche/?fastFundSearch[code]='


    #print(isin_codes)
    name_list = []
    price_list = []

    print("Getting Prices...\nPlease Wait")
    for i in range(len(isin_codes)):
        # From www.boursorama.com
        if sys.argv[-2] =='-ft':
            res = requests.get(url+ isin_codes[i] + ':EUR', headers={'User-Agent': 'Mozilla/5.0'})
        else:
            res = requests.get(url+ isin_codes[i], headers={'User-Agent': 'Mozilla/5.0'})
        
        #Checking for Bad download
        try:
            res.raise_for_status()
        except Exception as exc:
            print("There was a problem: %s" % (exc))
        
        #making soup

        soup_res = bs4.BeautifulSoup(res.text, 'html.parser')
        
        if sys.argv[-2] =='-ft':
            name = soup_res.find('h1', {'class':'mod-tearsheet-overview__header__name mod-tearsheet-overview__header__name--large'})
            price = soup_res.find('span',{'class':'mod-ui-data-list__value'})
            #print(name.text,price.text)
            name_list.append(name.text)
            price_list.append(price.text.replace(',', ''))

        else:
            name = soup_res.find_all('a',{'class' : 'c-link c-link--animated'})
            price = soup_res.find_all('td',{'class' : 'c-table__cell c-table__cell--dotted'})
            #print(name[2].text, ''.join(price[1].text.split()))
            name_list.append(name[2].text)
            price_list.append(''.join(price[1].text.split()))


    with open(output_file_name, 'w', encoding='utf-8') as f:
        print('Saving File as', output_file_name)
        for code, name, price in zip(isin_codes, name_list, price_list):
            f.write(code + ", " + name + ", " + price + "\n")
        #wr.writerow(price_list)

def main():
    if len(sys.argv)==1 or sys.argv[1]== '--help' or sys.argv[1]=='-h' or len(sys.argv)>4:
        help()
    else:
        getFunds()

if __name__=="__main__": 
    main()
