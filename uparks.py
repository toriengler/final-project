from bs4 import BeautifulSoup
import requests
import json
import sqlite3
from urllib.request import urlopen

CACHE_FNAME = 'parks_info.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

class HersheyPark():
    def __init__(self, ParkName='Hershey Park', ParkAddress= "No Address", ParkCity='No City', ParkState='No state', ParkZip="No Zip", Day='day unknown', Date='No Date', OpenTime='No Time', ClosedTime='No Time'):
        self.parkname=ParkName
        self.parkaddress=ParkAddress
        self.parkcity=ParkCity
        self.parkstate=ParkState
        self.parkzip=ParkZip
        self.opentime=OpenTime
        self.closedtime=ClosedTime
        self.day=Day
        self.date=Date


    def __str__(self):
        if self.opentime=="Closed":
            line= "the park is closed"
        else:
            line='the park is open at {} and closed at {}'.format(self.opentime, self.closedtime)
        return "{} : {}, {}, {}, {}, On {}, {}: {}".format(self.parkname, self.parkaddress, self.parkcity, self.parkstate, self.parkzip, self.day, self.date, line)

class HersheyRides():
    def __init__(self, RideName= 'No Name', RideDescription='No Desc', HeightMin='No Min', RideRating='No Rating', ParkRegion='Region Unknown', RatingId='No Rating', RatingDescription='No description', Star=False):
        self.ride_name=RideName
        self.ridedescription=RideDescription
        self.heights=HeightMin
        self.riderating=RideRating
        self.parkregion=ParkRegion

        self.ratingid=RatingId
        self.rating_desc=RatingDescription
        self.star=Star

    def __str__(self):
        return "{}: {}. This popular ride, with the {} rating, is located in our {} section of the park.\n The minimum height to ride is {} \n({})".format(self.ride_name, self.ridedescription, self.riderating, self.parkregion, self.heights, self.star)

def get_park_info():
    baseurl='http://www.hersheypark.com'
    parkpage=requests.get(baseurl).text
    soup= BeautifulSoup(parkpage, 'html.parser')
    park_info=soup.find_all('ul', class_='clist dropdown-links')[3]
    lst=park_info.find_all('li')
    links=[]
    for link in lst:
        links.append(link.find('a')['href'])
    links=links[:-1]
    url=make_request_using_cache(baseurl+links[5])
    soup= BeautifulSoup(parkpage, 'html.parser')

    address=soup.find_all('div', class_='container cf')[3]
    add=address.find('img').text
    addy=[]
    addy.append(add.strip().split(','))
    park_addy=addy[0][0]
    park_city=addy[0][1]
    park_zip=addy[0][2].split()[1]
    park_state=addy[0][2].split()[0]

    hours=make_request_using_cache(baseurl+links[3])
    soup= BeautifulSoup(hours, 'html.parser')
    cal=soup.find('div', class_='list-view list-content')
    dayntime=cal.find_all('li')
    days_n_times={}
    park_stuff=[]
    count=0
    for sched in dayntime:
        try:
            dates=sched.find('span', class_='day').text.split(', ')[1]
        except:
            dates=None
        try:
            day=sched.find('span', class_='day').text.split(', ')[0].strip()
        except:
            day=None
        try:
            hour=sched.find('span', class_='hours').text
            if hour.__contains__('Closed'):
                hour='Closed'
        except:
            hour=None

        days_n_times[(day, dates.strip())]=hour.strip()
        for key in days_n_times:
            park_hours=days_n_times[key]
            # print(park_hours)
            if park_hours!='Closed' and park_hours!=None:
                opentime=park_hours.split('-')[0]
                closedtime=park_hours.split('-')[1]
            else:
                opentime='Closed'
                closedtime='Closed'

        count+=1
        if count<=31:
            parkname='Hershey'
        else:
            parkname='ZooAmerica'

        park_instance=HersheyPark(ParkName=parkname, ParkAddress=park_addy, ParkCity= park_city, ParkState=park_state, ParkZip=park_zip, Day=day, Date=dates, OpenTime=opentime, ClosedTime=closedtime)
        park_stuff.append(park_instance)
    return park_stuff

def get_soup():
    ride_url='http://www.hersheypark.com/rides/search.php'
    ride_site=requests.get(ride_url).text
    soup= BeautifulSoup(ride_site, 'html.parser')
    return soup

# get ride names and return it
def get_ride_names():
    soup = get_soup()
    ride_info= soup.find('ul', id='rides-list')
    ifstate=ride_info.find_all('p', class_="ride-title")
    names=[]
    for i in ifstate:
        names.append(i.string)
    return names

