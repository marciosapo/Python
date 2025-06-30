import sqlite3
from tkinter import *
from tkinter import messagebox
from jogadores import Jogador  # Supondo que Jogador é uma classe definida no seu módulo
import random

# Variáveis globais
scored = False
playercombola = ""
playerpos = ""
side = ""
player_window = None
intervalo = False
intervalotime = 0
apitoFinal = False
ingame = False
mins = 0
secs = 0
timing = 0
team_start = ""
descontos = 0
golos = 0
golos2 = 0

# Função para conectar à base de dados e criar tabelas, se não existirem
def connect_db():
    try:
        conn = sqlite3.connect('basedados.db')
        cursor = conn.cursor()

        # Criar tabela Clube1 (Sporting) se não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS Clube1 (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Nome TEXT NOT NULL)''')

        # Criar tabela Clube2 (FC Porto) se não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS Clube2 (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Nome TEXT NOT NULL)''')

        # Criar tabela Players se não existir, incluindo os novos campos
        cursor.execute('''CREATE TABLE IF NOT EXISTS Players (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            Nome TEXT NOT NULL,
                            POS TEXT NOT NULL,
                            COND INTEGER NOT NULL,
                            Clube TEXT NOT NULL,
                            PosseBola INTEGER NOT NULL,
                            Desarme INTEGER NOT NULL,
                            BolasNasMaos INTEGER NOT NULL,
                            Passe INTEGER NOT NULL,
                            Finalizacao INTEGER NOT NULL,
                            Numero INTEGER NOT NULL)''')

        # Verificar se os times já foram inseridos
        cursor.execute("SELECT COUNT(*) FROM Clube1")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Clube1 (Nome) VALUES ('Sporting')")
        
        cursor.execute("SELECT COUNT(*) FROM Clube2")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO Clube2 (Nome) VALUES ('FC Porto')")

        # Verificar se os jogadores já foram inseridos na tabela
        cursor.execute("SELECT COUNT(*) FROM Players WHERE Clube = 'Sporting'")
        if cursor.fetchone()[0] == 0:
            jogadores_sporting = [
                ('Antonio Adan', 'GK', 100, 'Sporting', random.randint(25, 100), random.randint(25, 100), random.randint(50, 100), random.randint(25, 100), random.randint(25, 100),0),
                ('Sebastian Coates', 'CB', 100, 'Sporting', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),1),
                ('Gonçalo Inácio', 'CB', 100, 'Sporting', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),2),
                ('Ricardo Esgaio', 'RB', 100, 'Sporting', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),3),
                ('Nuno Santos', 'LB', 100, 'Sporting', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),4),
                ('Pedro Gonçalves', 'CM', 100, 'Sporting', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),5),
                ('Manuel Ugarte', 'CDM', 100, 'Sporting', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),6),
                ('Hidemasa Morita', 'CM', 100, 'Sporting', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),7),
                ('Marcus Edwards', 'RW', 100, 'Sporting', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),8),
                ('Paulinho', 'ST', 100, 'Sporting', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),9),
                ('Trincão', 'LW', 100, 'Sporting', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),10)
            ]
            cursor.executemany("INSERT INTO Players (Nome, POS, COND, Clube, PosseBola, Desarme, BolasNasMaos, Passe, Finalizacao, Numero) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", jogadores_sporting)

        cursor.execute("SELECT COUNT(*) FROM Players WHERE Clube = 'FC Porto'")
        if cursor.fetchone()[0] == 0:
            jogadores_porto = [
                ('Diogo Costa', 'GK', 100, 'FC Porto', random.randint(25, 100), random.randint(25, 100), random.randint(50, 100), random.randint(25, 100), random.randint(25, 100),0),
                ('Pepe', 'CB', 100, 'FC Porto', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),1),
                ('David Carmo', 'CB', 100, 'FC Porto', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),2),
                ('João Mário', 'RB', 100, 'FC Porto', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),3),
                ('Wendell', 'LB', 100, 'FC Porto', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),4),
                ('Otávio', 'CM', 100, 'FC Porto', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),5),
                ('Stephen Eustaquio', 'CDM', 100, 'FC Porto', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),6),
                ('Marko Grujić', 'CM', 100, 'FC Porto', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),7),
                ('Pepe Aquino', 'RW', 100, 'FC Porto', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),8),
                ('Taremi', 'ST', 100, 'FC Porto', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),9),
                ('Galeno', 'LW', 100, 'FC Porto', random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100), random.randint(25, 100),10)
            ]
            cursor.executemany("INSERT INTO Players (Nome, POS, COND, Clube, PosseBola, Desarme, BolasNasMaos, Passe, Finalizacao, Numero) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", jogadores_porto)

        cursor.execute("UPDATE Players SET COND = 100")
        
        conn.commit()
        return conn

    except sqlite3.Error as e:
        print(e)
        return None

