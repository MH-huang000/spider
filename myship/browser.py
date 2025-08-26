from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options

USER_DATA_DIR = r"C:\Users\MH\AppData\Local\Microsoft\Edge\User Data"
PROFILE_DIRECTORY = "Profile 3"
DRIVER_PATH = r"C:\browserdriver\edgedriver\msedgedriver.exe"

def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
    options.add_argument(f"--profile-directory={PROFILE_DIRECTORY}")
    service = EdgeService(executable_path=DRIVER_PATH)
    return webdriver.Edge(service=service, options=options)