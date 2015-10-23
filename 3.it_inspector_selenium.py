# peso pag : internet.tre.it =  1540 kB dagli strumenti per svilupaptore di firefox
# posso escludere img dal download ?
# orario esecuzione 8:00 - 23:30
# avviso per email
# TODO avviso solo se ip/hostname in lan. Ha senso quando lo script non sara' piu' in locale sul mio pc.
import smtplib
import string
#from bs4 import BeautifulSoup'
import sys, time
from datetime import datetime
#import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.keys import Keys

# ---- the alarm activation value
alarmValue = 500

host = "http://internet.tre.it"
#host = "http://ac3.tre.it/133/index.jsp?uri=/133/controllo-costi.jsp"

# ---- email settings
SUBJECT = "Watch out your internet limits!"
TO      = "bla@bla.com"
FROM    = "bla@bla.com"
gmail_user  = FROM
gmail_pwd   = "123stella"


# ---- time check ---
actualTime = datetime.now()
morning = actualTime.replace(hour=8, minute=0, second=0)
night   = actualTime.replace(hour=23, minute=0, second=0)

while (actualTime > morning and actualTime < night):

    ## ---------- http://jeanphix.me/Ghost.py/ evita di aprire la finestra!
    driver = webdriver.Firefox()
    driver.get( host)
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "spanRight"))
        )
    finally:
        MB = element.text
        driver.quit()

    #MB = driver.find_element_by_class_name('spanRight').text
    MB = MB.split()[0]

    #print "\n I found this: {} \n".format( MB )

    #MB = soup.find('div','box_Note').text.split()[2]   # ac3.it
    #MB = soup.find('span','spanRight').text.split()[0]  # internet.tre.it
    #MB = MB.encode('ascii','ignore')
    actualTime = datetime.now().strftime("%d-%b %H:%M:%S")

    if int(MB) < alarmValue:
        text =  " {} \tHey! Slow down! Only {} MB are left! \n".format(actualTime, MB)
        # ----  send email
        print text
        print " \tSending email.."
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
            print ' \temail successfully sent!\n'
        except:
            # ----- email fail
            print " \tnope.. :(\n {} \n\t".format(sys.exc_info()[0] )
    else:
        print " {} \tNp broh, still {} MB left. \n".format(actualTime, MB)

    #driver.close()

    # wait 30 min
    timeToWait = 60*30
    print " Next check in {} min \n".format( timeToWait )
    time.sleep( timeToWait )
    actualTime = datetime.now()
