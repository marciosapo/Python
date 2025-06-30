import sqlite3

class Jogador:
    def __init__(self):
        self.nome = ""
        self.posicao = ""
        self.CT = 0
        self.Clube = ""
        self.ST = ""
        self.CORD = ""
        self.TK = 0
        self.PossesBola = 0
        self.Desarme = 0
        self.BolasNasMaos = 0
        self.Passe = 0
        self.Finalizacao = 0
        self.numero = 0

    def getjogador(self, player_name, team):
        try:
            conn = sqlite3.connect('basedados.db')
            cursor = conn.cursor()
            
            # A consulta que busca o jogador pelo nome
            cursor.execute("SELECT Nome, POS, COND, Clube, PosseBola, Desarme, BolasNasMaos, Passe, Finalizacao, id, Numero FROM Players WHERE Nome = ? AND Clube = ?", (player_name, team,))
            player_data = cursor.fetchone()
            
            if player_data:
                self.nome = player_data[0]
                self.posicao = player_data[1]
                self.CT = player_data[2]
                self.Clube = player_data[3]
                self.PossesBola = player_data[4]
                self.Desarme = player_data[5]
                self.BolasNasMaos = player_data[6]
                self.Passe = player_data[7]
                self.Finalizacao = player_data[8]
                self.numero = player_data[9]     
            else:
                print(f"Jogador '{player_name}' não encontrado.")

        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
        finally:
            conn.close()
    def updatejogador(self, player_name, CT, team):
        try:
            conn = sqlite3.connect('basedados.db')
            cursor = conn.cursor()
            
            # A consulta que atualiza os dados do jogador na base de dados
            cursor.execute("""
                UPDATE Players SET COND = ? WHERE Nome = ? AND Clube = ?
            """, (CT, player_name, team))
            
            conn.commit()  # Confirma as alterações no banco de dados
            if cursor.rowcount > 0:
                print("Dados do jogador atualizados com sucesso.")
            else:
                print("Nenhum dado foi atualizado. Verifique se o jogador existe.")

        except sqlite3.Error as e:
            print(f"Erro ao atualizar o banco de dados: {e}")
        finally:
            conn.close()