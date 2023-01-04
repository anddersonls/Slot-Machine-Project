import random

#CONSTANTS
ROWS = 3
COLS = 3

#Dictionare
machine_symbols = {"@": 10, "$": 10, "&": 10, "#": 10}

#classe responsável por receber a aposta, em quais linhas vão ser apostadas e o valor apostado pra cada linha 
class Bet():

    #recebendo o valor total da aposta
    def bet_value(self): 
        self.amount = 0
        while self.amount <= 0:
            if self.amount <= 0:
                print("\nVocê deve digitar um valor de aposta válido!")
            try:
                self.amount = int(input("Valor que você deseja apostar: R$"))
            except:
                print("\nVocê deve digitar um valor de aposta válido!")        

    
    #recebendo as linhas em que o usuário quer apostar
    def get_lines(self):
        lines = []
        wanna_bet = input(f"\nDigite 'sim' caso queira apostar em alguma linha entre 1 e {ROWS} ou qualquer outra tecla para parar não apostar: ").lower()
        if wanna_bet in ["sim", "s"]:
            wanna_bet = True
        else:
            wanna_bet = False    
        while wanna_bet:
            line = input("\nEm qual linha você deseja apostar: ")
            if line.isdigit() and 1 <= int(line) <= 3 and line not in lines:
                lines.append(int(line))
                if len(lines)==3:
                    break
                else:
                    new_line = input("Digite 'sim' caso queira apostar em mais alguma linha ou qualquer outra tecla para parar por aqui: ").lower()
                    if new_line not in ["s", "sim"]:
                        wanna_bet = False
            else:
                print(f"\nVocê deve digitar um valor de linha válido (1-{ROWS})!")
        return lines        

    #recebendo o valor da aposta para cada linha    
    def get_bet_by_line(self):
        lines = self.get_lines()
        bet_by_line = []
        for value in (lines):
            bet_line=0
            while True:
                bet_line = input(f"\nDigite o valor que você deseja apostar na linha {value}: ")
                if bet_line.isdigit(): 
                    if int(bet_line) > 0 and (self.amount - int(bet_line)) >= 0:
                        bet_by_line.append(bet_line)      
                        self.amount -= int(bet_line)
                        break
                    else:    
                        print(f"\nVocê possui {self.amount}! Digite um valor válido dentro do que for possível apostar!")      
                else:    
                    print(f"\nVocê possui {self.amount}! Digite um valor válido dentro do que for possível apostar!") 

        return self.amount, lines, bet_by_line

    #recebe as colunas que o apostador quer apostar
    def get_columns(self):
        columns = []
        wanna_bet = input(f"\nDigite 'sim' caso queira apostar em alguma coluna 1 e {COLS} ou qualquer outra tecla para parar não apostar: ").lower()
        if wanna_bet in ["sim", "s"]:
            wanna_bet = True
        else:
            wanna_bet = False    
        while wanna_bet:
            column = input("\nEm qual coluna você deseja apostar: ")
            if column.isdigit() and 1 <= int(column) <= 3 and column not in columns:
                columns.append(int(column))
                if len(columns)==3:
                    break
                else:
                    new_colomn = input("Digite 'sim' caso queira apostar em mais alguma coluna ou qualquer outra tecla para parar por aqui: ").lower()
                    if new_colomn not in ["s", "sim"]:
                        wanna_bet = False
            else:
                print(f"\nVocê deve digitar um valor de linha válido (1-{COLS})!")

        return columns        

    #recebe a aposta do apostador para cada coluna que ele deseja apostar
    def get_bet_by_column(self):
        columns = self.get_columns()
        bet_by_column = []
        for value in (columns):
            bet_column=0
            while True:
                bet_column = input(f"\nDigite o valor que você deseja apostar na coluna {value}: ")
                if bet_column.isdigit(): 
                    if int(bet_column) > 0 and (self.amount - int(bet_column)) >= 0:
                        bet_by_column.append(bet_column)      
                        self.amount -= int(bet_column)
                        break
                    else:    
                        print(f"\nVocê possui {self.amount}! Digite um valor válido dentro do que for possível apostar!")      
                else:    
                    print(f"\nVocê possui {self.amount}! Digite um valor válido dentro do que for possível apostar!") 

        return self.amount, columns, bet_by_column