# Função para obter o nome dos times
def get_team():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Nome FROM Clube1")
            equipa1 = cursor.fetchone()[0]
            cursor.execute("SELECT Nome FROM Clube2")
            equipa2 = cursor.fetchone()[0]
            return equipa1, equipa2
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return None, None

# Função para carregar jogadores do banco de dados
def get_players(team_name):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Nome, POS, COND FROM Players WHERE Clube = ?", (team_name,))
            players_data = cursor.fetchall()
            return players_data
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return []

# Função para exibir informações de um jogador selecionado
def player_select(event, jogador_obj, team):
    if team == 1:
        team = "Sporting"
    else:
        team = "FC Porto"
    # Identifica qual listbox foi selecionado
    selected_listbox = event.widget
    
    # Verifica se há alguma seleção
    selection = selected_listbox.curselection()
    if not selection:
        return  # Se não houver seleção, sai da função
    
    # Pega o índice do jogador selecionado
    pos = selected_listbox.curselection()[0]  
    nn = selected_listbox.get(pos)  # Obtém a string com "POS - Nome"
    
    # Extrai o nome do jogador
    player_name = nn.split(' - ')[-1]  # Pega a última parte, que é o nome do jogador
    
    # Chama a janela para exibir detalhes do jogador
    playerwindow(player_name, jogador_obj, team)

