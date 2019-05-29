# Erdvę užpildančios kreivės ir jų pritaikymas teksto kodavimui paveiksliuke

Šios programos pagalba galima slėpti informaciją vaizduose

## Programos reikalingi paketai

Programai paleisti savo kompiuteryje reikia turėti:

    * Python3 programavimo kalbos mechanizmą
    * pyqt5-tools biblioteką
    * Image modulį
    
Python programvimo kalbos mechanizmą instaliuoti galima įvairiais būdais. Kaip tai padaryti galima rasti jų oficialiame puslapyje https://www.python.org/

Paprastam ir lengvam paketų instaliavimui naudojamas Pip. Kaip jį paprastai instaliuoti Windows operacinėje sistemoje galima rasti https://www.liquidweb.com/kb/install-pip-windows/ puslapyje.
Turint jį savo kompiuteryje labai paprastai galima atsisiųsti bet kokį kitą norimą Python modulį.
```
pip install Image
pip install pyqt5-tools
```

Įsidiegus šiuos komponentus į kompiuterį ir esant programos pagrindiniame aplankale, 
programą galima paprastai pasileisti su komanda: 
```python main.py. ```

## Programos struktūra

   Programa turi vieną pagrindinį aplankalą EUK. Jame yra keletas kitų:
   
    * uzkoduoti - aplankalas naudojamas užkoduotiems paveikslėliams saugoti
    * rezultatams - dekoduotiems failams saugoti
    * kodavimui - aplankalas, kuriame jau yra keletas paveikslėlių bei kitų failų, kuriuos galima naudoti kodavimui.
    
   Pagrindiniame EUK aplankale yra ir programos failai:
   
    * gui.ui bei ImageShow.ui xml kalba suformuoti grafinės sąsajos failai. Jie automatiškai sugeneruojami PyQt5 Designer įrankio pagalba.
    * DecodeFile.py ir EncodeFile.py failuose yra pagrindinis funkcionalumas naudojamas dekuoduojant ir užkoduojant failus.
    * imageDecoding.py ir imageEncoding.py failuose yra pagrindinis funkcionalumas naudojamas dekuoduojant ir užkoduojant tekstą iš įvesties.
    * main.py yra pagrindinis failas, kuriame jungiamas funkcionalumas su sukurta grafine sąsaja.
    

