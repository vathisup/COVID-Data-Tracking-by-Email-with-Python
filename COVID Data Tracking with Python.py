import smtplib as sm
import datetime as dat
import requests

# Please enter the Email and its password into 'username' and 'password' variable
# This app utilizes Google's SMTP server.
username = ''
password = ''
smtp_server = 'smtp.gmail.com'

now = dat.datetime.now()
full_time=now.strftime("%d, %m, %Y")
full_timeTwo=now.strftime("%Y-%m-%d 00:00:00")


initialTime=''
endTime=''
latestData=[]
specificData=[]

confirmed_case=''
total_death=''
total_recovered=''
total_active=''
date=''
specInfo=''
emptyList=[]
emptyListTwo=''
country=''
countryTwo=''
province=''
provinceTwo=''
#the variable 'country' and 'province' are there to make the text sent via email look nicer



class countryData:
    def __init__(self, country):
        self.country=countryChoice
        
    
    
    def getLatestData(self):
        countryData.clearData(self)
        
        global confirmed_case, total_death, total_active, total_recovered, date, country #I called these variables "global" to make sure it updates the value for the variable outside the class.
    
        latestData=requests.get(f"https://api.covid19api.com/total/country/{self.country}").json() 
        #I used the API with "total" to make sure to get the latest TOTAL data for all countries. Countries like china is divided into provinces's data each day. 
        #If i used the api professor used, it will only return the last province's data in china and not the entire country's data on the latest day.

        if(latestData=={"message": "Not Found"}): #If the user were to input an INVALID country.
            print("Country not found. Please restart the application and try again.")
            
        else:
            confirmed_case=latestData[-1]['Confirmed']
            total_death=latestData[-1]['Deaths']
            total_recovered=latestData[-1]['Recovered']
            total_active=latestData[-1]['Active']
            date=latestData[-1]['Date']
            country=latestData[-1]['Country']
            print('============================================')
            print(f'''Up until {date} {country} has the following covid data:
    - Confirmed Cases: {confirmed_case}
    - Total Deaths: {total_death}
    - Total Recovered: {total_recovered}
    - Active Cases: {total_active}
    ''')
            print('============================================')
    
        
    def clearData(self): #I don't know if this is needed but I don't want to delete it since I was afraid it might affect the application. So i leave it there, but its original purpose is to reset the variable's value.
        global confirmed_case, total_death, total_active, total_recovered
        confirmed_case=None
        total_death=None
        total_recovered=None
        total_active=None

class specificCountryData:
    def __init__(self, country, initialTime, endTime):
        self.country=countryChoice
        self.iniTime=initialTime
        self.endTime=endTime

    def clearData(self):
        global confirmed_case, total_death, total_active, total_recovered
        confirmed_case=None
        total_death=None
        total_recovered=None
        total_active=None

    def getSpecificData(self):
        specificCountryData.clearData(self)
        global confirmed_case, total_death, total_active, total_recovered, specInfo, emptyList, emptyListTwo, countryTwo, provinceTwo, date
        
        #I called these variables "global" to make sure it updates the value for the variable outside the class.

        specificData=requests.get(f'https://api.covid19api.com/country/{self.country}?from={self.iniTime}&to={self.endTime}').json()

        #Some countries are divided into provinces when they give data each day such as CHINA. To make sure user gets all "status" with "time filter", i decided to include all provinces when providing info. 

        if(specificData=={"message": "Not Found"}):
            print("City not found or error in other inputs. Please restart the application and try again.")
        else:
            for i in range(len(specificData)):
                
                confirmed_case=specificData[i]['Confirmed']
                total_death=specificData[i]['Deaths']
                total_recovered=specificData[i]['Recovered']
                total_active=specificData[i]['Active']
                date=(specificData[i]['Date'])
                countryTwo=specificData[i]['Country']
                provinceTwo=specificData[i]['Province']
                
                if(provinceTwo==""):#This is for countries that gives out data for entire country instead of data by provinces.
                    specInfo=f''' 

            As of {date}, {countryTwo} has the following covid data:
    - Confirmed Cases: {confirmed_case}
    - Total Deaths: {total_death}
    - Total Recovered: {total_recovered}
    - Active Cases: {total_active}
    '''
                else:
                    specInfo=f''' 

                As of {date}, {provinceTwo} in {countryTwo} has the following covid data:
        - Confirmed Cases: {confirmed_case}
        - Total Deaths: {total_death}
        - Total Recovered: {total_recovered}
        - Active Cases: {total_active}
        '''
                print('============================================')
                print(specInfo)
                
                emptyList.append(specInfo) #I used the variable "specInfo" to store the info per iteration. Then, I append it into emptyList which is later joined together to become a big string and send the string.

                print('============================================')
        