def playerwindow(player_name, jogador_obj, team):
    global player_window
    # Verifica se a janela já está aberta
    if player_window is not None and player_window.winfo_exists():
        player_window.lift()  # Traz a janela para o foco
        return  # Se a janela já estiver aberta, não faz nada
    # Nova janela para exibir os detalhes do jogador
    player_window = Toplevel(root)
    player_window.title(f"Detalhes de {player_name}")
    player_window.geometry("400x330")  # Ajuste a altura para caber mais informações
    player_window.resizable(width=False, height=False)
    
    # Obtendo informações do jogador
    jogador_obj.getjogador(player_name, team)
    
    
    # Adicionando informações do jogador com grid para melhor layout
    Label(player_window, text="Nome:").grid(row=0, column=0, sticky=W, padx=10, pady=5)
    nome_label = Label(player_window, text=jogador_obj.nome, relief=SUNKEN, width=30)
    nome_label.grid(row=0, column=1, padx=10, pady=5, sticky=W)
    Label(player_window, text="Posição:").grid(row=1, column=0, sticky=W, padx=10, pady=5)
    pos_label = Label(player_window, text=jogador_obj.posicao, relief=SUNKEN, width=30)
    pos_label.grid(row=1, column=1, padx=10, pady=5, sticky=W)
    Label(player_window, text="Condição:").grid(row=2, column=0, sticky=W, padx=10, pady=5)
    cond_label = Label(player_window, text=str(jogador_obj.CT) + "%", relief=SUNKEN, width=30)
    cond_label.grid(row=2, column=1, padx=10, pady=5, sticky=W)
    Label(player_window, text="Clube:").grid(row=3, column=0, sticky=W, padx=10, pady=5)
    clube_label = Label(player_window, text=jogador_obj.Clube, relief=SUNKEN, width=30)
    clube_label.grid(row=3, column=1, padx=10, pady=5, sticky=W)
    Label(player_window, text="Posse de Bola:").grid(row=4, column=0, sticky=W, padx=10, pady=5)
    posse_bola_label = Label(player_window, text=jogador_obj.PossesBola, relief=SUNKEN, width=30)
    posse_bola_label.grid(row=4, column=1, padx=10, pady=5, sticky=W)
    Label(player_window, text="Desarme:").grid(row=5, column=0, sticky=W, padx=10, pady=5)
    desarme_label = Label(player_window, text=jogador_obj.Desarme, relief=SUNKEN, width=30)
    desarme_label.grid(row=5, column=1, padx=10, pady=5, sticky=W)
    Label(player_window, text="Bolas nas Mãos:").grid(row=6, column=0, sticky=W, padx=10, pady=5)
    bolas_maos_label = Label(player_window, text=jogador_obj.BolasNasMaos, relief=SUNKEN, width=30)
    bolas_maos_label.grid(row=6, column=1, padx=10, pady=5, sticky=W)
    Label(player_window, text="Passe:").grid(row=7, column=0, sticky=W, padx=10, pady=5)
    passe_label = Label(player_window, text=jogador_obj.Passe, relief=SUNKEN, width=30)
    passe_label.grid(row=7, column=1, padx=10, pady=5, sticky=W)
    Label(player_window, text="Finalização:").grid(row=8, column=0, sticky=W, padx=10, pady=5)
    finalizacao_label = Label(player_window, text=jogador_obj.Finalizacao, relief=SUNKEN, width=30)
    finalizacao_label.grid(row=8, column=1, padx=10, pady=5, sticky=W)
    # Botão para fechar a janela
    Button(player_window, text="Fechar", command=player_window.destroy).grid(row=10, column=0, columnspan=2, pady=10)
    # Botão para fechar a janela
    close_button = Button(player_window, text="Fechar", command=close_player_window)
    close_button.grid(row=10, column=0, columnspan=2, pady=10)
    # Ajuste do tamanho das colunas
    player_window.grid_columnconfigure(1, weight=1)
    # Adiciona o protocolo para limpar a variável quando a janela for fechada
    player_window.protocol("WM_DELETE_WINDOW", close_player_window)

def close_player_window():
    global player_window
    if player_window is not None:
        player_window.destroy()  # Destrói a janela
        player_window = None  # Limpa a referência da janela
    

def passoubola(jogador_obj, jogador_obj2):
    global scored, playercombola, playerpos, side, apitoFinal
    if apitoFinal:
        return
    if scored:
        return
    if side == "Sporting":
        jogador_obj.getjogador(listbox1.get(random.randint(1,10)).split(' - ')[-1], "Sporting")
        while True:
            jogador_obj2.getjogador(listbox1.get(random.randint(0,10)).split(' - ')[-1], "Sporting")
            if jogador_obj2.nome != jogador_obj.nome:
                break
        side = "Sporting"
    else:
        jogador_obj.getjogador(listbox2.get(random.randint(1,10)).split(' - ')[-1], "FC Porto")
        while True:
            jogador_obj2.getjogador(listbox2.get(random.randint(0,10)).split(' - ')[-1], "FC Porto")
            if jogador_obj2.nome != jogador_obj.nome:
                break
        side = "FC Porto"
    # Atualiza a mensagem para mostrar a falta
    update_game_message(f"{jogador_obj.nome}, passou a bola\n {jogador_obj2.nome} recebeu a bola!")
    
    
    # Atualizar o jogador que está com a bola e a sua posição
    jogador_obj.CT -= random.randint(0,3)
    jogador_obj2.CT -= random.randint(0,3)
    jogador_obj.updatejogador(jogador_obj.nome, jogador_obj.CT, jogador_obj.Clube)
    jogador_obj2.updatejogador(jogador_obj2.nome, jogador_obj2.CT, jogador_obj2.Clube)
    playercombola = jogador_obj2.nome
    playerpos = jogador_obj2.posicao
    
    # Limpar listas da interface e atualizar a condição dos jogadores
    listbox3.delete(0, "end")
    listbox6.delete(0, "end")
    refreshCOND(jogador_obj)
    root.after(300, lambda: game_control(jogador_obj, jogador_obj2))

