# link do site >>> https://ic360.com.br/
# login >>> 07039312964_48884
# senha >>> Lais2023@

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pyautogui
from random import choice
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import zipfile
from fake_useragent import UserAgent

def proxies(username, password, endpoint, port):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxies",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (endpoint, port, username, password)

    extension = 'proxy_extension.zip'

    with zipfile.ZipFile(extension, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return extension

proxy_list = [
    {"host":"181.41.197.13",'port':'59100','username':'','password':'','failed':0},
              {"host":"181.215.11.193",'port':'59100','username':'','password':'','failed':0},
              {"host":"185.187.233.239",'port':'59100','username':'','password':'','failed':0},
              {"host":"173.249.166.226",'port':'59100','username':'','password':'','failed':0},
              {"host":"141.11.140.183",'port':'59100','username':'','password':'','failed':0},
              {"host":"45.156.118.242",'port':'59100','username':'','password':'','failed':0},
              ]
def create_new_chrome_browser(use_proxy=True):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    ua = UserAgent(os='windows',min_percentage=.5)
    user_agent = ua.getChrome
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    prefs = {"credentials_enable_service": False,
        "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)    
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument(f"--user-agent={user_agent}")
    if use_proxy:
        
        if len(proxy_list) > 0:
            proxy_selected = choice(proxy_list)
            proxies(proxy_selected['username'], proxy_selected['password'], proxy_selected['host'], proxy_selected['port'])
            options.add_extension('proxy_extension.zip')
            print(proxy_selected,'proxy ok')
        
    else:
        proxy_selected = []
        pass
    # options.add_argument('--load-extension=proxy_extension.zip')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    while True:
        try:
            driver.get('http://checkip.amazonaws.com//')
            ip = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "/html/body")
                )
            )
            print(ip.text)
            proxy_list
            break
        except:
            if len(proxy_list) > 0:
                proxy_selected['failed'] += 1
                if proxy_selected['failed'] > 3:
                    proxy_list.remove(proxy_selected)
                    print('proxy ok',proxy_selected)
    return driver

