from bs4 import BeautifulSoup
import requests
import requests.exceptions
from collections import deque



#--------------------------------Crawler part------------------------------------------------------------------


def get_url( url: str) -> BeautifulSoup:
    """
    Overrides Scraper.get_url()
    :param url:
    :return:
    """
    try:

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    except requests.exceptions.RequestException:

        return get_url(url)



starturls = ['https://www.depensez.com/actus/','https://www.depensez.com/conseils/','https://www.depensez.com/consommation/', 'https://www.depensez.com/astuces/','https://www.depensez.com/non-classe/' ]
new_urls = deque(starturls)

def getpages(new_urls):


        #intiliser la liste qui va contenir tous les urls
        internalsurls = []
        while len(new_urls):
        # move url from the queue

                    next_url = new_urls.popleft()
                    print(next_url)
                    print('Processing url', next_url)
                    soup = get_url(next_url)
                    internalsurls.append(next_url)
                    print("processing all pages in this url  this may take few minutes")
                    #get all next pages
                    if soup.find('span', class_="last-page first-last-pages"):
                            while True:

                                  soup =get_url(next_url)
                                  if  'Page suivante' in soup.find('span', class_="last-page first-last-pages").text :

                                      next_url = soup.find('span', class_="last-page first-last-pages").find('a', href=True)["href"]
                                      print("pass to this page"+next_url)
                                      internalsurls.append(next_url)
                                  else : break
        return(internalsurls)






#avoir les liens qui existent au niveau de chaque lien

def getlinks(internalsurls):


    allurls=set()
    #pour avoir que les lienslocaux ayant des catégories
    baseurl='https://www.depensez.com/'
    for i, j  in  enumerate(internalsurls):
            print("Actual link")
            print(j)

            soup = get_url(j)
            print("preproccing all links that exists in this link....")

            #la structuratuion  ded liens au niveau de  la page consommation est différente des autre
            if 'consommation' in j :

                for link in soup.find('div', class_="main-content tie-col-md-8 tie-col-xs-12").find_all('a'):

                    # extract link url from the anchor
                    anchor = link.attrs['href'] if 'href' in link.attrs else ''
                    if baseurl in anchor:
                        print(anchor)
                        print("add add this url page")
                        allurls.add(anchor)
            else:

                    for link in soup.find('div', class_="mag-box-container").find('ul').find_all('a'):


                # extract link url from the anchor
                        anchor = link.attrs['href'] if 'href' in link.attrs else ''
                        if baseurl in anchor:
                                print(anchor)
                                print("add and url page")

                                allurls.add(anchor)
    return allurls



#-------------------------------- Scrapper part------------------------------------------------------------------




def getinfo(l):
    print("extract data from all links craweled")
    a = []
    for i,j in enumerate(l):

        print("page:"+j)

        soup =  get_url(j)

        if soup.find("h5"):
                item = {
                    'Titre': soup.find("h1").text,
                    'Category' : ""}
                list=soup.find("h5").find_all('a')

                category= ""
                #il y a des pages qui ont plus q'une catégorie


                for o in list:

                    category= category+" "+o.text
                item['Category']=category
        a.append(item)


 #liste qui contient toutes les pages ainsi que leurs catégories
    return (a)



if __name__ == '__main__':
    print("Crawler part ....")
    internalsurls= getpages(new_urls)
    print(internalsurls)
    l=getlinks(internalsurls)
    #print(l)
    print("Scrapper part ....")
    f=getinfo(l)
    print(f)