import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from bs4 import BeautifulSoup
import json, os
import paramiko, csv
import getpass, time

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''                             # acts as a browser to read the html file
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


url = "http://192.168.1.8:8080"                   # change the url of the reactor
client_response = Page(url)
# html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(client_response.html, 'lxml')

i=1
parameters = {}
for table in soup.find_all('td', attrs={'class':'sens_2'}):
    parameters[i]=table.text
    i+=1

i=1
reactor = {}
for value in soup.find_all('div', attrs={'id':'sensval'}):
    reactor[parameters[i]]=value.text
    i+=1

print(reactor)
iparameters={}
i=1
for inline in soup.find_all('dt', attrs={'type':'actuator'}):
    iparameters[i]=inline.text
    i+=1
iparameters[i+1] = 'Process time'
ireactor={}
i=1
for value in soup.find_all('span', attrs={'class':'val', 'style':'padding-left: 5px'}):
    ireactor[iparameters[i]]=value.text
    i+=1
time = soup.find('span', attrs={'id':'process_time'})
ireactor[iparameters[i+1]]=time.text
print(ireactor)

output ={}
output.update(reactor)
output.update(ireactor)

header = output.keys()
file_exists = os.path.isfile('reactor.csv')
with open('reactor.csv', 'a', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, header)
    if not file_exists:
        dict_writer.writeheader()
    dict_writer.writerow(output)

with open('result.json', 'w') as fp:
    json.dump(output, fp)

##hostname = 'ssh1.abc.in'
##command = 'scp result.json as1110011@ssh1.abc.in:/home/dbeb/dual/as1110011/private_html/result.json'
##password = ''
##username = ""
##port = 
##
##try:
##    t = paramiko.Transport((hostname, port))
##    t.connect(username=username, password=password)
##    sftp = paramiko.SFTPClient.from_transport(t)
##    sftp.put('result.json','/home/dbeb/dual/as1110011/private_html/result.json')
##
##finally:
##    t.close()

