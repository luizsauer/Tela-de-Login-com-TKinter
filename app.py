import sqlite3
import customtkinter as ctk
from tkinter import PhotoImage, END
from tkinter import messagebox

#! classe para conectar no banco de dados
class BackEnd():
    def conecta_db(self):
        self.conn = sqlite3.connect("Sistema_cadastros.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados Conectado")
    
    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados Desconectado")

    def cria_tabela(self):
        self.conecta_db()
        
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS Usuarios(
                                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                                Username TEXT NOT NULL,
                                Email TEXT NOT NULL,
                                Senha TEXT NOT NULL,
                                Confirma_senha TEXT NOT NULL
                            );
                            """)
        self.conn.commit()
        print("Tabela criada com sucesso!")
        self.desconecta_db()



    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()  # get busca a informaçao do username_cadastro_entry
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_entry.get()
        
        self.conecta_db()
        self.cursor.execute("""
                            INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha)
                            VALUES (?, ?, ?, ?)
                            """, (self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha_cadastro))
        
        try:
            if (self.username_cadastro == "" or self.email_cadastro == "" or self.senha_cadastro == "" or self.confirma_senha_cadastro == ""):
                messagebox.showerror(title="Sistema de Login", message="ERRO!!!\nPor favor preencha todos os campos!")
            elif (len(self.username_cadastro) < 4):
                messagebox.showwarning(title="Sistema de Login", message="O nome de usuario deve ter de pelo menos 4 caracteres.")
            elif (len(self.senha_cadastro) < 4):
                messagebox.showwarning(title="Sistema de Login", message="A senha deve ser ter pelo menos 4 caracteres.")
            elif (self.senha_cadastro != self.confirma_senha_cadastro):
                messagebox.showerror(title=" Sistema de Login", message="ERRO!!!\nAs senhas não são iguais!")
            else:
                self.conn.commit()
                messagebox.showinfo(title="Sistema de Login", message=f"Parabens {self.username_cadastro}\nOs seus dados foram cadastrados com sucesso!")
                self.desconecta_db()
                self.limpa_entry_cadastro()
        except:
            messagebox.showerror(title="Sistema de Login", message="Erro no processamento do seu cadastro!\nPor favor tente novamente!")
            self.desconecta_db()


    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()
        
        self.conecta_db()
        
        self.cursor.execute("""SELECT * FROM Usuarios 
                            WHERE (Username = ? AND Senha = ?)""", (self.username_login, self.senha_login))
        
        self.verifica_dados = self.cursor.fetchone() # fetch"ONE" faz a busca por apenas um dado no banco de dados
        try:
            if (self.username_login == "" or self.senha_login == ""):
                messagebox.showwarning(title="Sistema de Login", message="Por favor preencha todos os campos")
            elif (self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados):  #verifica se o username e senha tem no db
                messagebox.showinfo(title="Sistema de Login", message=f"Parabens {self.username_login} \nLogin feito com sucesso!")
                self.desconecta_db()
                self.limpa_entrey_login()
            else:
                messagebox.showerror(title="Sistema de Login", message="ERRO!!!\nDados não encontrados no sistema.\nPor favor verifique os seus dados ou cadastre-se")
                self.desconecta_db()
        
        except sqlite3.Error as e:
            messagebox.showerror(title="Sistema de Login", message=f"Erro ao acessar o banco de dados: {e}")
            self.desconecta_db()
        
        

#! classe inicial do FrontEnd
class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        # ctk.CTk.__init__(self)  # Chame o __init__() da classe mãe ctk.CTk
        # BackEnd.__init__(self)  # Chame o __init__() da classe mãe BackEnd
        self.configuracoes_da_janela_inicial()
        self.tela_de_login()
        self.cria_tabela()
    
    #configurando a janela principal
    def configuracoes_da_janela_inicial(self):
        self.geometry("700x400")
        self.title("Sistema de Login")
        self.resizable(False, False) # falso pra altura e largura
    
    def tela_de_login(self):
        
        #trabalhando com as imagens
        self.img = PhotoImage(file="logi-img.png")  # puxa a imagem
        self.img = self.img.subsample(6,6) # redimensiona a imagem
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10) #padx é o padding de 10px
        
        #titulo da plataforma
        self.title = ctk.CTkLabel(self, text="Faça o seu login ou cadastre-se\nna nossa plataforma para acesar\nos nossos serviços!", font=("Century Gothic bold", 14))
        self.title.grid(row=0, column=0, pady=10, padx=10)
        
        #criando a frame do formuladio de login
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=10)
        
        #criando o titulo do frame formulario
        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça o seu Login", font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, pady=10, padx=10)
        
        #colocando widgets dentro do frame - formulario de login
        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Seu nome de Usuário", font=("Century Gothic bold", 16), corner_radius=15)
        self.username_login_entry.grid(row=1, column=0, pady=10, padx=10)
        
        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Sua senha", font=("Century Gothic bold", 16), corner_radius=15, show="*")
        self.senha_login_entry.grid(row=2, column=0, pady=10, padx=10)
        
        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Clique para ver a senha", font=("Century Gothic bold", 14), corner_radius=20)
        self.ver_senha.grid(row=3, column=0, pady=10, padx=10)
        
        self.btn_login = ctk.CTkButton(self.frame_login, text="Fazer Login".upper(), font=("Century Gothic bold", 14), corner_radius=15, command=self.verifica_login)
        self.btn_login.grid(row=4, column=0, pady=10, padx=10)
        
        self.span = ctk.CTkLabel(self.frame_login, text="Se não tem conta, clique no botão abaixo para poder se \nCadastrar no nosso sistema!", font=("Century Gothic bold", 10))
        self.span.grid(row=5, column=0, pady=10, padx=10)
        
        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=300, fg_color="green", hover_color="#050", text="Fazer Cadastro".upper(), font=("Century Gothic bold", 14), corner_radius=15, command=self.tela_de_cadastro)
        self.btn_cadastro.grid(row=6, column=0, pady=10, padx=10)
    
    def tela_de_cadastro(self):
        
        #remover o formulario de login
        self.frame_login.place_forget()
        
        #criando o frame de formulario de Cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350, y=10)
        
        #criando o titulo do frame de cadastro
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça o seu Cadastro", font=("Century Gothic bold", 22))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)
        
        #criando os widgets da tela de cadastro
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu nome de usuário", font=("Century Gothic bold", 16), corner_radius=15)
        self.username_cadastro_entry.grid(row=1, column=0, padx=5, pady=10)
        
        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Seu email", font=("Century Gothic bold", 16), corner_radius=15)
        self.email_cadastro_entry.grid(row=2, column=0, padx=5, pady=10)
        
        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Sua senha", font=("Century Gothic bold", 16), corner_radius=15, show="*")
        self.senha_cadastro_entry.grid(row=3, column=0, padx=5, pady=10)
        
        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Confirme sua senha", font=("Century Gothic bold", 16), corner_radius=15, show="*")
        self.confirma_senha_entry.grid(row=4, column=0, padx=5, pady=10)
        
        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Clique para ver a senha", font=("Century Gothic bold", 14), corner_radius=20)
        self.ver_senha.grid(row=5, column=0, pady=10)
        
        self.btn_cadastrar_user = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="green", hover_color="#050", text="Fazer Cadastro".upper(), font=("Century Gothic bold", 14), corner_radius=15, command=self.cadastrar_usuario)
        self.btn_cadastrar_user.grid(row=6, column=0, padx=5, pady=10)
        
        self.btn_lobin_back = ctk.CTkButton(self.frame_cadastro, width=300, fg_color="#444", hover_color="#333", text="Voltar a Login".upper(), font=("Century Gothic bold", 14), corner_radius=15, command=self.tela_de_login)
        self.btn_lobin_back.grid(row=7, column=0, padx=10, pady=10)
    
    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)
        
    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
