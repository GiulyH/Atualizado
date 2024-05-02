from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.graphics import Rectangle, Line
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.spinner import SpinnerOption
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Criar a tabela 'users' se ela não existir
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    last_name TEXT,
                    email TEXT,
                    password TEXT
                  )''')

# Commit e fechar a conexão
conn.commit()
conn.close()

# Definindo cores
primary_color = get_color_from_hex("#4CAF50")  # verde
secondary_color = get_color_from_hex("#FFC107")  # amarelo
background_color = get_color_from_hex("#FFFFFF")  # branco
text_color = get_color_from_hex("#FFFFFF")  # branco
Window.clearcolor = background_color

from kivy.uix.floatlayout import FloatLayout

class RegisterScreen(Screen):

    def register_user(self, instance):
        # Verificar se todos os campos estão preenchidos
        if not all(field.text.strip() for field in [self.name_input, self.last_name_input, self.email_input, self.password_input, self.repeat_password_input]):
            self.show_popup("Erro", "Todos os campos são obrigatórios.")
            return

        # Verificar se as senhas coincidem
        if self.password_input.text != self.repeat_password_input.text:
            self.show_popup("Erro", "As senhas não coincidem.")
            return

        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Verificar se o email já está cadastrado
        cursor.execute("SELECT * FROM users WHERE email=?", (self.email_input.text,))
        if cursor.fetchone():
            self.show_popup("Erro", "Este e-mail já está registrado.")
            conn.close()
            return

        # Inserir os detalhes do usuário no banco de dados
        cursor.execute("INSERT INTO users (name, last_name, email, password) VALUES (?, ?, ?, ?)",
                       (self.name_input.text, self.last_name_input.text, self.email_input.text, self.password_input.text))
        conn.commit()

        # Fechar a conexão com o banco de dados
        conn.close()

        # Após o registro, retornar à tela de login
        self.parent.current = 'login'

    def go_back_to_login(self, instance):
        self.parent.current = 'login'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        # Adicionar imagem de fundo
        with layout.canvas.before:
            self.background = Rectangle(source='Cadastro.png', pos=layout.pos, size=layout.size)

        text_color = (1, 1, 1, 1)  # Cor do texto

        # Campo de entrada para nome
        self.name_input = TextInput(hint_text="Seu nome", multiline=False, background_color=(0, 0, 0, 0), foreground_color=text_color, size_hint=(None, None), size=(150, 30))
        self.name_input.pos_hint = {'center_x': 0.1, 'center_y': 0.6}

        # Campo de entrada para sobrenome
        self.last_name_input = TextInput(hint_text="Seu sobrenome", multiline=False, background_color=(0, 0, 0, 0), foreground_color=text_color, size_hint=(None, None), size=(155, 80))
        self.last_name_input.pos_hint = {'center_x': 0.1, 'center_y': 0.4}

        # Campo de entrada para e-mail
        self.email_input = TextInput(hint_text="E-mail", multiline=False, background_color=(0, 0, 0, 0), foreground_color=text_color, size_hint=(None, None), size=(150,135))
        self.email_input.pos_hint = {'center_x': 0.1, 'center_y': 0.2}

        # Campo de entrada para senha
        self.password_input = TextInput(hint_text="Senha", password=True, multiline=False, background_color=(0, 0, 0, 0), foreground_color=text_color, size_hint=(None, None), size=(300, 40))
        self.password_input.pos_hint = {'center_x': 0.7, 'center_y': 0.6}

        # Campo de entrada para repetir a senha
        self.repeat_password_input = TextInput(hint_text="Repita a Senha", password=True, multiline=False, background_color=(0, 0, 0, 0), foreground_color=text_color, size_hint=(None, None), size=(300, 29))
        self.repeat_password_input.pos_hint = {'center_x': 0.7, 'center_y': 0.5}

        # Adicionar CheckBoxes para seleção de gênero
        self.gender_female = CheckBox(group='gender', size_hint=(None, None), size=(30, 30))
        self.gender_female.pos_hint = {'center_x': 0.77, 'center_y': 0.35}

        self.gender_male = CheckBox(group='gender', size_hint=(None, None), size=(30, 30))
        self.gender_male.pos_hint = {'center_x': 0.67, 'center_y': 0.35}

        self.gender_other = CheckBox(group='gender', size_hint=(None, None), size=(30, 30))
        self.gender_other.pos_hint = {'center_x': 0.57, 'center_y': 0.35}

        # Adicionar TextInput para outros gêneros
        self.other_gender_input = TextInput(hint_text="Outro (especifique)", multiline=False, background_color=(0, 0, 0, 0), opacity=0, foreground_color=text_color, size_hint=(None, None), size=(200, 30))
        self.other_gender_input.pos_hint = {'center_x': 0.5, 'center_y': 0.1}

        # Botão de registro
        self.register_button = Button(text="Registrar", background_normal='', size_hint=(None, None), size=(100, 50), background_color=(0, 0, 0, 0), color=text_color)
        self.register_button.bind(on_press=self.register_user)
        self.register_button.pos_hint = {'center_x': 0.61, 'center_y': 0.25}

        # Botão de voltar
        back_button = Button(text="Voltar", size_hint=(None, None), size=(100, 50), background_color=(0, 0, 0, 0))
        back_button.bind(on_press=self.go_back_to_login)
        back_button.pos_hint = {'center_x': 0.6, 'center_y': 0.05}

        # Adicionar widgets ao layout
        layout.add_widget(Label(text="Cadastre-se", font_size=36, color=(1, 1, 1, 1), size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.9}))
        layout.add_widget(self.name_input)
        layout.add_widget(self.last_name_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.repeat_password_input)
        layout.add_widget(self.gender_female)
        layout.add_widget(self.gender_male)
        layout.add_widget(self.gender_other)
        layout.add_widget(self.other_gender_input)
        layout.add_widget(self.register_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

        # Atualizar o tamanho da imagem de fundo quando a janela for redimensionada
        self.bind(size=self._update_background_size)

    def _update_background_size(self, instance, value):
        self.background.size = instance.size


from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        # Adicionar imagem de fundo
        with layout.canvas.before:
            self.background = Rectangle(source='TelaLogin.jpg', pos=layout.pos, size=layout.size)

        text_color = (1, 1, 1, 1)  # Cor do texto

        # Definir tamanho dos campos de e-mail e senha
        self.email_input = TextInput(hint_text="E-mail", multiline=False, background_color=(0, 0, 0, 0),
                                      size_hint=(None, None), size=(150, 50), font_size=15,
                                      foreground_color=text_color, pos_hint={'x': 0, 'y': 0.5})
        self.password_input = TextInput(hint_text="Senha", password=True, background_color=(0, 0, 0, 0),
                                         multiline=False, size_hint=(None, None), size=(150, 45),
                                         font_size=15, foreground_color=text_color, pos_hint={'x': 0, 'y': 0.4})

        # Adicionar os campos de e-mail e senha
        layout.add_widget(Label(text="Student Academy Platform", font_size=50, color=(1, 1, 1, 1),
                                pos_hint={'x': 0.2, 'y': 0.7}))
        layout.add_widget(self.email_input)
        layout.add_widget(self.password_input)

        # Posicionar os botões "Registrar" e "Esqueci a senha" lado a lado acima do botão "Entrar"
        register_button = Button(text="Registrar", font_size=13, size_hint=(None, None), size=(40, 40),
                                 background_normal='', background_color=(0, 0, 0, 0), color=text_color,
                                 pos_hint={'x': 0.02, 'y': 0.35})
        register_button.bind(on_press=self.go_to_register)  # Alterada a função para ir para a tela de registro

        forgot_password_button = Button(text="Esqueci a senha",font_size=13, size_hint=(None, None), size=(150, 40),
                                         background_normal='', background_color=(0, 0, 0, 0), color=text_color,
                                         pos_hint={'x': 0.15, 'y': 0.35})
        forgot_password_button.bind(on_press=self.go_to_forgot_password)

        login_button = Button(text="Entrar", background_normal='', size_hint=(None, None), size=(90, 70),
                              background_color=(0, 0, 0, 0), color=text_color, pos_hint={'x': 0.10, 'y': 0.2})
        login_button.bind(on_press=self.check_login)

        # Adicionar os botões ao FloatLayout
        layout.add_widget(register_button)
        layout.add_widget(forgot_password_button)
        layout.add_widget(login_button)
        self.add_widget(layout)
        layout.add_widget(Label(text="Student Academy Platform", font_size=36, color=(1, 1, 1, 1), font_name='BebasNeue-Regular.otf',
                        pos_hint={'center_x': 0.5, 'y': 0.3}))


    def update_line(self, instance, value):
        instance.canvas.after.clear()
        with instance.canvas.after:
            Line(points=[instance.x, instance.y, instance.right, instance.y], width=2)

    def on_size(self, *args):
        self.background.size = self.size
        self.background.pos = self.pos

    def check_login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        # Verificar se o email e a senha foram fornecidos
        if not email or not password:
            self.show_popup("Erro", "Por favor, insira o e-mail e a senha.")
            return

        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Verificar se o usuário existe no banco de dados
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()

        # Fechar a conexão com o banco de dados
        conn.close()

        if user:
            print("Login bem-sucedido")
            self.parent.current = 'home'
        else:
            self.show_popup("Login Falhou", "Usuário ou senha incorretos.")

    def go_to_register(self, instance):
        self.parent.current = 'register'  # Alterado para ir para a tela de registro

    def go_to_forgot_password(self, instance):
        self.parent.current = 'forgot_password'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()


class ForgotPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', spacing=10, padding=(30, 30, 30, 30))

        self.email_input = TextInput(hint_text="E-mail", multiline=False, background_color=(1, 1, 1, 0.8), size_hint=(None, None), size=(100, 40), font_size=18)
        recover_button = Button(text="Recuperar Senha", background_normal='', size_hint=(None, None), size=(100, 40), background_color=(0, 0, 0, 0), color=text_color)
        recover_button.bind(on_press=self.recover_password)
        back_button = Button(text="Voltar", size_hint=(None, None), size=(100, 40), background_normal='', background_color=(0, 0, 0, 0), color=text_color)
        back_button.bind(on_press=self.go_back_to_login)

        layout.add_widget(Label(text="Esqueci a Senha", font_size=36, color=(1, 1, 1, 1)))
        layout.add_widget(self.email_input)
        layout.add_widget(recover_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def recover_password(self, instance):
        # Por enquanto, vamos apenas exibir uma mensagem
        self.show_popup("Recuperar Senha", "Instruções de recuperação de senha enviadas para o seu e-mail.")

    def go_back_to_login(self, instance):
        self.parent.current = 'login'

    def show_popup(self, title, content):
        popup = Popup(title=title, content=Label(text=content), size_hint=(None, None), size=(400, 200))
        popup.open()
        
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')

        # Add tabs
        tabs = TabbedPanel(do_default_tab=False)
        tabs.add_widget(TabbedPanelHeader(text='Cursos'))
        tabs.add_widget(TabbedPanelHeader(text='Trilhas'))
        tabs.add_widget(TabbedPanelHeader(text='Comunidade'))
        tabs.add_widget(TabbedPanelHeader(text='Perguntas'))
        tabs.add_widget(TabbedPanelHeader(text='Artigos'))
        layout.add_widget(tabs)

        search_bar = TextInput(hint_text='Pesquisar...')
        layout.add_widget(search_bar)

        level_panel = BoxLayout(orientation='vertical')
        level_panel.add_widget(Label(text='Nível'))
        level_panel.add_widget(Button(text='Iniciante'))
        level_panel.add_widget(Button(text='Intermediário'))
        level_panel.add_widget(Button(text='Avançado'))
        layout.add_widget(level_panel)

        categories = GridLayout(cols=2)
        categories.add_widget(Label(text='Saúde'))
        categories.add_widget(Button(text='Saiba Mais'))
        categories.add_widget(Label(text='Gestão'))
        categories.add_widget(Button(text='Saiba Mais'))
        categories.add_widget(Label(text='Programação'))
        categories.add_widget(Button(text='Saiba Mais'))
        layout.add_widget(categories)

        self.add_widget(layout)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(ForgotPasswordScreen(name='forgot_password'))
        sm.add_widget(HomeScreen(name='home')) 
        return sm
    
if __name__ == "__main__":
    MyApp().run()
