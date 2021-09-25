from zipfile import ZipFile
import zipfile
import wget
import os
import subprocess
import pycountry

# define variables
path = '/path/ipvanish/'
url = 'https://www.ipvanish.com/software/configs/configs.zip'
filename = path + '/' + os.path.basename(url)
best_ping = 99999

# get user's choice
def get_choice():
    print("1 - delete old configs, and download + unzip new config\n2 - check best server to desired country\n3 - exit")
    choice = int(input("Enter number:\n"))
    return (choice)

# get country from user input
def get_country():
    print("Please enter the name of the country you would like to connect to")
    country = str(input("Country: "))
    return(country)

# convert user selection into 2 letter country notion
def get_country_code(country):
    mapping = {country.name: country.alpha_2 for country in pycountry.countries}
    code = mapping.get(country)
    if type(code) is str:
        return(code)
    else:
        return("Country not found!")

# deletes old *.zip & *.ovpn files, downloads new file and unzips it
def delete_and_renew_config():
    for config_file in os.listdir(path):
        if config_file.endswith(".ovpn") or config_file.endswith(".crt") or config_file == "configs.zip":
            os.remove(path + config_file)
    wget.download(url, '/path/ipvanish/configs.zip')
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(path)


        
        def get_host_and_ping(conf_file):
    with open(path + conf_file) as file:
        for i, line in enumerate(file):
            if i == 3:
                host = line.split()[1]
                ping = os.system("ping -c 1 " + host)
                return [host, ping]


# returns dictionary with the form: {"filename.ovpn" : [ "host", avgping]}
def get_servers(code):
    srvs = {}
    for config_file in os.listdir(path):
        if config_file.startswith("ipvanish-" + code):
            # first 0 is placeholder for HOSTNAME, second is for AVG PING
            srvs[config_file] = get_host_and_ping(config_file)
    return(srvs)

# returns the config file name of the best server
def return_best_server(servers):
    for index, (server, host) in enumerate(servers.items()):
        if float(host[1]) < float(best_ping):
            best_srv = server
    return(best_srv)


# main while loop
while 1:
    choice = get_choice()
    if choice == 1:
        delete_and_renew_config()
    elif choice == 2:
        country = get_country()
        code = get_country_code(country)
        servers = get_servers(code)
        best_srv = return_best_server(servers)
        print("The best server is: " + best_srv)
    elif choice == 3:
        break