# Função para registrar um gol
def marcou(jogador_obj, jogador_obj2):
    global scored, playercombola, playerpos, side, golos, golos2, apitoFinal
    if apitoFinal:
        return
    if scored:
        return
    if side == "Sporting":
        jogador_obj.getjogador(listbox1.get(random.randint(1,10)).split(' - ')[-1], "Sporting")
        golos += 1
    else:
        jogador_obj.getjogador(listbox2.get(random.randint(1,10)).split(' - ')[-1], "FC Porto")
        golos2 += 1
    update_golos()
    # Atualiza a mensagem para mostrar a falta
    update_game_message(game_message_label.cget("text")  + f"\nGOLO... do {jogador_obj.Clube} - Marcado por {playercombola}")
    # Atualiza os detalhes de quem marcou e a bola
    side = "Sporting"
    scored = True
    # Limpar listas e atualizar condições
    
    jogador_obj.CT -= random.randint(0,3)
    jogador_obj.updatejogador(jogador_obj.nome, jogador_obj.CT, jogador_obj.Clube)
    refreshCOND(jogador_obj)
    if side == "Sporting":
        jogador_obj.getjogador(listbox2.get(random.randint(1,10)).split(' - ')[-1], "FC Porto")
        side = "FC Porto"
    else:
        jogador_obj.getjogador(listbox1.get(random.randint(1,10)).split(' - ')[-1], "Sporting")
        side = "Sporting"
    playercombola = jogador_obj.nome
    playerpos = jogador_obj.posicao
    root.after(800, lambda: recomeco(jogador_obj, jogador_obj2))

def recomeco(jogador_obj, jogador_obj2):
    global scored, playercombola, playerpos, side, golos, golos2, apitoFinal
    if apitoFinal:
        return
    if not scored:
        return
    if side == "Sporting":
        jogador_obj.getjogador(listbox1.get(5).split(' - ')[-1], "Sporting")
        jogador_obj2.getjogador(listbox1.get(6).split(' - ')[-1], "Sporting")
    else:
        jogador_obj.getjogador(listbox2.get(5).split(' - ')[-1], "FC Porto")
        jogador_obj2.getjogador(listbox2.get(6).split(' - ')[-1], "FC Porto")
    # Atualiza a mensagem para mostrar a falta
    update_game_message(f"{jogador_obj.nome}, recomeça a partida passando a bola para {jogador_obj2.nome}")
    playercombola = jogador_obj2.nome
    playerpos = jogador_obj2.posicao
    scored = False
    root.after(300, lambda: game_control(jogador_obj, jogador_obj2))
    
def rematou(jogador_obj, jogador_obj2):
    global scored, playercombola, playerpos, side, golos, golos2
    if apitoFinal:
        return
    if scored:
        return
    if side == "Sporting":
        jogador_obj.getjogador(listbox1.get(random.randint(1,10)).split(' - ')[-1], "Sporting")
    else:
        jogador_obj.getjogador(listbox2.get(random.randint(1,10)).split(' - ')[-1], "FC Porto")
    # Atualiza a mensagem para mostrar a falta
    update_game_message(f"{jogador_obj.nome}, rematou!")

    # Limpar listas e atualizar condições
    listbox3.delete(0, "end")
    listbox6.delete(0, "end")
    jogador_obj.CT -= random.randint(0,3)
    jogador_obj.updatejogador(jogador_obj.nome, jogador_obj.CT, jogador_obj.Clube)
    refreshCOND(jogador_obj)
    i = random.randint(0,20)
    if i == 1 and i == 17:
        root.after(300, lambda: marcou(jogador_obj, jogador_obj2))
    else:
        root.after(300, lambda: defendeu(jogador_obj, jogador_obj2))
    
    

