from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
import pyautogui


class PlaylistUltimato:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("lang=pt-BR")
        path = 'D:\DOWNLOADS\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=path, chrome_options=options)
        self.wait = WebDriverWait(
            self.driver,
            10,
            poll_frequency=1,
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException,
            ],
        )
        self.link_spofity = ""
        self.DeveUsarLoginFacebook = False
        self.email = ""
        self.senha = ""

    def obterInfos(self):
        self.DeveUsarLoginFacebook = False
        self.email = "email@email.com"
        self.senha = "senha123456"
        self.link_spofity = "https://open.spotify.com/playlist/3l2RrQaxL6feRQepsC92GE"
        self.nome_playlist_nova = "Minha playlist"
        # if pyautogui.confirm('Como deseja fazer login?', "Login", ['Spotfy', 'Facebook']) == "Facebook":
        #     self.DeveUsarLoginFacebook = True
        # self.email = pyautogui.prompt('Qual de nome de Usuario?')
        # self.senha = pyautogui.password('Qual sua senha?')
        # self.link_spofity = pyautogui.prompt('Qual o link da playlist origem?')
        # self.nome_playlist_nova = pyautogui.prompt('Qual o nome da playlist destino?')
        #https: // open.spotify.com / playlist / 0ac71TW9B8eyrSKN16sbk0

    def Start(self):
        self.obterInfos()
        self.driver.get(self.link_spofity)
        time.sleep(2)
        self.LoginSpotify()
        if self.DeveUsarLoginFacebook == True:
            self.LogarComFacebook()
        else:
            self.LogarComEmail()
        time.sleep(5)
        self.ClicarNoMenuOpcoes()

    def LoginSpotify(self):
        print("Loggando no Spotify")
        login_button = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (By.XPATH, '//button[text()="Entrar"]')
            )
        )
        login_button.click()

    def LogarComEmail(self):
        campo_email = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//input[@name="username"]')))
        campo_senha = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//input[@name="password"]')))
        botao_entrar = self.wait.until(
            CondicaoExperada.element_to_be_clickable((By.XPATH, '//button[text()="Entrar"]')))

        campo_email.send_keys(self.email)
        time.sleep(0.5)
        campo_senha.send_keys(self.senha)
        time.sleep(0.5)
        botao_entrar.click()

    def LogarComFacebook(self):
        print("logando no facebook")
        botao_logar_com_facebook = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (By.XPATH, '//a[text()="Continuar com o Facebook"]')
            )
        )
        botao_logar_com_facebook.click()
        self.InserirDadosLoginFacebook()

    def InserirDadosLoginFacebook(self):
        campo_email = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//input[@name="email"]')))
        campo_senha = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//input[@name="pass"]')))
        botao_login = self.wait.until(CondicaoExperada.element_to_be_clickable((By.XPATH, '//button[@name="login"]')))

        campo_email.clear()
        self.digite_como_uma_pessoa(self.email, campo_email)
        time.sleep(1)
        campo_senha.clear()
        self.digite_como_uma_pessoa(self.senha, campo_senha)
        time.sleep(1)
        botao_login.click()
        time.sleep(5)


    def ClicarNoMenuOpcoes(self):
        try:
            time.sleep(1.5)
            scroll_box = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[4]/main/div/div[2]/div/div/div[2]/section/div[4]/div[1]/div[2]')
            menu_opcoes_do_album = scroll_box.find_elements_by_xpath(
                '//button[@class="_605821ce181f6de6632eabd6a46377fb-scss _50a94aaa6bd60a02583729be7f0e4f93-scss"]'
            )
            self.addMusica(menu_opcoes_do_album)
            print("primeira leva")

            while True:
                ActionChains(self.driver).move_to_element(menu_opcoes_do_album[len(menu_opcoes_do_album) - 1]).perform()
                novo_scroll = self.driver.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[4]/main/div/div[2]/div/div/div[2]/section/div[4]/div[1]/div[2]')
                mais_btns = novo_scroll.find_elements_by_xpath(
                    '//button[@class="_605821ce181f6de6632eabd6a46377fb-scss _50a94aaa6bd60a02583729be7f0e4f93-scss"]'
                )
                arrAux = mais_btns.copy()
                if (mais_btns[len(mais_btns)-1] == menu_opcoes_do_album[len(menu_opcoes_do_album)-1]):
                    break
                else:
                    arrAux.clear()
                    for x in range(0, len(mais_btns)):
                        if (mais_btns[x] not in menu_opcoes_do_album):
                            menu_opcoes_do_album.append(mais_btns[x])
                            arrAux.append(mais_btns[x])

                self.addMusica(arrAux)
                print("outra leva")

            print("FIM")

        except:
            pass

    def addMusica(self, arrMusicas):
        for btn in arrMusicas:
            print("Clicando em opcoes")
            ActionChains(self.driver).context_click(btn).perform()
            add_to_playlist_button = self.wait.until(
                CondicaoExperada.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//nav[@class="react-contextmenu react-contextmenu--visible"]/div[@class="react-contextmenu-item" and text()="Adicionar à playlist"]',
                    )
                )
            )
            time.sleep(1)
            add_to_playlist_button.click()
            thumbnail_playlist = self.wait.until(
                CondicaoExperada.visibility_of_any_elements_located(
                    (By.XPATH, '//div[@class="mo-coverArt-hoverContainer"]')
                )
            )
            time.sleep(1)
            print('Clicando em "Adicionar a Playlist"')
            thumbnail_playlist[0].click()
            time.sleep(1)

    def adicionarSemScroll(self):
        # menu_opcoes_do_album = self.driver.find_elements_by_xpath(
        #     '//button[@class="_605821ce181f6de6632eabd6a46377fb-scss _50a94aaa6bd60a02583729be7f0e4f93-scss"]'
        # )
        # print('arr btns salvo')
        # for btn in menu_opcoes_do_album:
        #     ActionChains(self.driver).context_click(btn).perform()
        #     add_to_playlist_button = self.wait.until(
        #         CondicaoExperada.element_to_be_clickable(
        #             (
        #                 By.XPATH,
        #                 '//nav[@class="react-contextmenu react-contextmenu--visible"]/div[@class="react-contextmenu-item" and text()="Adicionar à playlist"]',
        #             )
        #         )
        #     )
        #     time.sleep(random.randint(1, 2))
        #     add_to_playlist_button.click()
        #     thumbnail_playlist = self.wait.until(
        #         CondicaoExperada.visibility_of_any_elements_located(
        #             (By.XPATH, '//div[@class="mo-coverArt-hoverContainer"]')
        #         )
        #     )
        #     time.sleep(1.5)
        #     thumbnail_playlist[0].click()
        #     print('Clicando em "Adicionar a Playlist"')
        #     time.sleep(random.randint(2, 4))
        return

    def localizarPlaylistNome(self, pPlaylists):
        for play in pPlaylists:
            path = '//span[text()="'+self.nome_playlist_nova+'"]'
            if play.find_elements_by_xpath(path) != None:
                return play


    def AddAlbumParaPlaylist(self, album_link):
        self.ClicarEmAdicionarParaPlaylist()
        self.ClicarNaPlaylistASerAdicionada(album_link)


    def ClicarNaPlaylistASerAdicionada(self, album_link):
        time.sleep(1)
        thumbnail_playlist = self.wait.until(
            CondicaoExperada.visibility_of_any_elements_located(
                (By.XPATH, '//div[@class="mo-info-name" and]')
            )
        )
        time.sleep(0.5)
        thumbnail_playlist[0].click()
        print('Clicando em "Adicionar a Playlist"')
        time.sleep(random.randint(2, 4))

    def ClicarEmAdicionarParaPlaylist(self):
        add_to_playlist_button = self.wait.until(
            CondicaoExperada.element_to_be_clickable(
                (
                    By.XPATH,
                    '//nav[@class="react-contextmenu react-contextmenu--visible"]/div[@class="react-contextmenu-item" and text()="Adicionar à playlist"]',
                )
            )
        )
        time.sleep(random.randint(1, 2))
        add_to_playlist_button.click()

    @staticmethod
    def digite_como_uma_pessoa(frase, campo_input_unico):
        print("Digitando...")
        for letra in frase:
            campo_input_unico.send_keys(letra)
            time.sleep(random.randint(1, 5) / 30)


bot = PlaylistUltimato()
bot.Start()
