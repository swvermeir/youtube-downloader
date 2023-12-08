import ssl
from urllib.parse import urlparse
import requests
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup, PageElement
import subprocess
from urllib.parse import urljoin, urlparse, urlunparse, urlsplit
import re
from typing import Iterable, Callable
import shutil
import os

from tqdm import tqdm

import logging
logging.basicConfig(level=logging.DEBUG)


def is_rel_url(url):
    parsed_url = urlparse(url)
    return not bool(parsed_url.netloc)

def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = parsed_url.netloc
    if scheme:
        base_url = f"{scheme}://{base_url}"
    return base_url

def fix_rel_url(rel_url, ref_url):
    if not is_rel_url(rel_url):
        return rel_url
    
    parsed_url = urlparse(ref_url)
    new_parsed_url = [parsed_url.scheme, parsed_url.netloc, rel_url, None, None, None]
    return urlunparse(new_parsed_url)


def string(iterable, level=1):
    assert level >= 1
    if isinstance(iterable, str):
        return iterable
    elif isinstance(iterable, (dict, CaseInsensitiveDict)):
        brackets = "{}"
        iterable = [f"{string(key, level=level+1)}: {string(value, level=level+1)}" for key, value in iterable.items()]
    elif isinstance(iterable, (set, dict)):
        brackets = "{}"
    elif isinstance(iterable, tuple):
        brackets = "()"
    elif isinstance(iterable, (list, Iterable)):
        brackets = "[]"
    else:
        return str(iterable)

    iterable_string = brackets[0] + '\n'
    for item in iterable:
        iterable_string += '\t' * level + string(item, level=level+1) + '\n'
    iterable_string += '\t' * (level - 1) + brackets[1]
    return iterable_string


class Program:
    def __init__(self, ):
        self.install_urls_url = None
        self.install_url = None
        self.install_file = None
    
    def get_install_url(self):
        # Important to keep empty since it is used in self.install()
        pass
    
    def get_install_file(self):
        logging.info(f"Downloading file from {self.install_url}")
        
        response = requests.get(self.install_url, stream=True)
        
        headers = response.headers
        logging.debug(f"Headers = {string(headers)}")
        
        size = headers.get('Content-Length')  # response.headers = CaseInsensitiveDict => Content-Length == content-length
        if size:
            size = int(size)
        logging.debug(f"size = {size}B")
        
        filename = None
        content_disposition = headers.get('Content-Disposition')
        if content_disposition:
            attachments = content_disposition.split(';')
            for att in attachments:
                att = att.strip()
                
                att_split = att.split('=')
                if len(att_split) != 2:
                    continue
                
                key, value = att_split
                if key == "filename":
                    filename = value.strip('"')
        if not filename:
            filename = self.install_url.split('/')[-1]
            
        try:
            with open(filename, 'wb'):
                pass
        except:
            filename = type(self).__name__ + ".exe"
        logging.debug(f"filename = {filename}")

        chunk_size = 8 * 1024 * 1024
        with open(filename, "wb") as file:
            with tqdm(total=size, unit='B', unit_scale=True) as pbar:
                for data in response.iter_content(chunk_size):
                    file.write(data)
                    pbar.update(len(data))
        self.install_file = filename
    
    def run_install_file(self, silent=False):
        args = [self.install_file]
        if silent:
            args.extend(['/Silent', '/s', '/S', '/silent'])
        subprocess.call(args, shell=True)
        
    def install(self, new_install_folder=None):
        """
        :param new_install_folder: None => Nothing happens; False => install file will be removed; path => install file will be moved
        :return:
        """
        self.get_install_url()
        self.get_install_file()
        self.run_install_file()
        if new_install_folder is None:
            return
        
        if new_install_folder:
            self.move_install_file(new_install_folder)
        else:
            self.remove_install_file()
        
    def remove_install_file(self):
        os.remove(self.install_file)
        
    def move_install_file(self, new_folder: str = None):
        filename = os.path.basename(self.install_file)
        new_path = os.path.join(new_folder, filename)
        shutil.move(self.install_file, new_path)
        self.install_file = new_path
    
