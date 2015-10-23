# peso pag : internet.tre.it =  1540 kB dagli strumenti per svilupaptore di firefox
# posso escludere img dal download ?
# orario esecuzione 8:00 - 23:30
# avviso per email
# TODO avviso solo se ip/hostname in lan. Ha senso quando lo script non sara' piu' in locale sul mio pc.
from __future__ import print_function
import smtplib
import string
import sys, time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---- the alarm activation value
alarmValue = 500

host = "http://internet.tre.it"

# ---- email settings
EMAIL_SUBJECT  = "Watch out your internet limits!"
EMAIL_TO       = "bla@bla.com"
EMAIL_FROM     = "bla@bla.com"
SMTP_SERVER    = "smtp.gmail.com"
SMTP_PORT      = 587
EMAIL_USERNAME = EMAIL_FROM
EMAIL_PASSWORD = "123stella"

# ---- time check ---
actualTime = datetime.now()
morning = actualTime.replace(hour=8, minute=0, second=0)
night   = actualTime.replace(hour=23, minute=0, second=0)

while (actualTime > morning and actualTime < night):

    ## ---------- http://jeanphix.me/Ghost.py/ evita di aprire la finestra!
    driver = webdriver.Firefox()
    driver.get(host)
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "spanRight"))
        )
    finally:
        MB = element.text.split()[0]
        driver.quit()

    actualTime = datetime.now().strftime("%d-%b %H:%M:%S")

    if int(MB) < alarmValue:
        text =  "{} \tHey! Slow down! Only {} MB are left! \n".format(actualTime, MB)
        # ----  send email
        print (text)
        print ('\tSending email..')

        BODY = string.join((
                "From: %s" % FROM,
                "To: %s" % TO,
                "Subject: %s" % SUBJECT ,
                "",
                text
                ), "\r\n")
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.ehlo()
            server.starttls()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.sendmail(FROM, TO, BODY)
            server.close()
            print ('\temail successfully sent!\n')
        except:
            # ----- email fail
            print ('\tnope.. :(\n {} \n\t'.format(sys.exc_info()[0])
    else:
        print ('{} \tNp broh, still {} MB left. \n'.format(actualTime, MB)

    # wait 30 min
    timeToWait = 60*30
    print ('Next check in {} min \n'.format(timeToWait))
    time.sleep( timeToWait )
    actualTime = datetime.now()