#classe responsável pelos métodos de cálculo dos ganhos
class Winnings(Bet):
    def __init__(self, amount, lines, bet_by_line, columns, bet_by_column):
        self.amount = amount
        self.lines = lines
        self.bet_by_line = bet_by_line
        self.columns = columns
        self.bet_by_column = bet_by_column


    #checando se houve algum ganho
    def checking_winnings_by_row(self, slot_machine):
        #checking winnings by row
        self.win = False
        for i in range(len(slot_machine)):
            count = 0
            previous_symbol = slot_machine[i][0]
            for j in range(ROWS):
                if (i+1) not in self.lines:
                    break
                current_symbol = slot_machine[i][j]
                if previous_symbol == current_symbol:
                    count += 1
            if count == COLS:
                self.amount = self.calculate_winnings_by_row(i+1)
                self.win = True

    

    #cálculo do valor ganho pela linha/coluna             
    def calculate_winnings_by_row(self, winning_line):                
        #calculando ganhos por linha
        amount = self.amount
        for i, line in enumerate(self.lines):
            if int(line) == int(winning_line):
                value = 0
                value = int(self.bet_by_line[i])*COLS
                amount += value
                print(f"\nParabés! Você acertou a aposta na linha {winning_line}!")
                print(f"Você recebeu R${value}!")
                print(f"Saldo atual: {amount}\n")
                return amount



    def checking_winnings_by_column(self, slot_machine):
        #checking winning by column
        for i in range(len(slot_machine)):
            count = 0
            previous_symbol = slot_machine[0][i]
            for j in range(COLS):
                if (i+1) not in self.columns:
                    print("quebrou")
                    break
                current_symbol = slot_machine[j][i]
                if previous_symbol == current_symbol:
                    count += 1
            if count == ROWS:
                self.amount = self.calculate_winnings_by_column(i+1)
                self.win = True

        if not self.win:
            print("\nSinto muito, infelizmente você não ganhou aposta alguma!")

        return self.amount

    
    def calculate_winnings_by_column(self, winning_column):
        for i, column in enumerate(self.columns):
            #print(f"coluna: {column}, winning_column: {winning_column}")
            amount = self.amount
            if int(column) == int(winning_column):
                value = 0
                value = int(self.bet_by_column[i])*COLS
                amount += value
                print(f"\nParabés! Você acertou a aposta na coluna {winning_column}!")
                print(f"Você recebeu R${value}!")
                print(f"Saldo atual: {amount}\n")
                return amount


#classe responsável por manter o funcionamento do jogo
class Game():
    #construindo a lista dos símbolos disponíveis
    def __init__(self):
        self.symbols_list = []
        for symbol, symbol_value in machine_symbols.items():
            for _ in range (symbol_value):
                self.symbols_list.append(symbol)
    

    #imprimindo a caça níqueis na tela
    def print_slot_machine(self):
        available_symbols = self.symbols_list[:]
        slot_machine = []
        print()
        for _ in range (COLS):
            slot_machine_line = []
            print("|", end="")
            for _ in range (ROWS):
                symbol = random.choice(available_symbols)
                available_symbols.remove(symbol)
                slot_machine_line.append(symbol)
                print(symbol, end="|")
            slot_machine.append(slot_machine_line)    
            print()

        return slot_machine


    def playing(self):
        round = Bet()
        round.bet_value()
        while True:
            amount, lines, bet_by_line = round.get_bet_by_line()
            amount, columns, bet_by_column = round.get_bet_by_column()
            play = Winnings(amount, lines, bet_by_line, columns, bet_by_column)
            slot_machine = self.print_slot_machine()
            play.checking_winnings_by_row(slot_machine)
            amount = play.checking_winnings_by_column(slot_machine)
            keep_playing = input("\nDigite 'sim' para jogar novamente, ou qualquer outra tecla para parar por aqui: ").lower()
            print()
            if keep_playing not in ["s", "sim"]:
                break
        
        print(f"\nSaldo final: {amount}!")
        print("Obrigado por jogar conosco, volte sempre!\n")

teste = Game()
teste.playing()