class ProgramDownloadFromButton(Program):
    def __init__(self):
        super().__init__()
        self.button_text = None
        
    def extra_link_condition(self, link: PageElement):
        return True
        
    def get_button_link(self):
        response = requests.get(self.install_urls_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        if not links:
            logging.error("No <a> tags (with href) found in response html")
            raise
        
        if self.button_text is None:
            logging.error("No self.button_text found, thus no correct button can be identified")
        
        for a in links:
            if self.button_text == a.text.strip() and self.extra_link_condition(a):  # Check for exact match
                break
        else:  # not break
            for a in links:
                if self.button_text in a.text.strip() and self.extra_link_condition(a):  # Check for unexact match
                    break
            else:
                logging.error(f"No <a> tag found with text: \"{self.button_text}\" and extra condition \"{self.extra_link_condition.__name__}\"")
                raise

        url = a['href']
        self.install_url = fix_rel_url(url, self.install_urls_url)
        logging.info(f"Found install url {self.install_url}")
        
    def get_install_url(self):
        return self.get_button_link()

class ProgramDownloadFromMultipleButtons(ProgramDownloadFromButton):
    def __init__(self):
        super().__init__()
        self.all_button_texts = []
        self.all_extra_link_conditions = []
        
    def get_install_url(self):
        install_urls_url_backup = self.install_urls_url
        for i, self.button_text in enumerate(self.all_button_texts):
            if self.all_extra_link_conditions:
                self.extra_link_condition = self.extra_link_conditions[i]
            self.get_button_link()
            self.install_urls_url = self.install_url
        self.install_urls_url = install_urls_url_backup
    

class Notepadpp(Program):
    def __init__(self):
        super().__init__()
        self.install_urls_url = "https://api.github.com/repos/notepad-plus-plus/notepad-plus-plus/releases/latest"
    
    def get_install_url(self):
        logging.info(f"Searching install file on {self.install_urls_url}")
        response = requests.get(self.install_urls_url)
        info = response.json()
        tag = info.get('tag_name')[1:]  # [1:] removes v in v8.5.6
        asset_name = f"npp.{tag}.Installer.x64.exe"
        
        assets = info.get('assets')
        for ass in assets:
            name = ass.get('name')
            if name == asset_name:
                url = ass.get("browser_download_url")
        self.install_url = url


class AntibodySoftwarePrograms(Program):  # Deprecated since DownloadFromButton should be good enough.
    def get_install_url(self):
        response = requests.get(self.install_urls_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        if not links:
            logging.error("No <a> tags (with href) found in response html")
            raise
        
        for a in links:
            bigis = a.find('big', recursive=False)
            if bigis and bigis.text.strip() in ("DOWNLOAD INSTALLER", "DOWNLOAD 64 BIT"):
                break
        else:  # not break
            logging.error("No <a> tag found with <big>DOWNLOAD INSTALLER</big>")
            raise
        
        url = a['href']
        self.install_url = fix_rel_url(url, self.install_urls_url)
        logging.info(f"Found install url {self.install_url}")

class WizTree(ProgramDownloadFromButton):
    def __init__(self):
        super().__init__()
        self.install_urls_url = "https://diskanalyzer.com/download?ref=upgrade"
        self.button_text = "DOWNLOAD INSTALLER"

class WizFile(ProgramDownloadFromButton):
    def __init__(self):
        super().__init__()
        self.install_urls_url = "https://antibody-software.com/wizfile/download?ref=upgrade"
        self.button_text = "DOWNLOAD INSTALLER"
        
class BulkImageDownloader(AntibodySoftwarePrograms):  # Removed from pc
    def __init__(self):
        super().__init__()
        self.install_urls_url = "https://bulkimagedownloader.com/download?ref=upgrade"
        self.button_text = "DOWNLOAD 64 BIT"


class Everything(ProgramDownloadFromButton):
    def __init__(self):
        super().__init__()
        self.install_urls_url = "https://www.voidtools.com/"
        self.button_text = "Download Installer 64-bit"
        
class Everything_alpha(ProgramDownloadFromButton):
    def __init__(self):
        super().__init__()
        self.install_urls_url = "https://www.voidtools.com/forum/viewtopic.php?f=12&t=9787#download"
        self.button_text = ".x64-Setup.exe"


class GlaryUtilities(Program):
    def __init__(self):
        super().__init__()
        self.install_url = "https://download.glarysoft.com/gu5setup.exe"
        
        
class MalwareBytes(Program):
    def __init__(self):
        super().__init__()
        # self.install_urls_url = "https://www.malwarebytes.com/"
        # self.button_text = "Free download"
        self.install_url = "https://www.malwarebytes.com/api/downloads/mb-windows?filename=MBSetup.exe"


class CpuZ(ProgramDownloadFromMultipleButtons):
    def __init__(self):
        super().__init__()
        self.install_urls_url = "https://www.cpuid.com/softwares/cpu-z.html"
        self.all_button_texts = ["setup • english32 and 64-bit version", "DOWNLOAD NOW!"]


class SevenZip(ProgramDownloadFromButton):
    def __init__(self):
        super().__init__()
        self.install_urls_url = "https://7-zip.org/"
        self.button_text = "Download"
    
    def extra_link_condition(self, link: PageElement):
        td_link = link.find_parent('td', class_="Item")
        if td_link is None:
            return False
        for td in td_link.find_next_siblings('td', class_="Item"):
            if td.text.strip() == "64-bit x64":
                return True
        return False


def update_all():
    # List of all programs on the pc
    pc_programs = [Notepadpp, WizTree, WizFile, Everything, GlaryUtilities, MalwareBytes, SevenZip]
    for program in pc_programs:
        program().install(new_install_folder=r"D:\gebruiker hdd\Set up files")
        
        
def main():
    x = update_all()
    
if __name__ == '__main__':
    main()