# Função para indicar quando um jogador falha ao tentar marcar
def falhou(jogador_obj, jogador_obj2):
    global scored, playercombola, playerpos, side, apitoFinal
    if apitoFinal:
        return
    if scored:
        return
    if side == "Sporting":
        jogador_obj.getjogador(listbox1.get(random.randint(1,10)).split(' - ')[-1], "Sporting")
        jogador_obj2.getjogador(listbox2.get(random.randint(1,10)).split(' - ')[-1], "FC Porto")
    else:
        jogador_obj.getjogador(listbox2.get(random.randint(1,10)).split(' - ')[-1], "FC Porto")
        jogador_obj2.getjogador(listbox1.get(random.randint(1,10)).split(' - ')[-1], "Sporting")
    # Atualiza a mensagem para mostrar a falta
    update_game_message(f"{jogador_obj.nome}, rematou, mas {jogador_obj2.nome} cortou a bola!")

    jogador_obj.CT -= random.randint(0,3)
    jogador_obj2.CT -= random.randint(0,3)
    jogador_obj.updatejogador(jogador_obj.nome, jogador_obj.CT, jogador_obj.Clube)
    jogador_obj2.updatejogador(jogador_obj2.nome, jogador_obj2.CT, jogador_obj2.Clube)
    # Define o jogador que vai cobrar o livre
    playercombola = jogador_obj2.nome
    playerpos = jogador_obj2.posicao
    side = jogador_obj2.Clube

    # Limpa a interface e atualiza as condições
    listbox3.delete(0, "end")
    listbox6.delete(0, "end")
    refreshCOND(jogador_obj)
    root.after(300, lambda: game_control(jogador_obj, jogador_obj2))

# Função para registrar uma falta
def falta(jogador_obj, jogador_obj2):
    global scored, playercombola, playerpos, side, apitoFinal
    if apitoFinal:
        return
    if scored:
        return
    if side == "Sporting":
        jogador_obj.getjogador(listbox1.get(random.randint(1,10)).split(' - ')[-1], "Sporting")
        jogador_obj2.getjogador(listbox2.get(random.randint(1,10)).split(' - ')[-1], "FC Porto")
    else:
        jogador_obj.getjogador(listbox2.get(random.randint(1,10)).split(' - ')[-1], "FC Porto")
        jogador_obj2.getjogador(listbox1.get(random.randint(1,10)).split(' - ')[-1], "Sporting")
    # Atualiza a mensagem para mostrar a falta
    update_game_message(f"{jogador_obj.nome}, sofreu uma falta\n {jogador_obj2.nome} vai marcar o livre!")

    jogador_obj.CT -= random.randint(0,4)
    jogador_obj2.CT -= random.randint(0,3)
    jogador_obj.updatejogador(jogador_obj.nome, jogador_obj.CT, jogador_obj.Clube)
    jogador_obj2.updatejogador(jogador_obj2.nome, jogador_obj2.CT, jogador_obj2.Clube)
    # Define o jogador que vai cobrar o livre
    playercombola = jogador_obj2.nome
    playerpos = jogador_obj2.posicao
    side = jogador_obj2.Clube
    
    # Limpa a interface e atualiza as condições
    listbox3.delete(0, "end")
    listbox6.delete(0, "end")
    refreshCOND(jogador_obj)

    # Simula uma jogada após a falta com chances de marcar gol ou perder
    if random.randint(1, 8) in [1, 7]:
        root.after(300, lambda: marcou(jogador_obj, jogador_obj2))
    else:
        root.after(300, lambda: defendeu(jogador_obj, jogador_obj2))


# Função que defende um remate
def defendeu(jogador_obj, jogador_obj2):
    global side, playercombola, playerpos, apitoFinal
    if apitoFinal:
        return
    if scored:
        return
    if side == "Sporting":
        jogador_obj.getjogador(listbox1.get(random.randint(1,10)).split(' - ')[-1], "Sporting")
        jogador_obj2.getjogador(listbox2.get(0).split(' - ')[-1], "FC Porto")
    else:
        jogador_obj.getjogador(listbox2.get(random.randint(1,10)).split(' - ')[-1], "FC Porto")
        jogador_obj2.getjogador(listbox1.get(0).split(' - ')[-1], "Sporting")
    update_game_message(f"{jogador_obj.nome}, rematou mas {jogador_obj2.nome} conseguiu defender!")
    jogador_obj.CT -= random.randint(0,3)
    jogador_obj2.CT -= random.randint(0,3)
    jogador_obj.updatejogador(jogador_obj.nome, jogador_obj.CT, jogador_obj.Clube)
    jogador_obj2.updatejogador(jogador_obj2.nome, jogador_obj2.CT, jogador_obj2.Clube)
    playercombola = jogador_obj2.nome
    playerpos = jogador_obj2.posicao
    side = jogador_obj2.Clube
    refreshCOND(jogador_obj)
    root.after(300, lambda: game_control(jogador_obj, jogador_obj2))

