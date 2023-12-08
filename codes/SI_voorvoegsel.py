import requests
import re
import numeralsystem as ns
import json
import os

folder = os.path.dirname(os.path.abspath(__file__))
prefixenboek_path = os.path.join(folder, "prefixenboek.json")


def parse(value, type):
    try:
        value = type(value)
    except ValueError:
        pass
    return value


def parse_int(value):
    return parse(value, int)


def parse_float(value):
    return parse(value, float)


def update_voorvoegsels():
    wikipagina = requests.get(url="https://nl.wikipedia.org/wiki/SI-voorvoegsel")
    htmlpagina = wikipagina.content
    htmltekst = str(htmlpagina, encoding="utf-8")
    htmlstr = '/n'.join(htmltekst.split("\n")).replace("</table>", "\n")
    tabel = re.findall("<table class=\"wikitable\">(.*)", htmlstr)[0]
    rijen = re.findall("<tr>(.*)", tabel.replace("</tr>", "\n"))
    
    titels = []
    titels_slecht = re.findall("<th>(.*)", rijen[0].replace("/n", "\n"))
    for titel in titels_slecht:
        if titel[:2] == "<a":
            titel = re.findall(">(.*)</a>", titel)[0]
        if '<i>' in titel:
            titel = re.findall("<i>(.*)</i>", titel)[0]
        titels.append(titel)
    
    prefixenboek = []
    for rij in rijen[1:]:
        kolommen = re.findall("<td>(.*)", rij.replace("/n", "\n"))
        kolommenboek = {}
        for i, kolom in enumerate(kolommen):
            if i == len(kolommen) / 2:
                prefixenboek.append(kolommenboek)
                kolommenboek = {}
            
            if kolom[:2] == "<a":
                kolom = re.findall(">(.*)</a>", kolom)[0]
            if '<sup>' in kolom:
                kolom = re.findall("<sup>(.*)</sup>", kolom)[0]
            value = ''.join(kolom.replace(',', '.').replace('−', '-').split())
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
            kolommenboek[titels[i]] = value
        
        prefixenboek.append(kolommenboek)
    
    with open(prefixenboek_path, 'w') as f:
        json.dump(prefixenboek, f)


# try:
#     update_voorvoegsels()
# except:
#     pass
with open(prefixenboek_path, 'r') as f:
    prefixenboek = json.load(f)
    prefixenboek = [prefix for prefix in prefixenboek if not prefix['n'] % 3]  # filter out deci, deca, centi, hecto


class SIPrefix:
    def __init__(self, getal, eenheid=None, base=10):
        if isinstance(getal, (int, float, ns.BaseN)):
            self.getal = getal
            self.eenheid = "" if eenheid is None else eenheid
            return
        
        if eenheid is None:
            if not isinstance(getal, str):
                getal = str(getal)
            getal_backup = getal
            getal = re.findall(r"[-+]?[\d]+(?:[.,]?[\d]+)?(?:[eE]?[\d]+)?", getal_backup)[0]
            eenheid = getal_backup.replace(getal, "").strip()
        if isinstance(getal, str):
            getal = getal.replace(',', '.')
        
        self.getal = ns.BaseN(getal, n=base) if base else float(getal) if '.' in getal else int(getal)
        self.eenheid = eenheid
    
    def __str__(self, f="", sep=""):
        return f"{self.getal:{f}}{sep}{self.eenheid}"
    
    def __repr__(self):
        return f"SIPrefix({self.getal}, {self.eenheid})"
    
    def get_getal_eenheid(self):
        return self.getal, self.eenheid
    
    def prefixboek(self):
        for prefix in prefixenboek:
            if not int(prefix['n']) % 3:
                precisie = prefix["Decimaal"]
                if precisie <= self.getal < 1000 * precisie:
                    return prefix
        else:
            return {"Decimaal": 1, "Symbool": ''}
    
    def transform(self, dgt: int = None):
        prefixboek = self.prefixboek()
        self.getal /= prefixboek["Decimaal"]
        self.getal = self.getal if dgt is None else round(self.getal, dgt)
        self.eenheid = prefixboek["Symbool"] + self.eenheid
        return self
    
    def transform_r(self):
        if self.eenheid and len(self.eenheid) > 1:
            prefix = self.eenheid[0]
            if prefix == 'u':
                self.eenheid = self.eenheid.replace('u', 'µ', 1)
                prefix = 'µ'
            if prefix == 'd':
                if self.eenheid[1] == 'a':
                    prefix = 'da'
                else:
                    prefix = ''
            
            for prefixboek in prefixenboek:
                if prefixboek["Symbool"] == prefix:
                    self.getal *= prefixboek["Decimaal"]
                    self.eenheid = self.eenheid.replace(prefix, '', 1)
        return self
