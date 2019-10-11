import pandas as pd

hostGroup={}
contactGroup={}
def bulkHostCheckAsServices(xlsxFile):

    hosts=[]
    df = pd.read_excel(xlsxFile, header=0)

    excelColumnName = "Host Name"
    excelAddressName = "IP"
    excelGroupName = "Host Group"
    excelContactName = "Contact Group"
    excelLatitude = "Latitude"
    excelLongitude = "Longitude"


    for index, row in df.iterrows():
        # Columns in excel
        try:
            Name = row[excelColumnName]
            IP = row[excelAddressName]
            Group = row[excelGroupName]
            Contact = row[excelContactName]
            Latitude = row[excelLatitude]
            Longitude = row[excelLongitude]

            hosts.append({"Name":Name.rstrip(),"IP":IP.rstrip(),"Host Group":Group.rstrip(),"Contact Group":Contact.rstrip(),"Latitude":Latitude,"Longitude":Longitude})
        except BaseException as e:
            logger.error('Failed importing: ' + str(e))
    return hosts

#bulkHostCheckAsServices('FILE.xlsx')

def groups(xlsxFile):

    
    df = pd.read_excel(xlsxFile, header=0)
    

    excelColumnName = "Host Name"
    excelAddressName = "IP"
    excelGroupName = "Host Group"
    excelContactName = "Contact Group"
    #excelLatitude = "Latitude"
    #excelLongitude = "Longitude"

    Services = True
    for index, row in df.iterrows():
        # Columns in excel
        try:
            Name = row[excelColumnName]
            IP = row[excelAddressName]
            Group = row[excelGroupName]
            Contact = row[excelContactName]
            #Latitude = row[excelLatitude]
            #Longitude = row[excelLongitude]

            if Group in hostGroup:
                hostGroup[Group].append(Name)
            else:
                hostGroup[Group]=[Name]

            if Contact in contactGroup:
                contactGroup[Contact].append(Name)
            else:
                contactGroup[Contact]=[Name]
        except BaseException as e:
            logger.error('Failed importing: ' + str(e))

    return hostGroup,contactGroup


#print(groups('FILE.xlsx'))
