class sendEmail:
    def __init__(self, receiver):
        self.receiver=receiver
        
    
    def sendLatestMail(self):
        global username, password, date, country, confirmed_case, total_death, total_recovered, total_active
        with sm.SMTP(smtp_server, 587) as conn:
            conn.starttls()
            conn.login(username, password)
            conn.sendmail(username, self.receiver, f'''Subject: {country}'s Covid data up until {date}\n\n 

        As of {date}, {country} has the following covid data:
- Confirmed Cases: {confirmed_case}
- Total Deaths: {total_death}
- Total Recovered: {total_recovered}
- Active Cases: {total_active}
''')

    def sendSpecificMail(self):
        global username, password, date, emptyListTwo, emptyList, provinceTwo

        emptyListTwo=("\n").join(emptyList) #This is where I joined the list of time filtered data.

        with sm.SMTP(smtp_server, 587) as conn:
            conn.starttls()
            conn.login(username, password)
            conn.sendmail(username, self.receiver, f"Subject: {countryTwo}'s Covid data up until {date}\n\n {emptyListTwo}")
loopOne=True
loopTwo=True

print(f"Welcome to COVID's data tracking centre. \n")

while(loopOne):
    while(loopTwo):
        countryChoice=input(f"Please enter the country to want to get data on: ")
        receiver=input(f"Please input the email of your reciever: ")
        userChoice=input(f"Press 1 to get the latest data, press 2 to get data from a specific period of time: ")
        if(userChoice=="1"):
            chosenCountry=countryData(countryChoice)
            chosenCountry.getLatestData()

            date=date.replace("T00:00:00Z","") #this is to remove "T00:00:00Z" from the date part when it is sent to user.
            
            sendOrNot=input(f"Is this what you want to send? Y/N: ")
            
            if(sendOrNot=="Y" or sendOrNot=="y"):
                
                sendMail=sendEmail(receiver)
                sendMail.sendLatestMail()
                print("Sent.")

            elif(sendOrNot=="N" or sendOrNot=="n"):
                print(f"Please restart the application to re-enter.")
                break
        elif(userChoice=="2"):
            initialTime=input(f"Please input your starting date in (Y-Month-Day. Ex: 2021-11-01): ")
            endTime=input(f"Please input your ending date in (Y-Month-Day. Ex: 2021-11-03): ")

            timeOne=initialTime
            timeTwo=endTime



            splitTimeOne=timeOne.split("-")
            splitTimeTwo=timeTwo.split("-")

            
            if(len(splitTimeOne)!=3 or len(splitTimeTwo)!=3): #for when the user failed to user "-" in the format
                print("Wrong time input format. Please restart the application to try again.")
                break

            xOne=int(splitTimeOne[0])
            xTwo=int(splitTimeOne[1])
            xThree=int(splitTimeOne[2])

            yOne=int(splitTimeTwo[0])
            yTwo=int(splitTimeTwo[1])
            yThree=int(splitTimeTwo[2])

            if(int(splitTimeTwo[0])<2020 or int(splitTimeTwo[1])>12 or int(splitTimeTwo[2])>31 or int(splitTimeOne[0])<2020 or int(splitTimeOne[1])>12 or int(splitTimeOne[2])>31): #for when the user uses an incorrect time format.
                print("Time input is out of range as data before 2020 doesn't exist or other problems occured. Please restart the application and try again.")
                break


            x=dat.datetime(xOne,xTwo,xThree)
            y=dat.datetime(yOne,yTwo,yThree)


            if(x<y): #the initialTime must be BEFORE the endTime.
                
                

    
                chosenCountryTwo=specificCountryData(countryChoice, initialTime, endTime)
                chosenCountryTwo.getSpecificData()

                date=date.replace("T00:00:00Z","")

                sendOrNotTwo=input(f"Is this what you want to send? Y/N: ")
                if(sendOrNotTwo=="Y" or sendOrNotTwo=="y"):
                    
                    sendMailTwo=sendEmail(receiver)
                    sendMailTwo.sendSpecificMail()
                    emptyListTwo=''
                    emptyList.clear()
                    print("Sent.")


                elif(sendOrNotTwo=="N" or sendOrNotTwo=="n"):
                    print(f"Please restart the application to re-enter.")
                    break
            else:
                print("Wrong Time Format or other problems occured. Please restart the app and try again.")
                break
        else: 
            print("INVALID INPUT. Please restart the application to start again.")
            break

        loopTwo=False

    restart=input('Do you want to restart the application? Y/N: ')
    if(restart=="Y" or restart=="y"):
        loopTwo=True
    elif(restart=="N" or restart=="n"):
        print('Exiting the application ...')
        loopTwo=False
        loopOne=False
    else:
        print("Invalid Input. Please try again.")
        loopTwo=False