# Função que atualiza as condições dos jogadores
def refreshCOND(jogador_obj):
    listbox3.delete(0, "end")
    listbox6.delete(0, "end")
    i = 0
    while (i <= 10):
        player_name = listbox1.get(i).split(' - ')[-1]
        jogador_obj.getjogador(player_name, "Sporting")
        listbox3.insert(i, f"{jogador_obj.CT}%")
        i = i + 1
    i = 0
    while (i <= 10):
        player_name = listbox2.get(i).split(' - ')[-1]
        jogador_obj.getjogador(player_name, "FC Porto")
        listbox6.insert(i, f"{jogador_obj.CT}%")
        i = i + 1

# Função que controla o cronômetro do jogo
def gameCrono(jogador_obj, jogador_obj2):
    global intervalo, ingame, secs, mins, timing, parte, intervalotime, playercombola, playerpos, side, apitoFinal, descontos
    # Condições para parar o cronômetro no intervalo ou final de parte
    if mins >= 45 and parte == 1 and not intervalo:
        intervalo = True
        descontos = mins - 45
        mins = 45
        secs = 0
        update_parte_label("INTERVALO")
        update_game_message("Árbitro apita para o intervalo")
        update_tempo_label()
    if mins >= 90 and parte == 2 and not apitoFinal:
        queroDescontos = random.randint(2, 8)
        if mins >= (90+queroDescontos):
            apitoFinal = True
            intervalo = False
            ingame = False
            descontos = mins - 90
            mins = 90
            secs = 0
            update_parte_label("APITO FINAL")
            update_game_message("Árbitro apita para o final do jogo")
            update_tempo_label()
    if intervalo:
        intervalotime += 10
        if intervalotime >= 20:
            parte = 2
            if team_start == "Sporting":
                player_name = listbox2.get(5).split(' - ')[-1]
                player_name2 = listbox2.get(6).split(' - ')[-1]
                jogador_obj.getjogador(player_name, "Sporting")
                jogador_obj2.getjogador(player_name2,"Sporting")
                side = "FC Porto"
            else:
                player_name = listbox1.get(5).split(' - ')[-1]
                player_name2 = listbox1.get(6).split(' - ')[-1]
                jogador_obj.getjogador(player_name, "FC Porto")
                jogador_obj2.getjogador(player_name2,"FC Porto")
                side = "Sporting"
            update_game_message(f"{jogador_obj.nome}, recomeça a partida passando a bola para {jogador_obj2.nome}")
            playercombola = jogador_obj2.nome
            playerpos = jogador_obj2.posicao
            intervalo = False
            update_parte_label(parte)
            update_tempo_label()
    if not intervalo and not apitoFinal and ingame and not scored:
        # Simulação do cronômetro avançando
        timing += 10
        if timing >= 10:
            secs += random.randint(30, 60)
            if secs >= 60:
                secs -= 60
                mins += 1
        update_tempo_label()
    root.after(500, lambda: gameCrono(jogador_obj, jogador_obj2))
        
