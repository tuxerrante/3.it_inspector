# NON FUNZIONA !
#
# orario esecuzione 8:00 - 23:30
# avviso per email?
# avviso solo se ip/hostname in lan. Ha senso quando lo script non sara' piu'
#   in locale sul mio pc.

# http://www.crummy.com/software/BeautifulSoup/bs4/doc/
# il parser lxml e' piu' veloce di quello integrato html.parser:
#    BeautifulSoup(markup, "lxml")
import smtplib
import string
from bs4 import BeautifulSoup
import sys
from datetime import datetime
import json
import requests
#import codecs

# the alarm activation value
alarmValue = 500



host = "http://internet.tre.it"
#host = "http://ac3.tre.it/133/index.jsp?uri=/133/controllo-costi.jsp"
headers = {"Host":"internet.tre.it",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"it-IT,it;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":"gzip, deflate",
             "DNT":"1",
            "Cookie": "__gads=ID=2f2dac4b04660e5f:T=1444225089:S=ALNI_MYfK2ppMc9TdEq7FB5AE_emWAs8ZA; _ga=GA1.3.285244798.1444225090; __utma=246631489.1283562247.1445359621.1445376258.1445421485.4; __utmz=246631489.1445359621.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=246631489; ASP.NET_SessionId=5pnmcxb4sgovz3ip4lsgfefj; pageVisit=ffdf96dab2314d78af7cdc0175fed691; cookiesAccepted=1",
            "Connection":  "keep-alive",
             "Cache-Control":"max-age=0"
            }
# --- urlib and requests don't work!            
# ------------ Selenium ? http://selenium-python.readthedocs.org/en/latest/getting-started.html
urlOpened  = requests.get( host, headers=headers) #, allow_redirects=False)
page = urlOpened.text

#with open("ac3.it.html", 'w') as f:
with open("internet.tre.it.html", 'w') as f:
    f.write( page.encode('ascii', 'ignore') )

soup = BeautifulSoup( page , 'lxml')
#print
#print (soup.prettify())

#   email settings
SUBJECT = "Watch out your internet limits!"
TO      = "asd@asd.it"
FROM    = "asd@asd.it"
gmail_user  = FROM
gmail_pwd   = "pippo"

# time check ...


#MB = soup.find('div','box_Note').text.split()[2]   # ac3.it
MB = soup.find('span','spanRight').text.split()[0]  # internet.tre.it
#MB = MB.encode('ascii','ignore')
time = datetime.now().strftime("%d-%b %H:%M:%S")

if int(MB) < alarmValue:
    text =  "{}  Hey! Slow down! Only {} MB are left! \n".format(time, MB)
    #   send email
    print text
    print "  Sending email.."
    BODY = string.join((
            "From: %s" % FROM,
            "To: %s" % TO,
            "Subject: %s" % SUBJECT ,
            "",
            text
            ), "\r\n")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, BODY)
        server.close()
        print '   email successfully sent!\n'
    except:
        print "   nope.. :(\n {} \n\t".format(sys.exc_info()[0] )
else:
    print " time: Np broh, still {} MB left. \n".format(MB)

urlOpened.close()

# wait 30 min
