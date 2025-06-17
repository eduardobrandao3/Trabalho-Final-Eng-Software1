import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
import time

class TestFormasPagamento(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para cada teste."""
        # Configura o driver do Chrome
        opcoes = Options()
        # opcoes.add_argument("--headless")  # Descomente para rodar sem abrir janela do navegador
        opcoes.add_argument("--disable-gpu")
        opcoes.add_argument("--no-sandbox")
        self.navegador = webdriver.Chrome(options=opcoes)
        
        # Obtém o caminho absoluto para o arquivo HTML
        file_path = os.path.abspath('payment_methods.html')
        self.navegador.get(f'file:///{file_path}')
        
        # Configura a espera
        self.espera = WebDriverWait(self.navegador, 10)

    def tearDown(self):
        """Finaliza o teste, fechando o navegador."""
        self.navegador.quit()

    # --- 1. TESTES DE CENÁRIO DE SUCESSO ---

    def test_carregamento_pagina(self):
        """Testa se a página de formas de pagamento carrega corretamente."""
        self.assertIn("Formas de Pagamento - Uber", self.navegador.title)
        self.assertEqual(
            self.navegador.find_element(By.CLASS_NAME, "card-title").text,
            "Formas de Pagamento"
        )
        self.assertTrue(self.navegador.find_element(By.ID, "paymentForm").is_displayed())
        self.assertTrue(self.navegador.find_element(By.ID, "paymentList").is_displayed())
        print("\n[SUCESSO] Página de formas de pagamento carregada corretamente.")
        time.sleep(1)

    def test_adicionar_forma_pagamento(self):
        """Testa a adição de uma nova forma de pagamento."""
        # Preenche o nome do cartão
        campo_nome_cartao = self.navegador.find_element(By.ID, "cardName")
        campo_nome_cartao.send_keys("Cartão de Teste")

        # Preenche o número do cartão
        campo_numero_cartao = self.navegador.find_element(By.ID, "card-number")
        campo_numero_cartao.send_keys("4242424242424242424")

        # Preenche a data de validade
        campo_data_validade = self.navegador.find_element(By.ID, "card-expiry")
        campo_data_validade.send_keys("12/25")

        # Preenche o código de segurança
        campo_codigo_seguranca = self.navegador.find_element(By.ID, "card-cvc")
        campo_codigo_seguranca.send_keys("123")

        # Marca a opção de definir como principal
        checkbox_principal = self.navegador.find_element(By.ID, "isMain")
        checkbox_principal.click()

        print("\n[SUCESSO] Forma de pagamento adicionada corretamente.")
        time.sleep(2)

    def test_definir_como_principal(self):
        """Testa definir uma forma de pagamento existente como principal."""
        # Garante que há pelo menos duas formas de pagamento
        lista_pagamentos = self.navegador.find_element(By.ID, "paymentList")
        formas_pagamento = lista_pagamentos.find_elements(By.CLASS_NAME, "list-group-item")
        self.assertGreaterEqual(
            len(formas_pagamento), 2, "Necessário pelo menos duas formas de pagamento para este teste"
        )

        # Encontra uma forma não principal e clica em 'definir como principal'
        for forma in formas_pagamento:
            if "Principal" not in forma.text:
                botao_definir_principal = forma.find_element(By.CLASS_NAME, "set-primary-btn")
                botao_definir_principal.click()
                break

        print("\n[SUCESSO] Forma de pagamento definida como principal.")
        time.sleep(1)

    # --- 2. TESTES DE VALIDAÇÃO E ERROS ---

    def test_validacao_campo_obrigatorio(self):
        """Testa a validação do campo obrigatório 'Nome no Cartão'."""
        # Tenta enviar o formulário sem preencher o nome
        botao_enviar = self.navegador.find_element(By.ID, "submitBtn")
        self.navegador.execute_script("arguments[0].click();", botao_enviar)

        # Verifica a mensagem de validação
        campo_nome_cartao = self.navegador.find_element(By.ID, "cardName")
        mensagem_validacao = campo_nome_cartao.get_attribute("validationMessage")
        print(f"\n[VALIDAÇÃO] Mensagem para campo obrigatório: '{mensagem_validacao}'")
        time.sleep(1)

    def test_remover_principal_falha(self):
        """Testa a tentativa de remover a forma de pagamento principal com outras disponíveis."""
        # Garante que há pelo menos duas formas de pagamento
        lista_pagamentos = self.navegador.find_element(By.ID, "paymentList")
        formas_pagamento = lista_pagamentos.find_elements(By.CLASS_NAME, "list-group-item")
        self.assertGreaterEqual(
            len(formas_pagamento), 2, "Necessário pelo menos duas formas de pagamento para este teste"
        )

        # Encontra a forma principal e clica em 'remover'
        for forma in formas_pagamento:
            if "Principal" in forma.text:
                botao_remover = forma.find_element(By.CLASS_NAME, "delete-btn")
                botao_remover.click()
                break

        # Aguarda o modal de confirmação e tenta confirmar
        self.espera.until(
            EC.visibility_of_element_located((By.ID, "confirmationModal"))
        )
        botao_confirmar = self.navegador.find_element(By.ID, "confirmAction")
        botao_confirmar.click()

        # Aguarda o alerta de falha
        self.espera.until(EC.alert_is_present())
        alerta = self.navegador.switch_to.alert
        self.assertIn(
            "Você precisa definir outro método como principal antes de remover este.",
            alerta.text
        )
        alerta.accept()
        print("\n[VALIDAÇÃO] Falha ao tentar remover forma de pagamento principal.")
        time.sleep(1)

    # --- 3. TESTES DE FUNCIONALIDADE DA INTERFACE ---

    def test_remover_forma_pagamento(self):
        """Testa a remoção de uma forma de pagamento não principal."""
        # Garante que há formas de pagamento disponíveis
        lista_pagamentos = self.navegador.find_element(By.ID, "paymentList")
        formas_pagamento = lista_pagamentos.find_elements(By.CLASS_NAME, "list-group-item")
        self.assertGreater(
            len(formas_pagamento), 0, "Necessário pelo menos uma forma de pagamento para este teste"
        )

        # Encontra uma forma não principal e clica em 'remover'
        contagem_inicial = len(formas_pagamento)
        for forma in formas_pagamento:
            if "Principal" not in forma.text:
                botao_remover = forma.find_element(By.CLASS_NAME, "delete-btn")
                botao_remover.click()
                break

        # Aguarda o modal de confirmação e confirma a remoção
        self.espera.until(
            EC.visibility_of_element_located((By.ID, "confirmationModal"))
        )
        botao_confirmar = self.navegador.find_element(By.ID, "confirmAction")
        botao_confirmar.click()

        # Aguarda o alerta de sucesso
        self.espera.until(EC.alert_is_present())
        alerta = self.navegador.switch_to.alert
        self.assertIn("Forma de pagamento removida com sucesso!", alerta.text)
        alerta.accept()

        # Verifica se a forma de pagamento foi removida
        self.espera.until(
            EC.presence_of_element_located((By.ID, "paymentList"))
        )
        formas_atualizadas = self.navegador.find_elements(By.CLASS_NAME, "list-group-item")
        self.assertLess(len(formas_atualizadas), contagem_inicial)
        print("\n[SUCESSO] Forma de pagamento não principal removida corretamente.")
        time.sleep(1)

    def test_botao_voltar(self):
        """Testa o botão de voltar para a página de perfil."""
        botao_voltar = self.navegador.find_element(By.CLASS_NAME, "btn-light")
        botao_voltar.click()
        self.espera.until(
            EC.url_contains("passenger_profile.html")
        )
        self.assertIn("passenger_profile.html", self.navegador.current_url)
        print("\n[FUNCIONALIDADE] Botão de voltar funcionando corretamente.")
        time.sleep(1)


class TestCadastroVeiculo(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para cada teste."""
        opcoes = Options()
        # opcoes.add_argument("--headless")  # Descomente para rodar sem interface gráfica
        opcoes.add_argument("--disable-gpu")
        opcoes.add_argument("--no-sandbox")
        self.navegador = webdriver.Chrome(options=opcoes)
        self.espera = WebDriverWait(self.navegador, 10)

        # Carrega a página de cadastro de veículo
        file_path = os.path.abspath('vehicle_register.html')
        self.navegador.get(f'file:///{file_path}')

        # Cria um arquivo dummy para testes de upload
        self.arquivo_dummy = os.path.abspath('dummy_crlv_image.txt')
        with open(self.arquivo_dummy, "w") as f:
            f.write("Este é um arquivo de teste para upload do CRLV.")

    def tearDown(self):
        """Finaliza o teste, fechando o navegador e limpando arquivos."""
        if os.path.exists(self.arquivo_dummy):
            os.remove(self.arquivo_dummy)
        self.navegador.quit()

    def _wait_for_and_handle_alert(self, expected_text_fragment):
        """
        Espera por um alerta, verifica seu texto e o aceita.
        Retorna o texto do alerta para verificação adicional.
        """
        try:
            alerta = self.espera.until(EC.alert_is_present())
            texto_alerta = alerta.text
            self.assertIn(expected_text_fragment, texto_alerta)
            alerta.accept()
            return texto_alerta
        except TimeoutException:
            self.fail("O alerta esperado não apareceu dentro do tempo limite.")
        except NoAlertPresentException:
            self.fail("Nenhum alerta estava presente quando a verificação foi feita.")

    def test_estado_inicial(self):
        """Verifica se a página carrega com todos os campos visíveis e vazios."""
        formulario = self.navegador.find_element(By.ID, 'vehicleForm')
        campos = [
            ('plate', 'Placa'),
            ('brand', 'Marca'),
            ('model', 'Modelo'),
            ('yearFab', 'Ano de Fabricação'),
            ('yearModel', 'Ano do Modelo'),
            ('color', 'Cor'),
            ('renavam', 'RENAVAM'),
            ('capacity', 'Capacidade de Passageiros'),
            ('insurance', 'Seguro Obrigatório'),
            ('app', 'Seguro APP')
        ]
        
        for campo_id, nome_campo in campos:
            campo = formulario.find_element(By.ID, campo_id)
            self.assertTrue(campo.is_displayed(), f"O campo '{nome_campo}' deveria estar visível.")
            self.assertEqual(campo.get_attribute('value'), '', f"O campo '{nome_campo}' deveria estar vazio.")

        select_categoria = Select(formulario.find_element(By.ID, 'category'))
        self.assertEqual(select_categoria.first_selected_option.get_attribute('value'), '', 
                        "O campo 'Categoria' deveria iniciar sem seleção.")
        
        campo_crlv = formulario.find_element(By.ID, 'crlv')
        self.assertTrue(campo_crlv.is_displayed(), "O campo 'CRLV' deveria estar visível.")
        self.assertEqual(campo_crlv.get_attribute('value'), '', "O campo 'CRLV' deveria estar vazio.")

        botao_enviar = formulario.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.assertTrue(botao_enviar.is_displayed(), "O botão 'Cadastrar Veículo' deveria estar visível.")
        self.assertEqual(botao_enviar.text.strip(), "Cadastrar Veículo", 
                        "O texto do botão deveria ser 'Cadastrar Veículo'.")
        print("\n[SUCESSO] Estado inicial da página verificado.")
        time.sleep(1)

    def test_cadastro_veiculo_sucesso(self):
        """Testa o cadastro de um veículo preenchendo todos os campos obrigatórios."""
        formulario = self.navegador.find_element(By.ID, 'vehicleForm')

        # Preenche os campos de texto e número
        formulario.find_element(By.ID, 'plate').send_keys('ABC1234')
        formulario.find_element(By.ID, 'brand').send_keys('Toyota')
        formulario.find_element(By.ID, 'model').send_keys('Corolla')
        formulario.find_element(By.ID, 'yearFab').send_keys('2020')
        formulario.find_element(By.ID, 'yearModel').send_keys('2021')
        formulario.find_element(By.ID, 'color').send_keys('Preto')
        formulario.find_element(By.ID, 'renavam').send_keys('12345678901')
        formulario.find_element(By.ID, 'capacity').send_keys('4')
        formulario.find_element(By.ID, 'insurance').send_keys('SEG123456')
        formulario.find_element(By.ID, 'app').send_keys('APP987654')

        # Seleciona a categoria
        Select(formulario.find_element(By.ID, 'category')).select_by_value('Executivo')

        # Faz o upload do arquivo CRLV
        formulario.find_element(By.ID, 'crlv').send_keys(self.arquivo_dummy)

        # Envia o formulário
        botao_enviar = formulario.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.navegador.execute_script("arguments[0].click();", botao_enviar)

        # Verifica o alerta de sucesso
        texto_alerta = self._wait_for_and_handle_alert("Veículo cadastrado com sucesso! Status: Pendente")
        print(f"\n[SUCESSO] Veículo cadastrado: '{texto_alerta}'")

        # Verifica o redirecionamento
        self.espera.until(EC.url_contains("vehicle_list.html"))
        self.assertIn("vehicle_list.html", self.navegador.current_url, 
                     "Deveria ter redirecionado para vehicle_list.html")
        print("[SUCESSO] Redirecionamento para lista de veículos confirmado.")
        time.sleep(3)

    def test_validacao_campos_obrigatorios(self):
        """Testa a validação de campos obrigatórios ao tentar enviar o formulário vazio."""
        formulario = self.navegador.find_element(By.ID, 'vehicleForm')
        botao_enviar = formulario.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.navegador.execute_script("arguments[0].click();", botao_enviar)

        # Verifica a mensagem de validação do campo 'Placa'
        campo_placa = formulario.find_element(By.ID, 'plate')
        mensagem_validacao = campo_placa.get_attribute("validationMessage")
        self.assertIn("Preencha este campo", mensagem_validacao, 
                     "Falha na validação do campo 'Placa'.")
        print(f"\n[VALIDAÇÃO] Mensagem para campo obrigatório 'Placa': '{mensagem_validacao}'")
        time.sleep(1)

    def test_selecao_categoria(self):
        """Testa a funcionalidade de seleção de categoria."""
        formulario = self.navegador.find_element(By.ID, 'vehicleForm')
        select_categoria = Select(formulario.find_element(By.ID, 'category'))

        # Verifica as opções disponíveis
        opcoes = [opt.get_attribute('value') for opt in select_categoria.options]
        opcoes_esperadas = ['', 'Comum', 'Executivo', 'Bagageiro']
        self.assertEqual(opcoes, opcoes_esperadas, 
                        "As opções de categoria não correspondem às esperadas.")

        # Seleciona uma opção e verifica
        select_categoria.select_by_value('Comum')
        self.assertEqual(select_categoria.first_selected_option.get_attribute('value'), 'Comum',
                        "A categoria 'Comum' deveria estar selecionada.")
        print("\n[SUCESSO] Seleção de categoria 'Comum' verificada.")

        # Muda para outra opção
        select_categoria.select_by_value('Executivo')
        self.assertEqual(select_categoria.first_selected_option.get_attribute('value'), 'Executivo',
                        "A categoria 'Executivo' deveria estar selecionada.")
        print("[SUCESSO] Seleção de categoria 'Executivo' verificada.")
        time.sleep(1)

    def test_upload_arquivo_crlv(self):
        """Testa o upload do arquivo CRLV."""
        formulario = self.navegador.find_element(By.ID, 'vehicleForm')
        campo_crlv = formulario.find_element(By.ID, 'crlv')

        # Faz o upload do arquivo dummy
        campo_crlv.send_keys(self.arquivo_dummy)

        # Verifica se o campo contém o nome do arquivo
        valor_campo = campo_crlv.get_attribute('value')
        self.assertIn('dummy_crlv_image.txt', valor_campo, 
                     "O campo CRLV deveria conter o nome do arquivo enviado.")
        print("\n[SUCESSO] Upload do arquivo CRLV verificado.")
        time.sleep(1)

    def test_botao_voltar(self):
        """Testa o botão de voltar para a página de lista de veículos."""
        botao_voltar = self.navegador.find_element(By.CLASS_NAME, 'btn-light')
        botao_voltar.click()

        self.espera.until(EC.url_contains("vehicle_list.html"))
        self.assertIn("vehicle_list.html", self.navegador.current_url, 
                     "Deveria ter redirecionado para vehicle_list.html")
        print("\n[SUCESSO] Botão de voltar funcionando corretamente.")
        time.sleep(1)


if __name__ == '__main__':
    unittest.main()