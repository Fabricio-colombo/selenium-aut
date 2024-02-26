from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.select import Select
from random import choice
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import zipfile
from fake_useragent import UserAgent
import time
from twocaptcha import TwoCaptcha
from selenium.webdriver.common.action_chains import ActionChains
import os
import random




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
              {"host":"181.41.197.51",'port':'59100','username':'','password':'***************','failed':0},
              {"host":"141.11.141.243",'port':'59100','username':'','password':'***************','failed':0},
              {"host":"185.74.55.82",'port':'59100','username':'','password':'***************','failed':0},
              {"host":"2.56.249.158",'port':'59100','username':'','password':'***************','failed':0},
              {"host":"191.96.73.137",'port':'59100','username':'','password':'***************','failed':0},
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

def login_bradesco(usuario, senha):
    driver = create_new_chrome_browser(use_proxy=True)
    try:
        driver.get("https://www.bradescopromotoranet.com.br/")
        for tentativa1 in range(3):
            try:
                WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((By.ID, 'cphBodyMain_cphBody_txtLogin'))
                )
                print("Iniciando o Login")
                break
            except TimeoutException:
                print(f"Tentativa de pegar o ID do login = {tentativa1+1}")
        else:
            raise TimeoutException("Página indisponível após 3 tentativas.")
    except (TimeoutException, WebDriverException, NoSuchElementException): 
        print("Página indisponível")
        retorno =  {
            "sucesso": False,
            "msg_retorno": 'A página pode estar temporariamente indisponível',
        }
        driver.quit()
        return retorno
    
    try:
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.ID, 'cphBodyMain_cphBody_txtLogin'))
        )
        driver.find_element(By.ID, "cphBodyMain_cphBody_txtLogin").send_keys(usuario)
        print(f"Digitou o login {usuario}")
        
        WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.ID, "cphBodyMain_cphBody_txtSenha"))
        )
        driver.find_element(By.ID, "cphBodyMain_cphBody_txtSenha").send_keys(senha)
        print(f"Digitou a senha {senha}")
        
        elemento_enter = WebDriverWait(driver, 1).until(
            EC.visibility_of_element_located((By.ID, "cphBodyMain_cphBody_btnEntrar"))
        )
        elemento_enter.send_keys(Keys.ENTER)
        print(f"Apertou ENTER para entrar.")
        
        try:
            for tentativa2 in range(5):
                WebDriverWait(driver, 1).until( 
                    EC.visibility_of_element_located((By.ID, "cphBodyMain_imgLogo"))
                )
                print(f"Tentativa de pegar ID da logotipo {tentativa2+1}")
                print("Logotipo encontrado, login bem-sucedido.")
                break
        except TimeoutException:
            print("Logotipo não encontrado, verificando alerta de mensagem.")
            
            try:
                elemento_alerta = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((By.ID, "dvDialog"))
                )
                print("Alerta de login inválido detectado.")
                mensagem = elemento_alerta.text
                print(f"Mensagem de alerta: {mensagem}")
                retorno = {
                    "driver": False,
                    "msg_retorno": mensagem,
                }
                print(retorno)
                driver.quit()
                return retorno
            except TimeoutException:
                print("Nenhum alerta de mensagem detectado.")
    
    except Exception as e:
        print(f"Error: {e}")
        driver.quit()
        return {'driver': False, 'msg_retorno': 'Válido'}

    link_refin = 'https://www.bradescopromotoranet.com.br/Forms/Proposta/CadastroProposta.aspx?prop=VPUjo2IpaA0%3d&prod=QPTSe18vz14%3d'
    try:
        WebDriverWait(driver, 1).until (
            EC.visibility_of_element_located((By.ID, 'cphBodyMain_imgLogo'))
        )
        driver.get(link_refin)
        print("Acessando o link de refinanciamento")   
    except:
        print('Falha ao acessar o link do refin')
        
    try:
        try:
            select_filial = '//*[@id="cphBodyMain_cphBody_cphBody_Panel1"]/div/h2'
            text_filial = driver.find_element(By.XPATH, select_filial).text
            print(text_filial)
        except:
            print('Não localizou o texto: FAVOR SELECIONAR UMA FILIAL')
        if text_filial == 'FAVOR SELECIONAR UMA FILIAL':
            camp_select = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.ID, 'cphBodyMain_cpPromotoras_ddlPromotora'))
            )
            camp_select.click()
            time.sleep(0.5)
            camp_select.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
            camp_select.send_keys(Keys.ENTER)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'UpdateProgress1'))
                )
                print('Esperando o LOADING...')
                driver.execute_script("document.getElementById('UpdateProgress1').style.display='block';")
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.ID, 'UpdateProgress1'))
                )
                print('Esperou o loading com sucesso.')

            except TimeoutException:
                print('Não esperou o loading.')
        else:
            print('Não precisou selecionar uma filial.')
    except Exception as e:
        print('Erro inesperado: ', e)
    
    try:
        for espera_validacao in range(5):
            WebDriverWait(driver, 1).until (
                EC.visibility_of_element_located((By.CLASS_NAME, 'form'))
            )
            print(f"Esperando validação = {espera_validacao} de 5")
            break
    except TimeoutException:
        print('Não esperou para preencher')
    
    try:
        elemento_select = driver.find_element(By.CSS_SELECTOR, "#cphBodyMain_cphBody_cphBody_ucDadosValidacao_drpEmpresa")
        driver.execute_script("arguments[0].style.display = 'block';", elemento_select)
        select = Select(elemento_select)
        select.select_by_index(1)
        print("Preencheu o campo Empresa.")
    except:
        print('Falha ao preencher o campo Empresa')
    
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'UpdateProgress1'))
        )
        print('Loading começou.')

        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, 'UpdateProgress1'))
        )
        print('Esperou o loading com sucesso.')

    except TimeoutException:
        print('Não esperou o loading.')
    time.sleep(0.5)
    
    try:
        elemento_select2 = driver.find_element(By.CSS_SELECTOR, '#cphBodyMain_cphBody_cphBody_ucDadosValidacao_drpProduto')
        driver.execute_script("arguments[0].style.display = 'block';", elemento_select2)
        select2 = Select(elemento_select2)
        select2.select_by_index(3)
        print("Preencheu o campo Produto.")
    except:
        print('Falha ao preencher o campo Produto')
    
    try:
        elemento_alerta_produto = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "dvDialog"))
        )
        mensagem = elemento_alerta_produto.text
        print(f"Mensagem de alerta: {mensagem}")
        elemento_exit_alerta = driver.find_element(By.CLASS_NAME, 'ui-icon-closethick')
        elemento_exit_alerta.click()
        print('Exitou o alerta')
    except:
        print("Falha ao exitar o alerta")
    
    try:
        WebDriverWait(driver, 5).until(
            lambda driver: len(Select(driver.find_element(By.ID, 'cphBodyMain_cphBody_cphBody_ucDadosValidacao_drpLoja')).options) > 0
        )
        print("Campo Loja está pronto para ser preenchido.")
    except TimeoutException:
        print("Campo Loja não está pronto para ser preenchido no tempo esperado.")
    time.sleep(1.5)
    
    try:
        elemento_select3 = driver.find_element(By.CSS_SELECTOR, '#cphBodyMain_cphBody_cphBody_ucDadosValidacao_drpLoja')
        driver.execute_script("arguments[0].style.display = 'block';", elemento_select3)
        select3 = Select(elemento_select3)
        select3.select_by_index(1)
        print('Preencheu o campo Loja')
    except:
        print('Falha ao preencher o campo Loja')
    
    try:
        WebDriverWait(driver, 5).until(
            lambda driver: len(Select(driver.find_element(By.ID, 'cphBodyMain_cphBody_cphBody_ucDadosValidacao_drpFilial')).options) > 0
        )
        print("Campo Filial está pronto para ser preenchido.")
    except TimeoutException:
        print("Campo Filial não está pronto para ser preenchido no tempo esperado.")
    time.sleep(1.5)
    
    try:
        elemento_select4 = driver.find_element(By.CSS_SELECTOR, '#cphBodyMain_cphBody_cphBody_ucDadosValidacao_drpFilial')
        driver.execute_script("arguments[0].style.display = 'block';", elemento_select4)
        select4 = Select(elemento_select4)
        select4.select_by_index(1)
        print('Preencheu o campo Filial')
    except:
        print("Falha ao preencher o campo Filial")
    
    try:
        WebDriverWait(driver, 5).until(
            lambda driver: len(Select(driver.find_element(By.ID, 'cphBodyMain_cphBody_cphBody_ucDadosValidacao_drpTipoBeneficio')).options) > 0
        )
        print("Campo Beneficio está pronto para ser preenchido.")
    except TimeoutException:
        print("Campo Beneficio não está pronto para ser preenchido no tempo esperado.")
    time.sleep(1.5)
    
    try:
        elemento_select5 = driver.find_element(By.CSS_SELECTOR, '#cphBodyMain_cphBody_cphBody_ucDadosValidacao_drpTipoBeneficio')
        driver.execute_script("arguments[0].style.display = 'block';", elemento_select5)
        select5 = Select(elemento_select5)
        select5.select_by_index(1)
        print('Preencheu o campo Beneficio')
    except:
        print("Falha ao preencher o campo Beneficio")
    
    try:
        numero_dialogo = 46
        numero_dialogo2 = 56
        while True:
            api_key = "08577d94e9e2272e61226ad7f039e3b0"
            solver = TwoCaptcha(api_key)
            file_address = "E:/LIS/LIS/BRADESCO/img_captchar/captcha.png"
            id_captcha = 'cphBodyMain_cphBody_cphBody_ucCaptcha_captcha'
            time.sleep(0.5)
            if os.path.exists(file_address):
                os.remove(file_address)
            
            captcha = driver.find_element(By.ID, id_captcha)
            captcha.screenshot(file_address)
            print('Screenshot do Captchar')

            id = solver.send(file=file_address)
            print("Arquivo enviado:", file_address)
            time.sleep(5)

            captcha_answer = None
            attempts = 0
            while attempts < 5:
                try:
                    captcha_answer = solver.get_result(id)
                    print("Captcha resolvido:", captcha_answer)
                    if captcha_answer != "0000":
                        break
                except Exception as e:
                    print(f"Erro ao resolver captcha: {e}")
                    time.sleep(5)
                attempts += 1
                
            driver.find_element(By.ID, 'cphBodyMain_cphBody_cphBody_ucCaptcha_txtCaptcha').clear()
            print('Limpou o campo para digitar o captchar...')
            time.sleep(0.5)
            driver.find_element(By.ID, 'cphBodyMain_cphBody_cphBody_ucCaptcha_txtCaptcha').send_keys(captcha_answer)
            print(f'Digitou o Captchar: {captcha_answer}')
            time.sleep(0.5)
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, 'cphBodyMain_cphBody_cphBody_ucConsultaMargem_ucConsultaMargemRefin_txtCpf'))
            )
            preencher_cpf = driver.find_element(By.ID, 'cphBodyMain_cphBody_cphBody_ucConsultaMargem_ucConsultaMargemRefin_txtCpf')
            lista_de_cpfs = ['08507623913', '07376663908', '91519276915']
            cpf_aleatorio = random.choice(lista_de_cpfs)
            preencher_cpf.send_keys(cpf_aleatorio)
            print('Preencheu o CPF para teste do CAPTCHA')
            time.sleep(0.5)
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, 'cphBodyMain_cphBody_cphBody_ucConsultaMargem_ucConsultaMargemRefin_btnPesquisarCpf'))
            )
            clicar_lupa = driver.find_element(By.ID, 'cphBodyMain_cphBody_cphBody_ucConsultaMargem_ucConsultaMargemRefin_btnPesquisarCpf')
            actions = ActionChains(driver)
            actions.double_click(clicar_lupa).perform()
            print('Pesquisou CPF')
            
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, f'body > div:nth-child({numero_dialogo})'))
                )
                dv_dialog = driver.find_element(By.CSS_SELECTOR, f'body > div:nth-child({numero_dialogo})')

                mensagem_de_erro = dv_dialog.find_element(By.TAG_NAME, 'p').text
                print("Mensagem de erro capturada:", mensagem_de_erro)
                try:
                    WebDriverWait(driver, 1).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, f'body > div:nth-child({numero_dialogo}) > div.ui-dialog-titlebar.ui-corner-all.ui-widget-header.ui-helper-clearfix > button > span.ui-button-icon.ui-icon.ui-icon-closethick'))
                    )
                    fechar_alerta = driver.find_element(By.CSS_SELECTOR, f'body > div:nth-child({numero_dialogo}) > div.ui-dialog-titlebar.ui-corner-all.ui-widget-header.ui-helper-clearfix > button > span.ui-button-icon.ui-icon.ui-icon-closethick')
                    fechar_alerta.click()
                    print('Fechou o alerta de: Código de segurança inválido.')
                except:
                    print('Não fechou o alerta de: Código de segurança inválido.')
                if mensagem_de_erro == 'Código de segurança inválido.':
                    limpar_cpf = driver.find_element(By.ID, 'cphBodyMain_cphBody_cphBody_ucConsultaMargem_ucConsultaMargemRefin_txtCpf')
                    limpar_cpf.clear()
                    print('limpou o campo de CPF')
                    print('Código de segurança inválido - Refazendo o loop')
                    numero_dialogo += 11
                    numero_dialogo2 += 11
                    continue
            except:
                print('NÃO capturou o erro: Código de segurança inválido.')
            
            try:
                WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, f'body > div:nth-child({numero_dialogo}) > div.ui-dialog-titlebar.ui-corner-all.ui-widget-header.ui-helper-clearfix > button > span.ui-button-icon.ui-icon.ui-icon-closethick'))
                )
                fechar_alerta = driver.find_element(By.CSS_SELECTOR, f'body > div:nth-child({numero_dialogo}) > div.ui-dialog-titlebar.ui-corner-all.ui-widget-header.ui-helper-clearfix > button > span.ui-button-icon.ui-icon.ui-icon-closethick')
                fechar_alerta.click()
                print('Fechou o alerta de: Código de segurança inválido.')
            except:
                print('Não fechou o alerta de: Código de segurança inválido.')

            try:
                print('Tentando localizar se o CPF é válido.')
                WebDriverWait(driver, 1).until (
                    EC.visibility_of_element_located((By.CSS_SELECTOR, f'body > div:nth-child({numero_dialogo2})'))
                )
                dv_dialog2 = driver.find_element(By.CSS_SELECTOR, f"body > div:nth-child({numero_dialogo2})")

                mensagem_de_erro2 = dv_dialog2.find_element(By.TAG_NAME, 'p').text
                print("Mensagem de erro capturada:", mensagem_de_erro2)
            except:
                print('NÃO capturou o erro: Não foram localizados dados para o CPF informado.')
            
            try:
                WebDriverWait(driver, 1).until (
                    EC.visibility_of_element_located((By.CSS_SELECTOR, f'body > div:nth-child({numero_dialogo2}) > div.ui-dialog-titlebar.ui-corner-all.ui-widget-header.ui-helper-clearfix > button > span.ui-button-icon.ui-icon.ui-icon-closethick'))
                )
                fechar_alerta_cpf = driver.find_element(By.CSS_SELECTOR, f'body > div:nth-child({numero_dialogo2}) > div.ui-dialog-titlebar.ui-corner-all.ui-widget-header.ui-helper-clearfix > button > span.ui-button-icon.ui-icon.ui-icon-closethick')
                fechar_alerta_cpf.click()
                print('fechou o alerta de: Não foram localizados dados para o CPF informado.')
            except:
                print('não fechou o alerta de CPF válido.')
            
            try:
                if mensagem_de_erro2 == 'Não foram localizados dados para o CPF informado.':
                    print('MSG: Não foram localizados dados para o CPF informado - SAINDO DO LOOP')
                    print('SUCESSO!! CPF É VÁLIDO')
                    break
            except:
                print('Não localizou o alerta para válidar o CPF e por isto não saiu do loop')
                
            break

    except Exception as e:
        print('Não conseguiu passar do captchar')
        print(f"Ocorreu um erro: {e}")
        
    time.sleep(9999)
    return {'driver': driver}



    
   
usuario = "1012-LISJV@BEVICRED"
senha = "Lispro2024@"
driver = login_bradesco(usuario,senha)
cpf = '08507623913'