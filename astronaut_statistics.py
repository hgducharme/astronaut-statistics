from bs4 import BeautifulSoup
import requests, re, json

# for astronaut in astronauts, populate a data structure with degrees, age accepted into astronaut program, military experience, etc.

# Create a requests Session because we are making multiple requests to nasa.gov.
session = requests.Session()

#def find_every_instance(dataSet, word):
    #regex = re.compile('(?:'+'\/astronauts\/biographies'+')(?:[^\"]+)')
    #return re.findall(regex, dataSet)

class Astronaut:
    def __init__(self, name, biography):
        self.name = name 
        self.biography = biography

    def get_education():
        bachelors = 5 # TODO: Change this to the string found in the biography.
        self.education = {'bachelors': [bachelors]}

def get_active_astronauts():     
    # The links on the active astronuats page are generated using javascript, so call the JSON URL.
    # active_astronauts_page = session.get('https://www.nasa.gov/api/1/record/node/376740.json', timeout = 0.5) UNCOMMENT
    # activeAstronautsJSON = active_astronauts_page.json() UNCOMMENT

    # For right now, just use data from the downloaded JSON file so we don't make too many requests to NASA.gov.
    with open("376740.json") as json_file:
        json_data = json.load(json_file)

    # The body of the JSON file is where all the astronaut names and links are stored.
    #landingPageBody = activeAstronautsJSON['landingPage']['body'] UNCOMMENT
    landingPageBody = json_data['landingPage']['body'] 
    soup = BeautifulSoup(landingPageBody, 'html.parser')

    # Initialize active astronauts dictionary.
    activeAstronauts = {}

    # Find all links that contain a string; aka find all astronaut names and their respective webpage link.
    astronauts = soup.find_all('a',string=True)

    # For every link and name in 
    for k, link in enumerate(astronauts):
        name = link.string
        webPageLink = link['href']
    
        # If the link is not already a full URL, make it a full URL.
        if link['href'][0] == '/':
            webPageLink = 'https://www.nasa.gov' + link['href'] + '/biography'

        # Find link to actual biography page on the astronaut's web page.
        webPageHTML = session.get(webPageLink)
        webPageSoup = BeautifulSoup(webPageHTML.content, 'html.parser')

        #if k == len(astronauts)-1:
        print(webPageSoup.find_all('p'))


        activeAstronauts[name] = Astronaut(name, webPageLink)
    
    #for key, value in activeAstronauts.items():
        #print(value.name, value.biography)


    '''
    # Each astronaut has an HTML section that looks like:
    # <p><a href="/astronauts/biographies/joseph-m-acaba">Acaba, Joseph M.</a> <a href="[twitter link]"><img align="middle" alt="Twitter" src="[image source]" /></a></p>
    
    # Link to bio looks like: /astronauts/biographies/[astronaut-name]
    regex = re.compile('(?:\/astronauts\/biographies)(?:[^\"]+)')
    # Find every instance in the landing-page body that matches the regex.
    activeAstronautBios = re.findall(regex, landingPageBody)

    # Astronaut's name looks like: >lastName, firstName Initial.<
    regex = re.compile('')
    activeAstronautNames = re.findall(regex, landingPageBody)'''

### TODO: Some bios change when going to the html bio page, maybe for each name click on their name and then from the next page find the actual bio page.
### TODO: Handle the time out error
def get_active_astronaut_bios():
    # The links on the active astronuats page are generated using javascript, so call the JSON URL.
    active_astronauts_page = session.get('https://www.nasa.gov/api/1/record/node/376740.json', timeout = 0.5)
    activeAstronautsJSON = active_astronauts_page.json()

    # The body of the JSON file is where all the links are stored.
    landingPageBody = activeAstronautsJSON['landingPage']['body']
    
    # Each link to an astronaut's bio has the form: /astronauts/biographies/[astronaut-name]
    regex = re.compile('(?:\/astronauts\/biographies)(?:[^\"]+)')
    # Find every instance in the landing-page body that matches the regex.
    activeAstronautBios = re.findall(regex, landingPageBody)

    # Make every link in the array have the format: https://www.nasa.gov/astronauts/biographies/[astronaut]/biography
    for i in range(len(activeAstronautBios)):
        activeAstronautBios[i] = 'https://www.nasa.gov' + activeAstronautBios[i] + '/biography'

    return activeAstronautBios

# TODO def get_former_astronaut_bios():

def initialize_active_astronauts(activeAstronautBios):

    # Initialize a dictionary to store every active astronaut.
    activeAstronauts = {}

    # Iterate throught the bios and initialize active astronauts with names.
    for i, bio in enumerate(activeAstronautBios):

        # Get the HTML page, and check the website response.
        bioPage = session.get(bio)
        if not bioPage.ok:
            print('Could not print: ' + bio)
            continue

        # Store the HTML page as a Soup object.
        bioPageHTML = BeautifulSoup(bioPage.content, 'html.parser')

        # Split the title string into an array, delete the last 4 words, and put it back together.
        astronautName = bioPageHTML.title.string.split()
        del astronautName[-4:]
        astronautName = " ".join(astronautName)
        print(astronautName)

        # Initialize the astronaut as an Astronaut object and store it in a dictionary.
        activeAstronauts[astronautName] = Astronaut(astronautName, bio)

    return activeAstronauts
# TODO def initialize_former_astronauts(formerAstronautBios):

def main():
    # First get the links to each active astronaut's biography page.
    #currentAstronautBios = get_active_astronaut_bios()

    # Use the biographies of all active astronauts to initialize each active Astronaut.
    #activeAstronauts = initialize_active_astronauts(currentAstronautBios)

    get_active_astronauts()
    

main()