# Função que controla o início e o desenvolvimento do jogo
def playgame(jogador_obj, jogador_obj2):
    global team_start
    if listbox1.get(0) == "":
        messagebox.showwarning("ERRO", "Não podes iniciar o jogo sem carregar as equipas primeiro.")
        return
    global playercombola, side, playerpos, rematabola, passabola, intervalo, ingame, scored, parte, team_start, descontos
    descontos = 0
    if not intervalo and not ingame:
        # Escolher qual time começa
        team_start = random.choice(["Sporting", "FC Porto"])
        if team_start == "Sporting":
            player_name = listbox1.get(5).split(' - ')[-1]
            player_name2 = listbox1.get(6).split(' - ')[-1]
            jogador_obj.getjogador(player_name, "Sporting")
            jogador_obj2.getjogador(player_name2,"Sporting")
            side = "Sporting"
        else:
            player_name = listbox2.get(5).split(' - ')[-1]
            player_name2 = listbox2.get(6).split(' - ')[-1]
            jogador_obj.getjogador(player_name, "FC Porto")
            jogador_obj2.getjogador(player_name2,"FC Porto")
            side = "FC Porto"
        playercombola = jogador_obj2.nome
        playerpos = jogador_obj2.posicao
        update_game_message(f"{jogador_obj.nome}, começa a partida passando a bola para {jogador_obj2.nome}")
        parte = 1
        ingame = True
        update_parte_label(parte)
        update_tempo_label()
        gameCrono(jogador_obj, jogador_obj2)
        root.after(100, lambda: game_control(jogador_obj, jogador_obj2))
                 
def game_control(jogador_obj, jogador_obj2):
    opcao = random.randint(0,3)
    match opcao:
        case 0:
            rematou(jogador_obj, jogador_obj2)
        case 1:
            falhou(jogador_obj, jogador_obj2)
        case 2:
            falta(jogador_obj, jogador_obj2)
        case 3:
            passoubola(jogador_obj, jogador_obj2)

# Função para atualizar o texto da mensagem do jogo
def update_game_message(message):
    global side
    game_message_label.config(text=message)
    if side == "Sporting":
        game_message_label.config(bg="green", fg="white")
    else:
        game_message_label.config(bg="blue", fg="white")

# Função para atualizar o texto da parte do jogo
def update_parte_label(parte):
    if parte == "INTERVALO" or parte == "APITO FINAL":
        parte_label.config(text=f"{parte}")
    else:
        parte_label.config(text=f"{parte}º Parte")
        
def update_golos():
    global golos, golos2
    golos_label.config(text=f"{golos}")
    golos_label2.config(text=f"{golos2}")
    
# Função para atualizar o texto da parte do jogo
def update_tempo_label():
    global mins, secs
    fmins = 0
    fsecs = 0
    if mins < 10:
        fmins = "0" + str(mins)
    else:
        fmins = str(mins)
    if secs < 10:
        fsecs = "0" + str(secs)
    else:
        fsecs = str(secs)
    if descontos == 0:
        tempo_label.config(text=f"{fmins}:{fsecs}")
    else:
        tempo_label.config(text=f"{fmins}:{fsecs}({descontos})")

