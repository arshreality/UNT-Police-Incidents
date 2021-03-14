# importing required modules 
import PyPDF2 
import geopy
from geopy.geocoders import Nominatim
import haversine as hs
from haversine import Unit
import io
import requests
import pandas as pd

abb_dict = {
  "AGG":"Aggravated",
  "ALCH":"Alcohol",
  "APPREH":"Apprehension",
  "BEV":"Beverage",
  "BURG":"Burglary",
  "CONSUMP":"Consumption",
  "CONT":"Container",
  "CRIM":"Criminal",
  "CS":"Controlled Substance",
  "CSA":"Campus Security Authority",
  "D.L.":"Driver's License",
  "D.W.I.":"Driving While Intoxicated",
  "DEL":"	Delivery",
  "DISP":"Display",
  "DWLS":"Driving While License Suspended",
  "ENG":"Engaging",
  "EVID":"Evidence",
  "FABR":"Fabricate",
  "FEL":"Felony",
  "FICT":"Ficticious",
  "FMFR":"Fail to Maintain Financial Responsibility",
  "FSRA":"Fail to Stop / Render Aid",
  "FV":"Family Violence",
  "Govt Recd":"Government Record",
  "INFLU":"Influence",
  "INJ":"Injury",
  "LIC":"License",
  "MISCH":"Mischief",
  "MISD":"Misdemeanor",
  "MJ":"Marijuana",
  "O/":"Over",
  "OA":"Outside Agency",
  "ORG":"Organized",
  "Oz":"Ounce",
  "PG":"Penalty Group",
  "POSS":"Possession",
  "U/":"Under",
  "UUMV":"Unauthorized Use of Motor Vehicle",
  "VEH":"Vehicle",
  "W/":"With",
  "Clred": "Cleared"
}

# create empty dataframe with columns
columns = ['Nature', 'Case', 'Reported', 'Occurred', 'Location', 'Disposition', 'Distance', 'Latitude', 'Longitude', 'Speech Output', 'Date']

df = pd.DataFrame(columns=columns)


def get_incidents():
    loc2 = (33.212031, -97.151035)
    # url = 'https://police.unt.edu/sites/default/files/dailylog.pdf'

    # r = requests.get(url)
    # f = io.BytesIO(r.content)
    
    # creating a pdf file object 
    f = open('dailylog.pdf', 'rb') 
      
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(f) 
      
    # printing number of pages in pdf file 
    numOfPages = (pdfReader.numPages) 
    
    all_words = []

    for page in range(numOfPages):
      # creating a page object 
      pageObj = pdfReader.getPage(page) 
        
      # extracting text from page 
      text = (pageObj.extractText()) 
      arr = text.split("\n")  

      # creating NL strings
      i = 0
      for word in arr:
          if word == "Disposition":
              break
          else:
              i += 1
      
      all_words += arr[i + 1:]
    
    string_arr = []
    locator = Nominatim(user_agent="myGeocoder")
    
    for word in all_words:
        if word == '':
          continue

        string_arr.append(word)
        if len(string_arr) == 6:
            temp = "{} was filed with the case number {} was reported on {} at {}. The disposition was {}. ".format(string_arr[0], string_arr[1], string_arr[2], string_arr[4], string_arr[5])
            location = locator.geocode(string_arr[4])
            if location is not None:
                loc1 = (location.latitude, location.longitude)
                
                distance = hs.haversine(loc1, loc2 ,unit=Unit.MILES)
                temp += " The incident was about {} miles away from you.".format('%s' % float('%.2g' % distance))
                if distance < 0.5:
                    temp += " Since the incident is less than half a mile away, you might want to take appropriate precautions. "
            else:
              index = string_arr[4].index(",")
              location = locator.geocode(string_arr[4][index + 2:])
              if location is not None:
                loc1 = (location.latitude, location.longitude)
                loc2 = (33.212031, -97.151035)
                distance = hs.haversine(loc1, loc2 ,unit=Unit.MILES)
              else:
                distance  = -1
                loc1 = (-1,-1)
            
            string_arr.append(distance)
            string_arr.append(loc1[0])
            string_arr.append(loc1[1])
            for abb, word in abb_dict.items():
              temp = temp.replace(abb, word)
            string_arr.append(temp)
            string_arr.append(string_arr[2].split(' ')[0])
            df.loc[len(df)] = string_arr
            string_arr.clear()
            continue
        
        if "     " in word:
            string_arr.clear()
            continue
        
    return string_arr


incidents = get_incidents()
print(df)

df.to_csv('incidents.csv')