def main ():
    def login_itau(usuario,senha):
        #abrir o navegador com o site

        driver = create_new_chrome_browser(use_proxy=True)
        driver.get("https://ic360.com.br/")

        # Esperar até que o botão "acessar" seja visível e interagível
        acessar_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'acessar')]"))
        )

        # Preencher o campo de usuário após o botão "acessar" ser visível
        login = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "UserName"))
        )
        login.send_keys(usuario)
        login.send_keys(Keys.TAB)

        # Preencher o campo de senha após o botão "acessar" ser visível
        senha_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "Passwd"))
        )
        senha_input.send_keys(senha)

        # Clicar no botão "acessar"
        acessar_button.click()
        try:
            elemento_apos_login = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > canal360i-root > canal360i-page-build > div > main > div > div > canal360i-controlador-pagina > div > div > div > canal360i-wrapper-mfe-strategy > canal360i-wrapper-mfe > div.container.ng-star-inserted > mf-corbans-chassi'))
            )
            return driver
        except:
            return False
        # Espera explícita para o primeiro Shadow Host
        
        
        
        
    def consulta_saldo_itau(cpf_original,matricula_original):
        operacoes = []
        shadow_host1 = WebDriverWait(driver, 55).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > canal360i-root > canal360i-page-build > div > main > div > div > canal360i-controlador-pagina > div > div > div > canal360i-wrapper-mfe-strategy > canal360i-wrapper-mfe > div.container.ng-star-inserted > mf-corbans-chassi'))
        )
        shadow_root1 = driver.execute_script('return arguments[0].shadowRoot', shadow_host1)

        # Espera explícita para o segundo Shadow Host
        shadow_host2 = WebDriverWait(shadow_root1, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#home > div > microfrontend-corbans-chassi-base-pagina-padrao > section > div > microfrontend-corbans-chassi-inss > mf-corban-inss'))
        )
        shadow_root2 = driver.execute_script('return arguments[0].shadowRoot', shadow_host2)

        # Espera explícita para o elemento dentro do segundo Shadow Root
        elemento_cpf = WebDriverWait(shadow_root2, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#voxel-input-0'))
        )
        # <<<<<<<<<<<<<<<<< CPF >>>>>>>>>>>>>>>>
        time.sleep(1)
        cpf_completo = cpf_original.zfill(11)
        elemento_cpf.send_keys(cpf_completo)
        cpf = elemento_cpf.get_attribute('value')

        # Espera explícita para o elemento dentro do segundo Shadow Root para o campo de matrícula
        elemento_matricula = WebDriverWait(shadow_root2, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#voxel-input-1'))
        )
        # <<<<<<<<<<<<<<<<< MATRÍCULA >>>>>>>>>>>>>>>>
        time.sleep(1)
        matricula_completa = matricula_original.zfill(10)
        elemento_matricula.send_keys(matricula_completa)
        matricula = elemento_matricula.get_attribute('value')

        # Espera explícita para o elemento do checkbox
        elemento_checkbox = WebDriverWait(shadow_root2, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#voxel-checkbox-1'))
        )
        time.sleep(1)
        elemento_checkbox.click()

        time.sleep(1)
        try:
            # Tente encontrar o elemento com o seletor CSS '#voxel-describedby-0'
            driver.find_element(By.CSS_SELECTOR, '#voxel-describedby-0')
            
            # Se o elemento for encontrado, retorne mensagem de CPF inválido
            return {
                "sucesso": False,
                "msg_retorno": 'CPF inválido',
                "cpf": cpf,
                "operacoes": []
            }
        except NoSuchElementException:
            # Se o elemento não for encontrado, prossiga com a ação
            elemento_matricula.send_keys(Keys.RETURN)



        # Espera explícita para o primeiro Shadow Host
        shadow_host1 = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > canal360i-root > canal360i-page-build > div > main > div > div > canal360i-controlador-pagina > div > div > div > canal360i-wrapper-mfe-strategy > canal360i-wrapper-mfe > div.container.ng-star-inserted > mf-corbans-chassi'))
        )
        shadow_root1 = driver.execute_script('return arguments[0].shadowRoot', shadow_host1)

        # Espera explícita para o segundo Shadow Host
        shadow_host2 = WebDriverWait(shadow_root1, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#home > div > microfrontend-corbans-chassi-base-pagina-padrao > section > div > microfrontend-corbans-chassi-inss > mf-corban-inss'))
        )
        shadow_root2 = driver.execute_script('return arguments[0].shadowRoot', shadow_host2)

        # Espera explícita para o terceiro Shadow Host
        shadow_host3 = WebDriverWait(shadow_root2, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#consentimento > div > componente-consentir-mfe'))
        )
        shadow_root3 = driver.execute_script('return arguments[0].shadowRoot', shadow_host3)
        
        try:
            # Localizar o elemento com o texto e exibir seu conteúdo
            seletor_mensagem = 'consentimento-main > componente-consentir-mfe-solicitacao-consentimento > componente-consentir-mfe-consentimento-online > div > div > voxel-alert > div > div > span'
            elemento_mensagem = WebDriverWait(shadow_root3, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, seletor_mensagem))
            )
            texto_mensagem = elemento_mensagem.text
            print(texto_mensagem)

            # Obter o elemento para o clique dentro do terceiro Shadow Root
            link_simule_sem_consultar = WebDriverWait(shadow_root3, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#consultar-dados > div > div > p > a'))
            )

            # Se tudo ocorrer bem até aqui, você pode prosseguir com o código

        except TimeoutException:
            # Tratamento de erro caso o elemento não seja encontrado
            mensagem_retorno = {
                "sucesso": False,
                "msg_retorno": 'Nenhuma Operação Encontrada',
                "cpf": cpf,
                "operacoes":[]
            }
            print(mensagem_retorno)
            return mensagem_retorno


        # Usar JavaScript para clicar no elemento
        driver.execute_script("arguments[0].click();", link_simule_sem_consultar)

        # Espera explícita para o primeiro Shadow Host
        shadow_host1 = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > canal360i-root > canal360i-page-build > div > main > div > div > canal360i-controlador-pagina > div > div > div > canal360i-wrapper-mfe-strategy > canal360i-wrapper-mfe > div.container.ng-star-inserted > mf-corbans-chassi'))
        )
        shadow_root1 = driver.execute_script('return arguments[0].shadowRoot', shadow_host1)

        # Espera explícita para o segundo Shadow Host
        shadow_host2 = WebDriverWait(shadow_root1, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#home > div > microfrontend-corbans-chassi-base-pagina-padrao > section > div > microfrontend-corbans-chassi-inss > mf-corban-inss'))
        )
        shadow_root2 = driver.execute_script('return arguments[0].shadowRoot', shadow_host2)
        
        # Localizar todos os elementos que contêm o valor da parcela dentro do segundo Shadow Root
        valor_parcela_elementos = WebDriverWait(shadow_root2, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#refinanciamento > div.refinanciamento-conteudo > div.refinanciamento-cabecalho > div.refinanciamento-informacoes > div:nth-child(1) > strong'))
        )

        # Inicializar listas vazias para armazenar os valores coletados
        valores_parcela = []

        # Iterar sobre os elementos e coletar os valores
        for valor_parcela_elemento in valor_parcela_elementos:
            valores_parcela.append(valor_parcela_elemento.text)

        # Localizar todos os elementos que contêm o número de Parcelas Pagas dentro do segundo Shadow Root
        parcelas_pagas_elementos = WebDriverWait(shadow_root2, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#refinanciamento > div.refinanciamento-conteudo > div.refinanciamento-cabecalho > div.refinanciamento-informacoes > div:nth-child(2) > strong'))
        )

        # Inicializar listas vazias para armazenar os valores coletados
        parcelas_pagas = []

        # Iterar sobre os elementos e coletar os valores
        for parcelas_pagas_elemento in parcelas_pagas_elementos:
            parcelas_pagas.append(parcelas_pagas_elemento.text)

        # Localizar todos os elementos que contêm a Taxa Origem dentro do segundo Shadow Root
        taxa_origem_elementos = WebDriverWait(shadow_root2, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#refinanciamento > div.refinanciamento-conteudo > div.refinanciamento-cabecalho > div.refinanciamento-informacoes > div:nth-child(3) > strong'))
        )

        # Inicializar listas vazias para armazenar os valores coletados
        taxas_origem = []

        # Iterar sobre os elementos e coletar os valores
        for taxa_origem_elemento in taxa_origem_elementos:
            taxas_origem.append(taxa_origem_elemento.text)

        # Localizar todos os elementos que contêm o Saldo Devedor dentro do segundo Shadow Root
        saldo_devedor_elementos = WebDriverWait(shadow_root2, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#refinanciamento > div.refinanciamento-conteudo > div.refinanciamento-cabecalho > div.refinanciamento-informacoes > div:nth-child(4) > strong'))
        )

        # Inicializar listas vazias para armazenar os valores coletados
        saldos_devedor = []

        # Iterar sobre os elementos e coletar os valores
        for saldo_devedor_elemento in saldo_devedor_elementos:
            saldos_devedor.append(saldo_devedor_elemento.text)

        # Iterar sobre os valores coletados e criar operações
        for valor, parcelas, taxa, saldo in zip(valores_parcela, parcelas_pagas, taxas_origem, saldos_devedor):
            # Converter a string 'parcelas' para um número inteiro
            parcelas_int = int(parcelas.split(' de ')[0])
            # Subtrair o número de parcelas pagas de 84 para obter as parcelas em aberto
            abertas = 84 - parcelas_int
            operacoes.append({
                "matricula": matricula,
                'parcela': valor,
                "saldo_devedor": saldo,
                'taxa': taxa,
                'abertas': f'{abertas}',
                'pagas': parcelas_int
            })


        msg_retorno = f"{len(operacoes)} Operação Encontrada" if len(operacoes) < 2 else f"{len(operacoes)} Operações Encontradas"
        return {
            "sucesso": True,
            "msg_retorno": msg_retorno,
            "cpf": cpf,
            "operacoes": operacoes
        }

    
    usuario = "07039312964_48884"
    senha = "Lais2023@"
    driver = login_itau(usuario,senha)
    cpf = '80790364700' 
    matricula = '458651303'  
    retorno = consulta_saldo_itau(cpf,matricula)
    print(retorno)


if __name__ == '__main__':
    main()