def get_ride_info():
    # call ride names function and return list of ride instances
    soup = get_soup()
    ride_info= soup.find('ul', id='rides-list')
    links=ride_info.find_all('li')
    list_links=[]
    for l in links:
        link=l.find('a')['href']
        list_links.append(link)
    names = get_ride_names()
    i = iter(names)
    j = iter(list_links)
    link_dict = list(zip(i, j))
    request_urls=[]
    for x in link_dict:
        request_urls.append(x[1])
    baseurl='http://www.hersheypark.com/'
    ride_stuff=[]
    for request_url in request_urls:
        res=make_request_using_cache(baseurl+request_url)
        soup= BeautifulSoup(res, 'html.parser')
        try:
            name=soup.find('h1', class_='content-h1').text
        except:
            print('No ride name')
        ride_info= soup.find('div', class_='rides-detail-sec1 rides-detail-sec')
        if ride_info!=None:
            try:
                _desc= ride_info.find_all('div', class_='romance-copy')
                for p in _desc:
                    ride_desc=p.text.strip().split('\n')[0]
            except:
                ride_desc=None
            more_dets=soup.find('div', class_='rides-detail-sec3 rides-detail-sec')
            heights=more_dets.find('ul', class_='clist cf height-wrap')
        if heights!=None:
            try:
                shortest_height=heights.find_all('li')[-1].text    # string
                if shortest_height[-1]=='*':
                    star=True
                else:
                    star=False
            except:
                shortest_height=None
                star=False
            try:
                ride_rat=more_dets.find_all('h3')[1].string
                ride_rating=ride_rat.split('- ')[1]
            except: ride_rating=None
            num=more_dets.find_all('img')
            try:
                for i in num:
                    rating_id=i['alt'].split('-')[0]
                    rating_description=i.string.strip()
            except:
                rating_id=None
                rating_description=None
            try:
                park_region=more_dets.find_all('div', class_='additional-info')[1]
                park_region=park_region.find('li').string
            except:
                park_region=None
        ride_instance=HersheyRides(RideName= name, RideDescription=ride_desc, HeightMin=shortest_height, RideRating=ride_rating, ParkRegion=park_region, RatingId=rating_id, RatingDescription=rating_description, Star=star)
        ride_stuff.append(ride_instance)
    return ride_stuff

DBNAME='HersheyPark.db'

def init_db():
    try:
        conn = sqlite3.connect(DBNAME)
        cur=conn.cursor()
    except:
        print('could not connect')
    statement = '''
        DROP TABLE IF EXISTS 'Rides';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Ratings';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Hours';
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE 'Rides' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'RideName' TEXT ,
                'RideDescription' TEXT,
                'HeightMin' TEXT,
                'RideRating' TEXT,
                'RideRatingID' TEXT,
                'ParkRegion' TEXT,
                'SupervisionRequired' BOOLEAN);
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE 'Ratings' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'RatingName' TEXT ,
            'RatingDescription' TEXT
        );
    '''
    cur.execute(statement)
    conn.commit()
    statement = '''
        CREATE TABLE 'Hours' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Weekday' TEXT,
            'Dates' TEXT,
            'ClosedTime' TEXT,
            'OpenTime' TEXT,
            'ParkName' TEXT
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()

def insert_info():
    rides = get_ride_info()
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    for ride in rides:
        insertion= (None, ride.ride_name, ride.ridedescription, ride.heights, ride.riderating, ride.ratingid, ride.parkregion, ride.star)
        statement = 'INSERT INTO "Rides" '
        statement += 'VALUES (?, ?, ?, ? ,?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()

    parks=get_park_info()
    for park in parks:
        insertion=(None, park.day, park.date, park.opentime, park.closedtime, park.parkname)
        statement = 'INSERT INTO "Hours" '
        statement += 'VALUES (?, ?, ?, ?, ?,?)'
        cur.execute(statement, insertion)
    conn.commit()

    Ratingnames=['Childrens Ride', 'Mild Thrill Ride', 'Moderate Thrill Ride', 'High Thrill Ride', 'Aggressive Thrill Ride']
    descriptions=[ "This is a low-speed, gentle ride intended for young children and may accommodate chaperones where permitted."
    ,"This is a low to medium speed ride with expected changes in elevation and speed. This ride may require some rider body control and is not intended for unaccompanied toddlers or very young children.", "This is a medium speed ride where riders may experience unexpected changes in elevation and speed. This ride may contain moderate twists, turns, bumps, spins, and loops, and may require some rider body control."
    ,"This is a fast-paced ride experience with unexpected changes in speed, direction, and/or elevation. This ride may contain significant twists, turns, bumps, spins, and loops, and requires rider full body control"
    ,"This is a high-speed experience. Riders will experience many unexpected, rapid changes in speed, direction, and/or elevation and requires rider full body control. This ride is not recommended for guests with physical, cognitive, and/or medical limitations."]
    i = iter(Ratingnames)
    j = iter(descriptions)
    ratings = list(zip(i, j))
    for rat in ratings:
        rating=rat[0]
        des=rat[1]
        insertion= (None, rating, des)
        statement="INSERT INTO 'Ratings'"
        statement+= "VALUES (?, ?, ?)"
        cur.execute(statement, insertion)
    conn.commit()

if __name__ == '__main__':
    init_db()
    insert_info()
