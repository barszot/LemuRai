from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from game import State


rules = """
Zasady gry:

To jest jednoosobowa gra. Główny gracz to śmieszny król lemurów, który musi dbać o poddanych.
Gra ma cel edukacyjny - doradca króla (komputer - chatbot), pomaga graczowi podejmować decyzje i opisuje mu dlaczego takie aspekty
jak technologia, kultura, szpitale i ochrona przed klęskami żywiołowymi są istotne
Królestwo posiada pieniądze, które w każdej turze można (ale nie trzeba) wydać na poprawę czterech aspektów królestwa:
1) Kultura
2) Technologia
3) Szpitale
4) Ochrona przed klęskami żywiołowymi

Z każdą turą gry do skarbca przybywa pieniędzy zależnie od trzech czynników: wielkości populacji lemurów
oraz punktów 'technologii' i 'kultury'. 

- Technologia wpływa na zyski,
- Kultura wpływa na zyski (w mniejszym stopniu niż technologia) oraz na szczęście oraz rozrastanie się populacji,
- Szpitale zwiększają uleczalność chorób podczas epidemii, dzięki czemu można chronić poddanych przed śmiercią
- Ochrona przed klęskami żywiołowymi (w skrócie 'ochrona'), chroni poddanych przed śmiercią z powodu suszy, powodzi, ulew, i tym podobnych.

Rozgrywka wyglada tak:
Gracz (człowiek), wpisuje jak przydzieli pieniądze w danej turze. Następnie doradca (komputer - chatbot), sprawdza czy liczba zainwestowanych pieniędzy nie przekracza
tej w skarbcu. Jeśli jest okej, pomaga mu podjąć decyzję (na przykład doradza inwestycję w kulturę, czy zbudowanie ochronnego systemu przed wielką ulewą, edukując gracza).
Następnie gracz może (ale nie musi), zmienić decyzję, i wtedy jest egzekwowana przez kod komputerowy gry. Chatbot generuje śmieszkowatą, krótką
wypowiedź króla lemurów, która streszcza decyzję (np. że postanowił zainwestować sporo w technologię i trochę w kulturę, ale to ma być żartobliwie powiedziane).

Na końcu tury poddani (także komputer), komentują decyzję króla oraz obecne zdarzenia. Na przykład jeśli dofinansował technologię której brakowało akurat pieniędzy, chwalą to.
Jeśli była klęska żywiołowa a król nie zadbał o ochronę i sporo lemurów zginęło - są źli na króla. Jesli byla epidemia i mało lemurów zginęło dzięki szpitalom, doceniają wcześniejsze inwestycje w szpitale.

"""

class Communicator:
    def __init__(self):
        self.adviser_messages = [
            SystemMessage(content="""
                Jesteś lemurem - doradcą głównego gracza, króla lemurów.
                Sprawdzasz czy starczy pieniędzy na dane inwestycje i doradzasz/odradzasz królowi jego decyzji,
                zanim podejmie je ostatecznie.
                """ + rules),
        ]
        self.king_messages = [
            SystemMessage(content="""
                Jesteś śmieszkowatym królem lemurów. Reprezentujsz gracza i podsumowujesz jego decyzję w krótkich śmiesznych słowach.
                Mimo pozornej lekkomyślności starasz się słuchać doradcy i dbać o poddanych.
                """ + rules),
        ]
        self.people_messages = [
            SystemMessage(content="""
                Jesteś państwem lemurów, które reaguje na decyzje króla.
                """ + rules),
        ]
        
        self.model = ChatOllama(model="llama3.1:8b", base_url="http://10.8.0.1:8080")

     


        # Wywołanie modelu
        # response = model.invoke([HumanMessage(content="Who is king julien?")])
        # print(response.content)


