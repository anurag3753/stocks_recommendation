import os

def setup_env():
    pwd                             = os.getcwd()
    os.environ["attendees"]         = pwd + "/" + "data" + "/" + "attendees.txt"
    os.environ["calender_conf"]     = pwd + "/" + "config" + "/" + "calender.conf"
    os.environ["creds"]             = pwd + "/" + "config" + "/" + "credentials.json"
    os.environ["token"]             = pwd + "/" + "config" + "/" + "token.pickle"
    os.environ["data_csv_path"]     = pwd + "/" + "data" + "/" + "data.csv"
    os.environ["download_location"] = pwd + "/" + "data"
    os.environ["eventTemplate"]     = pwd + "/" + "data" + "/" + "eventTemplate.yaml"
    os.environ["map"]               = pwd + "/" + "data" + "/" + "map.yaml"
    os.environ["pwd"]               = pwd

setup_env()