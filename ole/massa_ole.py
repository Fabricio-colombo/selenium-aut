from models import *

banco = "ole"
#fator_divisao_lines_until_update = 20 significa que o arquivo atualiza a cada 5%: 100/20

def wait_loading(driver):
    time.sleep(0.8)
    for n in range(10):
        try:
            class_name = driver.find_element(By.ID, "divLoading").get_attribute("class")
            print(class_name)
            if class_name == "loading hidden":
                break
            else:
                time.sleep(1)
        except:
            break
    return


def consulta_saldo_inss_ole(cpf, parcela,matricula, driver):
    for n in range(3):
        driver.get("https://ola.oleconsignado.com.br/Identificacao")
        parcela = fix_valor(parcela)
        cpf = str(cpf)
        while len(cpf) < 11:
            cpf = '0' + cpf
        for n in range(5):
            try:
                cpf_input = WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.ID, "CPF"))
                )
                for n in range(11):
                    cpf_input.send_keys(Keys.BACKSPACE)

                cpf_input.send_keys(cpf)
                break

            except:
                driver.refresh()
        else:
            return {"saldo_devedor": "falha banco", "taxa": "falha banco"}
        print("tem cpf")

        WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.ID, "btnIniciarOperacao"))
        ).click()

        wait_loading(driver)

        print("encerrou loading")
        try:
            WebDriverWait(driver, 1.5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//*[contains(text(), 'Operações Disponíveis - Empréstimo')]",
                    )
                )
            ).click()
            break
        except:
            pass
    else:
        return {
    'saldo_devedor':'nao encontrado',
    'taxa':'nao encontrado'
            }
    try:
        
        tabela_matriculas = WebDriverWait(driver, 1.5).until(
            EC.visibility_of_element_located((By.ID, "tbRefin"))
        )
        print("tabela_matricula")
    except:
        try:
            erro = (
                WebDriverWait(driver, 1)
                .until(EC.visibility_of_element_located((By.ID, "divMensagemErro")))
                .text
            )
            print(erro)
        except:
            erro = "Nenhuma Operação Encontrada"
        return {
'saldo_devedor':'nao encontrado',
'taxa':'nao encontrado'
        }

    trs = tabela_matriculas.find_elements(By.TAG_NAME, "tr")
    print(len(trs))
    matriculas_verificar = {}
    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, "td")
        if len(tds) == 0:
            continue
        matricula = (tds[0].text).strip()
        try:
            td_link = tds[1]
            link = td_link.find_elements(By.TAG_NAME, "a")[0].get_attribute("href")
            print(link)
        except:
            print("link nao encontrado")
            continue
        matriculas_verificar.update({matricula: link})

    for matricula_encontrada in matriculas_verificar.keys():
        if matricula_encontrada != matricula.strip():
            continue
        print(f"verificando matricula {matricula}")
        driver.get(matriculas_verificar[matricula])

        try:
            tabela = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "tblContratosAptoRefin"))
            )
        except:
            continue
        contratos = tabela.find_elements(By.TAG_NAME, "tr")
        for contrato in contratos:
            print("novo contrato")

            tds = contrato.find_elements(By.TAG_NAME, "td")
            if len(tds) <= 1:
                continue
            taxa = tds[4].text
            parcela_encontrada = tds[5].text
            print('parcela_encontrada:',fix_valor(parcela_encontrada),fix_valor(parcela))
            if fix_valor(parcela_encontrada) != fix_valor(parcela):
                print('valor de parcela diferente')
                
                continue
            saldo_devedor = tds[6].text
            print('saldo_devedor',saldo_devedor)
            return {
                    "saldo_devedor": fix_valor(saldo_devedor),
                    "taxa": fix_valor(taxa),
                }
            
    else:
        return {
'saldo_devedor':'nao encontrado',
'taxa':'nao encontrado'
        }

    # except Exception as e:
#         return {
# 'saldo_devedor':'nao encontrado',
# 'taxa':'nao encontrado'
#         }


def login_ole_orienta(usuario_id):
    
    driver = create_new_chrome_browser()
    doc = db.collection("usuarios_banco").document(usuario_id)
    doc_dict = doc.get().to_dict()
    if not doc_dict:
        return False
    usuario = doc_dict["usuario_banco"]
    senha = doc_dict["senha"]
    if doc_dict["status"] == "Senha Inválida":
        return False
    for n in range(4):
        driver.get("https://ola.oleconsignado.com.br/Usuario/Index?ReturnUrl=Home")
        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, "Login"))
            ).send_keys(usuario)
            break
        except:
            driver.refresh()
            try:
                WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.ID, "Login"))
                ).send_keys(usuario)
                break
            except:
                driver.refresh()
    else:
        return False
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "Senha"))
    ).send_keys(senha)
    driver.find_element(By.ID, "botaoAcessar").click()
    print("verificar login")

    driver.refresh()
    for n in range(5):
        try:
            WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.ID, "divCorrespondente"))
            )
            break
        except:
            try:
                msg_erro = (
                    WebDriverWait(driver, 1)
                    .until(EC.visibility_of_element_located((By.ID, "MensagensErro")))
                    .text
                )
                if "senha" in msg_erro:
                    driver.quit()
                    return False
            except:
                driver.refresh()
                pass

    return driver

