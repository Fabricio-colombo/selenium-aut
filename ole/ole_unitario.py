from models import *

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
    {"host":"181.41.197.13",'port':'59100','username':'****************','password':'***************','failed':0},
              {"host":"181.215.11.193",'port':'59100','username':'****************','password':'***************','failed':0},
              {"host":"185.187.233.239",'port':'59100','username':'****************','password':'***************','failed':0},
              {"host":"173.249.166.226",'port':'59100','username':'****************','password':'***************','failed':0},
              {"host":"141.11.140.183",'port':'59100','username':'****************','password':'***************','failed':0},
              {"host":"45.156.118.242",'port':'59100','username':'****************','password':'***************','failed':0},

]

#Função padrão, não alterar

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
                    alert_desenvolvimento(f'Proxy falhou 3 vezes {proxy_selected["host"]}')
                    proxy_list.remove(proxy_selected)
                    print('proxy ok',proxy_selected)
    return driver

              
def wait_loading(driver):
    time.sleep(.8)
    for n in range(10):
        try:
            class_name = driver.find_element(By.ID,'divLoading').get_attribute("class")
            print(class_name)
            if class_name == 'loading hidden':
                break
        except:
            time.sleep(1)
def login_usuario(usuario_id):
    for n in range(4):
        driver = create_new_chrome_browser()
        doc = db.collection("usuarios_banco").document(usuario_id)
        doc_dict = doc.get().to_dict()
        if not doc_dict:
            return False
        usuario = doc_dict["usuario_banco"]
        senha = doc_dict["senha"]
        if doc_dict["status"] == "Senha Inválida":
            return False
        
        driver.get("https://ola.oleconsignado.com.br/Usuario/Index?ReturnUrl=Home")
        try:
            WebDriverWait(driver,3).until(
                EC.element_to_be_clickable((By.ID, "Login"))
            ).send_keys(usuario)
            break
        except:
            driver.refresh()
            try:
                WebDriverWait(driver,3).until(
                    EC.element_to_be_clickable((By.ID, "Login"))
                ).send_keys(usuario)
                break
            except:
                driver.refresh()
    else:
        return False
#Essa função recebe dados da função principal, considere que ela recebe cpf e matrícula e eu altero depois
def higienizar_cpf_saldo_refin(doc, driver, nome_thread):
    try:
        # doc_dict = doc.to_dict()
        # usuario_banco = doc_dict["usuario_banco"]
        # usuario_conectado = threads_ativos[nome_thread]["usuario_logado"]
        # print(
        #     f"Logado no {usuario_conectado} e verificando cpf do usuário {usuario_banco}"
        # )
        driver.get("https://ola.oleconsignado.com.br/Identificacao")
        time.sleep(.5)
        try:
            WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.ID, "CPF"))
                        )
            cpf_input = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "CPF"))
                    )
            for n in range(11):
                cpf_input.send_keys(Keys.BACKSPACE)

            cpf_input.send_keys(doc_dict.get("cpf"))

        except:
            driver.refresh()
            try:
                cpf_input = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.ID, "CPF"))
                        )
                for n in range(11):
                    cpf_input.send_keys(Keys.BACKSPACE)

                cpf_input.send_keys(doc_dict.get("cpf"))
            except:
                erro = 'Inconsistência no Olé, tente novamente em alguns minutos'
                return {
                    "sucesso": False,
                    "msg_retorno": erro,
                    "cpf": doc_dict.get("cpf"),
                    'operacoes':[]
                }
        print('tem cpf')
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "btnIniciarOperacao"))
        ).click()
        
        wait_loading(driver)

        print("encerrou loading")
        try:
            WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), 'Operações Disponíveis - Empréstimo')]"))
                    ).click()
        except:
            erro = 'Nenhuma Operação Encontrada'
            return {
                "sucesso": False,
                "msg_retorno": erro,
                "cpf": doc_dict.get("cpf"),
                'operacoes':[]
            }
        try:
            tabela_matriculas = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.ID, "tbRefin"))
            )
            print('tabela_matricula')
        except:
            try:
                erro = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.ID, 'divMensagemErro'))
                ).text
                print(erro)
            except:
                erro = 'Nenhuma Operação Encontrada'
            return {
                "sucesso": False,
                "msg_retorno": erro,
                "cpf": doc_dict.get("cpf"),
                'operacoes':[]
            }
        
        trs = tabela_matriculas.find_elements(By.TAG_NAME,'tr')
        print(len(trs))
        matriculas_verificar = {}
        for tr in trs:
            tds = tr.find_elements(By.TAG_NAME,'td')
            if len(tds) == 0:
                continue
            matricula = (tds[0].text).strip()
            try:
                td_link = tds[1]
                link = td_link.find_elements(By.TAG_NAME,'a')[0].get_attribute('href')
                print(link)
            except:
                print('link nao encontrado')
                continue
            matriculas_verificar.update({matricula:link})
        
        for matricula in matriculas_verificar.keys():
            print(f'verificando matricula {matricula}')
            driver.get(matriculas_verificar[matricula])


            try:
                tabela = WebDriverWait(driver, 5).until(
                        EC.visibility_of_element_located((By.ID, 'tblContratosAptoRefin'))
                    )
            except:
                continue
            operacoes = []
            contratos = tabela.find_elements(By.TAG_NAME,'tr')
            for contrato in contratos:
                print('novo contrato')
                
                tds = contrato.find_elements(By.TAG_NAME,'td')
                print(len(tds))
                if len(tds)<=1:
                    continue
                for td in tds:
                    print(td.text)
                taxa = tds[4].text
                parcela = tds[5].text
                saldo_devedor = tds[6].text
                operacoes.append(
                    {
                        'matricula':matricula,
                        "parcela": parcela,
                        'saldo_devedor':saldo_devedor,
                        'taxa':taxa
                    }
                )
        if len(operacoes) == 0:
            return {
                "sucesso": False,
                "msg_retorno": f'Nenhuma Operação Encontrada',
                "cpf": doc_dict.get("cpf"),
                "operacoes":[]
            }
        msg_retorno = f"{len(operacoes)} Operação Encontrada" if len(operacoes) <2 else f"{len(operacoes)} Operações Encontradas"

        return {
                "sucesso": True,
                "msg_retorno": msg_retorno,
                "cpf": doc_dict.get("cpf"),
                "operacoes":operacoes
            }
    except Exception as e:
        try:
            alert = driver.switch_to.alert
            erro = alert.text
            print("adicionar verificação alerta")
            alert.accept()
            return {
                "sucesso": False,
                "msg_retorno": erro,
                "valor_liberado": 0,
                "cpf": doc_dict.get("cpf"),
            }
        except:
            pass
        print(e, e.args)
        print("falha")
        try:
            threads_ativos[nome_thread]["docs"].remove(doc)
        except:
            pass
        threads_ativos[nome_thread]["usuario_logado"] = ""
        try:
            driver.quit()
        except:
            pass
        return {
            "sucesso": False,
            "msg_retorno": "Falha na Consulta - Tente Novamente",
            "cpf": doc_dict.get("cpf"),
            "valor_liberado": 0,
        }
