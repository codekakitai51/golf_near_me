from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
from datetime import datetime, date

app = Flask(__name__)

@app.route('/', methods = ["GET" , "POST"])
def index():
   if request.method == 'POST':
    dateForBellevue = request.form['date']
    timeFromHtml = request.form['time']
    driver = webdriver.Chrome()

    # scraping from Bellevue Golf Coarse ------------------
    driver.get("https://premier.cps.golf/Bellevuev3/(S(yjrsedugqisw1lyt5zs03cdr))/Home/WidgetView")

    ## dateForBellevue
    dateField = driver.find_element(by="id", value="FromDate")
    driver.execute_script("arguments[0].removeAttribute('readonly')", dateField)
    dateField.clear()
    dateField.send_keys(dateForBellevue)

    ## time
    timeField = driver.find_element(by="id", value="StartTimeDropDown")
    select = Select(timeField)
    select.select_by_value(timeFromHtml)   

    submitBtn = driver.find_element(by="id", value="btnSubmit")
    submitBtn.click()

    timeArrBellevue = []
    for h3tag in driver.find_elements(by="xpath", value="//div/div/h3"):
        if not h3tag.text: continue
        timeArrBellevue.append(h3tag.text)
    if len(timeArrBellevue) == 0:
       timeArrBellevue.append('there is no spot')
    # ------------------ scraping from Bellevue Golf Coarse 

    # scraping from Willows ---------------------
    driver.get("https://www.willowsrun.com/Book-a-Tee-Time")

    ## date 
    now = date.today()
    now_datetime = datetime.combine(now, datetime.min.time())
    tempDay = request.form['date']
    willowYear = int(tempDay[6:10])
    willowMonth = int(tempDay[1] if tempDay[0] == "0" else tempDay[0:2])
    willowDate = int(tempDay[4] if tempDay[3] == "0" else tempDay[3:5])
    sellectedDate = datetime(willowYear, willowMonth, willowDate)
    if str(sellectedDate - now_datetime)[1] == " " and int(str(sellectedDate - now_datetime)[0]) <= 7:
        dayDifferencial = int(str(sellectedDate - now_datetime)[0])

        if dayDifferencial == -1: print("call them and check availability")
        dateClick = driver.find_element(by="id", value="customcaleder_" + str(dayDifferencial))
        dateClick.click()

        ##time
        if len(timeFromHtml) == 4:
            s1 = timeFromHtml[1]
            s2 = timeFromHtml[2:]
            timeForWillow = "0" + s1 + ":00 " + s2
        else:
            s1 = timeFromHtml[1:3]
            s2 = timeFromHtml[3:]
            timeForWillow = s1 + ":00 " + s2       
        timeField = driver.find_element(by="id", value="dnn_ctr5398_DefaultView_ctl01_cmbHour")

        select = Select(timeField)
        select.select_by_value(timeForWillow) 
        time.sleep(8)
        timeArrWillow = []
        for timeDiv in driver.find_elements(by="xpath", value="//td/div/div"):
            if len(timeDiv.text) <= 1: continue
            else: timeArrWillow.append(timeDiv.text[11:])
            
        if not timeArrWillow:
            timeArrWillow.append('there is no spot!')

    else: timeArrWillow = "selected day is too early!"
    # --------------------- scraping from Willows

    return render_template('index.html', timeArrBellevue=timeArrBellevue, timeArrWillow=timeArrWillow, timeFromHtml=timeFromHtml, dateForBellevue=dateForBellevue)
   else: return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5500)