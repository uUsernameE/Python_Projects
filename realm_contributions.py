import smtplib
from pathlib import Path
import pyinputplus as pyip
import os
import ezsheets
import string

#email provider map with IMAP server domain name and port
#From IMAP server table 18-2 from Pg 467 of Automate the boring stuff
EMAIL_MAP = {
    "gmail": ["smtp.gmail.com", 587],
    "outlook": ["smtp-mail.outlook.com", 587],
    "yahoo": ["smtp.mail.yahoo.com", 587],
    "AT&T": ["smpt.mail.att.net", 465],
    "comcast": ["smtp.comcast.net", 587],
    "verizon": ["smtp.verizon.net", 465]
}

#phone carrier map with SMS gateways
#From SMS email gateway table 18-4 from Pg 480 of Automate the boring stuff
CARRIER_MAP = {
    "verizon": "vtext.com",
    "tmobile": "tmomail.net",
    "sprint": "messaging.sprintpcs.com",
    "at&t": "txt.att.net",
    "boost": "smsmyboostmobile.com",
    "cricket": "sms.cricketwireless.net",
    "uscellular": "email.uscc.net",
} #From https://github.com/acamso/demos/blob/master/_email/send_txt_msg.py


#######################################################################
#Check if a login file has been created. If so, read login information.
#If not, create a login file..Pg 243 of Automate the boring stuff
print("Realm Contribution Manager\nHave you already created your user?")
response = pyip.inputYesNo()
if response == "yes":
    ...
elif response == "no":
    ...


#######################################################################
#Google sheet read and manipulation..Pg 371 of Automate the boring stuff
spreadsheetID = "1-h9nx-xyS7XchJCGxQAeXEivRBXwMe6ePK1qN3WYsSw"
ss = ezsheets.Spreadsheet(spreadsheetID) #Replace elipses with the spreadsheet ID
conSheet = ss[0]
members = conSheet.getRows()

#Find which columns have the members' names, email, and phone number
emailCol, phoneCol, nameCol, carrierCol, endOfRow = None, None, None, "", None
for i, title in enumerate(members[0]):
    if title.lower() == ("email" or "emails"):
        emailCol = i
    if title.lower() == ("phone" or "phones"):
        phoneRCol = i
    if title.lower() == ("name" or "names"):
        nameCol = i
    if title.lower() == ("carrier" or "phone plan"):
        carrierCol = i
    if title == "":
        endOfRow = i
        break
del members[0]

#Determine how to find people with outstanding dues or take it from login file
'''
print("What do you want to use to determine whom needs to be notified, in lower case?\nFor example, \
      if you want to notify members that have a blank cell instead of \"Paid,\" then press enter/return.\n\
      If you want to notify members that have \"Unpaid\" marked in a cell, then type unpaid.")
'''

unpaid_key = ""
unpaid_dues = {}
for member in members:
    if member[0] != "":
        unpaid_count = 0
        for i in range(1,endOfRow):
            if member[i] == unpaid_key:
                unpaid_count += 1
                if emailCol != None:
                    unpaid_dues[member[nameCol]] = [member[emailCol]]
                if phoneCol != None:
                    unpaid_dues[member[nameCol]] = [member[phoneCol],member[carrierCol]]
        if member[nameCol] in unpaid_dues:
            unpaid_dues[member[nameCol]].append(unpaid_count)

for member in unpaid_dues:
    print(f"{member} is {unpaid_dues[member][-1]} months behind")



#communication_method = ""
user_email_host = ...
user_email = ...
user_password = ...


#######################################################################
#Sending emails and text messages..Pg 457 of Automate the boring stuff
#Connecting to an SMTP Server
#smtpObj = smtplib.SMTP(EMAIL_MAP[user_email_host][0], EMAIL_MAP[user_email_host][1])
#smtpObj.ehlo() #Sending the SMTP “Hello” Message to establish connection
#smtpObj.starttls() #Starting TLS Encryption
#smtpObj.login(user_email, user_password) #logging in to the SMTP server

#Check if the recipient wants to be contacted by phone or email
'''
if communication_method == "phone":
    for member in unpaid_dues:
        unpaid_dues[member][0] = unpaid_dues[member][0].translate({ord(c): None for c in "()- ."}) #If phone number is of the form (xxx) xxx-xxxx or xxx.xxx.xxxx, then convert to xxxxxxxxxx
        #translation_table = dict.fromkeys(map(ord, '!@#$'), None)
        #unicode_line = unicode_line.translate(translation_table)
        #From https://stackoverflow.com/questions/3939361/remove-specific-characters-from-a-string-in-python
        unpaid_dues[member][0] = f"{unpaid_dues[member][0]}@{CARRIER_MAP[unpaid_dues[member][1]]}" #Convert phone number to SMTP address
'''

#Sending an email
for member in unpaid_dues:
    smtpObj.sendmail(user_email, unpaid_dues[member][0], f"subject: Realm Reminder.\nDear {member},\nI have not \
                    recorded that a payment has been received by you to maintain the realm. Please \
                    don't forget to deliver funds to maintain our Minecraft realm or message me if \
                    there are any questions, conflicts, or concerns. Thank you, and have a great day!")
    print(f"{member} unpaid dues email was sent to {unpaid_dues[member][0]}")

#Disconnecting from the SMTP Server
#smtpObj.quit()