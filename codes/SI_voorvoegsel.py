import requests
import re
import numeralsystem as ns

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
        if i == len(kolommen)/2:
            prefixenboek.append(kolommenboek)
            kolommenboek = {}

        if kolom[:2] == "<a":
            kolom = re.findall(">(.*)</a>", kolom)[0]
        if '<sup>' in kolom:
            kolom = re.findall("<sup>(.*)</sup>", kolom)[0]
        kolommenboek[titels[i]] = ''.join(kolom.replace(',', '.').replace('−', '-').split())

    prefixenboek.append(kolommenboek)


# prefixenboek = [{'n': '24', 'Prefix': 'yotta', 'Symbool': 'Y', 'Naam': 'quadriljoen', 'Decimaal': 1_000_000_000_000_000_000_000_000},
#                 {'n': '-24', 'Prefix': 'yocto', 'Symbool': 'y', 'Naam': 'eenquadriljoenste', 'Decimaal': 0.000_000_000_000_000_000_000_001},
#                 {'n': '21', 'Prefix': 'zetta', 'Symbool': 'Z', 'Naam': 'triljard', 'Decimaal': 1_000_000_000_000_000_000_000},
#                 {'n': '-21', 'Prefix': 'zepto', 'Symbool': 'z', 'Naam': 'eentriljardste', 'Decimaal': 0.000_000_000_000_000_000_001},
#                 {'n': '18', 'Prefix': 'exa', 'Symbool': 'E', 'Naam': 'triljoen', 'Decimaal': 1_000_000_000_000_000_000},
#                 {'n': '-18', 'Prefix': 'atto', 'Symbool': 'a', 'Naam': 'eentriljoenste', 'Decimaal': 0.000_000_000_000_000_001},
#                 {'n': '15', 'Prefix': 'peta', 'Symbool': 'P', 'Naam': 'biljard', 'Decimaal': 1_000_000_000_000_000},
#                 {'n': '-15', 'Prefix': 'femto', 'Symbool': 'f', 'Naam': 'eenbiljardste', 'Decimaal': '0.000000000000001'},
#                 {'n': '12', 'Prefix': 'tera', 'Symbool': 'T', 'Naam': 'biljoen', 'Decimaal': '1000000000000'},
#                 {'n': '-12', 'Prefix': 'pico', 'Symbool': 'p', 'Naam': 'eenbiljoenste', 'Decimaal': '0.000000000001'},
#                 {'n': '9', 'Prefix': 'giga', 'Symbool': 'G', 'Naam': 'miljard', 'Decimaal': '1000000000'},
#                 {'n': '-9', 'Prefix': 'nano', 'Symbool': 'n', 'Naam': 'eenmiljardste', 'Decimaal': '0.000000001'},
#                 {'n': '6', 'Prefix': 'mega', 'Symbool': 'M', 'Naam': 'miljoen', 'Decimaal': '1000000'},
#                 {'n': '-6', 'Prefix': 'micro', 'Symbool': 'µ', 'Naam': 'eenmiljoenste', 'Decimaal': '0.000001'},
#                 {'n': '3', 'Prefix': 'kilo', 'Symbool': 'k', 'Naam': 'duizend', 'Decimaal': '1000'},
#                 {'n': '-3', 'Prefix': 'milli', 'Symbool': 'm', 'Naam': 'eenduizendste', 'Decimaal': '0.001'},
#                 {'n': '2', 'Prefix': 'hecto', 'Symbool': 'h', 'Naam': 'honderd', 'Decimaal': '100'},
#                 {'n': '-2', 'Prefix': 'centi', 'Symbool': 'c', 'Naam': 'eenhonderdste', 'Decimaal': '0.01'},
#                 {'n': '1', 'Prefix': 'deca', 'Symbool': 'da', 'Naam': 'tien', 'Decimaal': '10'},
#                 {'n': '-1', 'Prefix': 'deci', 'Symbool': 'd', 'Naam': 'eentiende', 'Decimaal': '0.1'}]


class SIPrefix:
    def __init__(self, getal, eenheid=None):
        if eenheid is None:
            getal_backup = getal
            getal = re.findall("[-+]?[\d]+(?:[.,]?[\d]+)?(?:[eE]?[\d]+)?", getal_backup)[0]
            eenheid = getal_backup.replace(getal, "").lstrip(' ')
        if isinstance(getal, str):
            getal = getal.replace(',', '.')
        self.getal = ns.BaseN(getal, n=10)
        self.eenheid = eenheid

    def __str__(self):
        return str(self.getal) + self.eenheid

    def prefixboek(self):
        for prefixboek in prefixenboek:
            if not int(prefixboek['n']) % 3:
                precisie = ns.BaseN(prefixboek["Decimaal"], n=10)
                if precisie <= self.getal < ns.BaseN('1000', n=10)*precisie:
                    return prefixboek
        else:
            return {"Decimaal": 1, "Symbool": ''}

    def transform(self, dgt=None):
        prefixboek = self.prefixboek()
        self.getal = self.getal / ns.BaseN(prefixboek["Decimaal"], n=10)
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
                    self.getal *= ns.BaseN(prefixboek["Decimaal"], n=10)
                    self.eenheid = self.eenheid.replace(prefix, '', 1)
        return self

