from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from game import State
import json
import asyncio
import threading
import sys

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
        self.state = State()
        self.text = ""
        self.adviser_message = SystemMessage(content="""
                Jesteś lemurem - doradcą głównego gracza, króla lemurów.
                Sprawdzasz czy starczy pieniędzy na dane inwestycje i doradzasz/odradzasz królowi jego decyzji,
                zanim podejmie je ostatecznie. Uważaj by chronić króla zarówno przed egoistycznymi jak i przed zbyt
                górnolotnymi, nierozsądnymi decyzjami (mimo że mogą brzmieć szlachetnie), w końcu
                piekło jest wybrukowane dobrymi intencjami. Wiesz że ważny jest balans i trzeba dbać o każdy z czterech
                aspektów królestwa. Nie wyświetlaj jsona ze stanem gry, po prostu opisuj go słownie, ale nie liczbami!
                Z drugiej strony nie możesz wpaść w paraliż analityczny i jeśli intuicja podpowiada ci że decyzja króla jest
                dobra, daj mu znać, że ma rację!
                Niech twoje wypowiedzi nie będą za długie. 3-5 zdań to dobra długość.
                """ + rules)
        
        self.king_message = SystemMessage(content="""
                Jesteś śmieszkowatym królem lemurów. Reprezentujesz gracza i podsumowujesz jego decyzję w krótkich śmiesznych słowach.
                Mimo pozornej lekkomyślności starasz się słuchać doradcy i dbać o poddanych. Twoje wypowiedzi to 1-2 zdania.
                Wypowiadasz się JAKO GRACZ a nie o graczu!!!
                """ + rules)
        
        self.people_message = SystemMessage(content="""
                Jesteś państwem lemurów, które reaguje na decyzje króla. Jesteś ludem! Jesteś poddanymi!
                Pamiętaj że poddani to NIE JEST doradca króla. Poddani to oddzielny, "wieloosoby" asystent,
                niepowiązany z doradcą
                """ + rules)

        self.calculator_message = SystemMessage(content=f"""
        Użytkownik podaje w swojej wypowiedzi wydatki na każdy z czterech aspektów królestwa:
        technologia, ochrona (przed klęskami żywiołowymi), szpitale, kultura.
        Jeśli któryś aspekt nie zostanie wymieniony to znaczy że przeznaczono na niego zero monet
        Aktualna liczba pieniędzy królestwa to: {self.state.coins}
        Przerób jego wypowiedź na json o dokładnie takich kluczach :
        {{
            "technologia": liczba pieniędzy przeznaczonych na technologię (integer a nie string),
            "kultura": liczba pieniędzy przeznaczonych na kulturę (integer a nie string),
            "szpitale": liczba pieniędzy przeznaczonych na szpitale (integer a nie string),
            "ochrona: liczba pieniędzy przeznaczonych na ochronę (przed klęskami żywiołowymi) (integer a nie string)
        }}
        Twoja odpowiedź ma zawierać TYLKO I WYŁĄCZNIE TAKI JSON (z dokładnie czterema kluczami), bez ŻADNYCH dodatkowych wartości!
        Nie dopisuj "Oto przetworzony wynik" ani nic podobnego, ma być TYLKO JSON!
        """)
        self.model = ChatOllama(model="llama3.1:8b", base_url="http://10.8.0.1:8080", keep_alive=1500)
        self.tour = 0
        self.verdict = ""
        self.expense = ""

    def gameStep(self, starting, data=None):
        """
        JEDEN -> czekamy na startowy werdykt
        DWA -> opcjonalna zmiana werdyktu
        TRZY -> egzekucja
        powtórz
        """

        if starting:
            self.verdict = data["verdict"]
            self.expense = data["expense"]
            response = self.model.invoke([self.adviser_message, HumanMessage(content=self.verdict+"\nSpis wydatków\n"+str(self.expense)+"\nObecny stan gry:\n"+str(self.state))])
            return {
                "adviser_response": response.content,
            }


        else:
            self.state.nextStep(self.expense)
            king_response = self.model.invoke([self.king_message, HumanMessage(content="Wyraź decyzję gracza (poniżej) swoimi słowami\n" + self.verdict + "\nSpis wydatków:\n" + str(self.expense))])
            people_response = self.model.invoke([self.people_message, HumanMessage(content="Zarządzenie króla:\n"+king_response.content+str(self.state))])
            self.tour += 1
            return {
                "king_response": king_response.content,
                "people_response": people_response.content,
            }

if __name__ == "__main__":
    communicator = Communicator()
    communicator.startGame()
