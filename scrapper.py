import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql_connector_conf import host_url, user_id, user_pass


db = mysql.connector.connect(
    host=host_url,
    user=user_id,
    passwd=user_pass,
    database="scrapper"
)

cathegories = ["webapp","mobile","remote","local","vendor","website","docu","video"]

headers = {
    'User-Agent': 'My User Agent 1.0',
}
    
def get_pages_and_insert(page_no, cathegory):
    page_url = f"https://www.vulnerability-lab.com/show.php?page={page_no}&cat={cathegory}"
    page_source = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(page_source.content, "html.parser")

    date_column_elements = soup.find_all("td", {"class" : "style14"})
    advisory_column_elements = soup.find_all("td", {"width" : "375"})
    version_column_elements = soup.find_all("td", {"class" : "x14"})
    type_column_elements = soup.find_all("td", {"width" : "50"})
    author_column_elements = soup.find_all("td", {"width" : "135"})
    exploit_count = 0

    link_list = list()
    for link in advisory_column_elements:
        link_list.append(link.find("a").get("href"))
    
    date_columns = list()
    for element in date_column_elements:
        date_columns.append(element.text)

    advisory_columns = list()
    for element in advisory_column_elements:
        advisory_columns.append(element.text)
        
    version_columns = list()
    for element in version_column_elements:
        if element.text == "D":
            exploit_count += 1
            continue
        version_columns.append(element.text)

    type_columns = list()
    for element in type_column_elements:
        type_columns.append(element.text)

    author_columns = list()
    for element in author_column_elements:
        author_columns.append(element.text)

    cursor = db.cursor()
    for i in range(exploit_count - 1, -1, -1):
        cursor.execute(f"SELECT COUNT(ADVISORYNAME) FROM vulnlab WHERE ADVISORYNAME='{advisory_columns[i]}'")
        count = cursor.fetchall()
        if count[0][0] > 0:
            print(advisory_columns[i], " This data pre-written, passed...")
            continue
        else:
            cursor.execute("INSERT INTO vulnlab (DATE, ADVISORYNAME, VERSION, TYPE, AUTHOR, LINKLIST, CATHEGORY) VALUES (%s,%s,%s,%s,%s,%s,%s)", (date_columns[i],advisory_columns[i],version_columns[i],type_columns[i],author_columns[i],link_list[i],cathegory))
            db.commit()



def main():
    for j in range(len(cathegories)):
        URL = f"https://www.vulnerability-lab.com/show.php?cat={cathegories[j]}"
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        page_bar = soup.find("div", {"class" : "Stil8"})
        page_count = 0
        for i in page_bar:
            continue
        else:
            page_count = int(i.text.strip())
            
        for i in range(page_count,0,-1):
            get_pages_and_insert(i,cathegories[j])
        else:
            print(F"finished {cathegories[j]}")

main()