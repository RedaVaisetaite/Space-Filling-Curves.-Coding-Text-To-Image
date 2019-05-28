## Erdvę užpildančios kreivės ir jų pritaikymas teksto kodavimui paveiksliuke
Šios programos pagalba galima slėpti informaciją vaizduose
------------------Programos paleidimas--------------------------------
Programa turi vieną pagrindinį aplankalą EUK. Jame yra keletas kitų:
    uzkoduoti - aplankalas naudojamas užkoduotiems paveikslėliams saugoti
    rezultatams - dekoduotiems failams saugoti
    kodavimui - aplankalas, kuriame jau yra keletas paveikslėlių bei kitų failų, kuriuos galima naudoti kodavimui.
Pagrindiniame EUK aplankale yra ir programos failai:
    gui.ui bei ImageShow.ui xml kalba suformuoti grafinės sąsajos failai. Jie automatiškai sugeneruojami PyQt5 Designer įrankio pagalba.
    DecodeFile.py ir EncodeFile.py failuose yra pagrindinis funkcionalumas naudojamas dekuoduojant ir užkoduojant failus.
    imageDecoding.py ir imageEncoding.py failuose yra pagrindinis funkcionalumas naudojamas dekuoduojant ir užkoduojant tekstą iš įvesties.
    main.py yra pagrindinis failas, kuriame jungiamas funkcionalumas su sukurta grafine sąsaja.
Programai paleisti savo kompiuteryje reikia turėti:
    Python3
    pyqt5-tools
Paprastam ir lengvam paketų instaliavimui naudojamas Pip. 
Turint jį savo kompiuteryje labai paprastai galima atsisiųsti bet kokį kitą norimą Python modulį.
Įsidiegus šiuos komponentus į kompiuterį ir esant programos pagrindiniame aplankale, 
programą galima paprastai pasileisti su komanda: python main.py. 