# Função para iniciar a interface do jogo
def start_game_interface():
    global root, listbox1, listbox2, listbox3, listbox6, game_message_label, parte_label, tempo_label, golos, golos_label, golos_label2

    root = Tk()  # Inicializa o Tkinter
    root.title("Simulação de Futebol")
    root.geometry("800x600")
    
    jogador_obj = Jogador()
    jogador_obj2 = Jogador()
    
    # Labels para Time 1 e Time 2
    equipa1, equipa2 = get_team()  # Função que retorna os nomes dos times
    Label(root, text=f"Equipa 1: {equipa1}").pack()
    Label(root, text=f"Equipa 2: {equipa2}").pack()
    
    # Labels Resultado
    Label(root, text=f"{equipa1}").place(x=250, y=70)  # Label de título
    golos_label = Label(root, text=f"{golos}", bg="black", fg="red", font=('Helvetica', 15, 'bold'), width=7, height=3)
    golos_label.place(x=230, y=100)  # Label para a mensagem do jogo ocupando toda a largura
    
    Label(root, text=f"{equipa2}").place(x=350, y=70)  # Label de título
    golos_label2 = Label(root, text=f"{golos2}", bg="black", fg="red", font=('Helvetica', 15, 'bold'), width=7, height=3)
    golos_label2.place(x=330, y=100)  # Label para a mensagem do jogo ocupando toda a largura
    
    # Labels para Mensagem do Jogo
    Label(root, text="Mensagem do Jogo:").place(x=10, y=430)  # Label de título
    game_message_label = Label(root, text="", bg="lightgray", width=110, height=5, wraplength=600)
    game_message_label.place(x=10, y=450)  # Label para a mensagem do jogo ocupando toda a largura
    
    

    # Listboxes para mostrar informações dos times e jogadores
    Label(root, text=f"{equipa1}", font=('Helvetica', 10, 'bold')).place(x=50, y=200)
    listbox1 = Listbox(root, width=20, height=10)  # Time 1 - nomes
    listbox1.pack(side=LEFT, padx=10, pady=10)
    Label(root, text="Condição Física", font=('Helvetica', 10, 'bold')).place(x=150, y=200)
    listbox3 = Listbox(root, width=20, height=10)  # Time 1 - condição física
    listbox3.pack(side=LEFT, padx=10, pady=10)
    
    Label(root, text=f"{equipa2}", font=('Helvetica', 10, 'bold')).place(x=300, y=200)
    listbox2 = Listbox(root, width=20, height=10)  # Time 2 - nomes
    listbox2.pack(side=LEFT, padx=10, pady=10)
    Label(root, text="Condição Física", font=('Helvetica', 10, 'bold')).place(x=450, y=200)
    listbox6 = Listbox(root, width=20, height=10)  # Time 2 - condição física
    listbox6.pack(side=LEFT, padx=10, pady=10)

    # Função para carregar jogadores nos listboxes
    def load_teams():
        players1 = get_players(equipa1)  # Função que retorna a lista de jogadores do time 1
        players2 = get_players(equipa2)  # Função que retorna a lista de jogadores do time 2

        # Carrega os jogadores na Listbox do Time 1
        listbox1.delete(0, END)  # Limpa a listbox antes de carregar
        listbox3.delete(0, END)  # Limpa a listbox de condição física também
        for player in players1:
            listbox1.insert(END, f"{player[1]} - {player[0]}")  # Insere POS e Nome
            listbox3.insert(END, f"{player[2]}%")  # Insere a condição física (simulando valor entre 0 e 100)

        # Carrega os jogadores na Listbox do Time 2
        listbox2.delete(0, END)  # Limpa a listbox antes de carregar
        listbox6.delete(0, END)  # Limpa a listbox de condição física também
        for player in players2:
            listbox2.insert(END, f"{player[1]} - {player[0]}")  # Insere POS e Nome
            listbox6.insert(END, f"{player[2]}%")  # Insere a condição física (simulando valor entre 0 e 100)

    Button(root, text="Carregar Jogadores", command=load_teams).pack(pady=10)

    # Botão para iniciar o jogo
    Button(root, text="Iniciar Jogo", command=lambda: playgame(jogador_obj, jogador_obj2)).pack(pady=10)

    # Labels para Mensagem do Jogo
    Label(root, text="Mensagem do Jogo:").place(x=10, y=430)  # Label de título
    game_message_label = Label(root, text="", bg="lightgray", width=110, height=5, wraplength=600)
    game_message_label.place(x=10, y=450)  # Label para a mensagem do jogo ocupando toda a largura

    # Parte do jogo (Primeira parte, Segunda parte, Intervalo, etc.)
    Label(root, text="Parte do Jogo:").pack(pady=5)
    parte_label = Label(root, text="Jogo não começou", font=("Helvetica", 14), fg="blue")
    parte_label.pack(pady=5)
    
    # Tempo Percorrido
    Label(root, text="Tempo Percorrido:").place(x=640, y=230)  # Label de título
    tempo_label = Label(root, text="", font=("Helvetica", 20), bg="black", fg="yellow", width=7, height=2)
    tempo_label.place(x=635, y=250)  # Ajusta a posição do tempo_label

    # Ligação do evento de seleção
    listbox1.bind('<<ListboxSelect>>', lambda event: player_select(event, jogador_obj, 1))
    listbox2.bind('<<ListboxSelect>>', lambda event: player_select(event, jogador_obj, 2))
    update_tempo_label()

    root.mainloop()

if __name__ == "__main__":
    start_game_interface()