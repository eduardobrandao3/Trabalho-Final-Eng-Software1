import unittest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class RegistrationTest(unittest.TestCase):

    def setUp(self):
        """Configuração inicial para cada teste."""
        # Configura o driver do Chrome
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless") # Descomente para rodar sem abrir janela do navegador
        self.driver = webdriver.Chrome(options=options)
        
        # Obtém o caminho absoluto para o arquivo HTML
        # Garanta que register.html e script.js estão na mesma pasta do seu teste
        file_path = os.path.abspath('register.html')
        self.driver.get(f'file:///{file_path}')

        # Cria um arquivo dummy para ser usado nos testes de upload
        self.dummy_file_path = os.path.abspath('dummy_file.txt')
        with open(self.dummy_file_path, "w") as f:
            f.write("Este é um arquivo de teste para upload.")

    def tearDown(self):
        """Finaliza o teste, fechando o navegador e limpando arquivos."""
        if os.path.exists(self.dummy_file_path):
            os.remove(self.dummy_file_path)
        self.driver.quit()

    # --- 1. TESTES DE CENÁRIO DE SUCESSO ---

    def test_passenger_registration_success(self):
        """Testa o cadastro de um passageiro preenchendo todos os campos obrigatórios."""
        driver = self.driver
        form = driver.find_element(By.ID, 'passengerForm')
        
        # Preenche os campos de texto
        form.find_element(By.CSS_SELECTOR, 'input[type="text"]:not(.cpf)').send_keys('Ana Silva')
        form.find_element(By.CLASS_NAME, 'cpf').send_keys('123.456.789-00')
        form.find_element(By.CSS_SELECTOR, 'input[type="date"]').send_keys('15/08/1995')
        form.find_element(By.CLASS_NAME, 'phone').send_keys('11987654321')
        form.find_element(By.CSS_SELECTOR, 'input[type="email"]').send_keys('ana.silva@example.com')
        
        # Seleciona o sexo (novo campo)
        Select(form.find_element(By.TAG_NAME, 'select')).select_by_value('feminino')
        
        # Preenche senhas
        password_fields = form.find_elements(By.CSS_SELECTOR, 'input[type="password"]')
        password_fields[0].send_keys('SenhaForte123!')
        password_fields[1].send_keys('SenhaForte123!')

        # Verifica o botão de submit (não clica para não recarregar a página)
        submit_button = form.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.assertEqual(submit_button.text, "Criar Conta")
        
        print("\n[SUCESSO] Formulário do Passageiro preenchido corretamente.")
        time.sleep(2)

    def test_driver_registration_success(self):
        """Testa o cadastro de um motorista preenchendo todos os campos obrigatórios."""
        driver = self.driver
        driver.find_element(By.ID, 'driverRole').click()
        time.sleep(0.5)
        form = driver.find_element(By.ID, 'driverForm')
        
        # Preenche dados pessoais
        text_inputs = form.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
        text_inputs[0].send_keys('Carlos Souza')     # Nome
        text_inputs[1].send_keys('987.654.321-00')    # CPF
        text_inputs[2].send_keys('12345678901')       # Número da CNH
        
        # Preenche dados da CNH
        selects = form.find_elements(By.TAG_NAME, 'select')
        Select(selects[0]).select_by_visible_text('B') # Categoria CNH

        date_inputs = form.find_elements(By.CSS_SELECTOR, 'input[type="date"]')
        date_inputs[0].send_keys('20/10/2028') # Validade CNH
        date_inputs[1].send_keys('25/05/1990') # Data de Nascimento (novo campo)

        # Preenche contato e sexo (novo campo)
        form.find_element(By.CLASS_NAME, 'phone').send_keys('11912345678')
        form.find_element(By.CSS_SELECTOR, 'input[type="email"]').send_keys('carlos.souza@example.com')
        Select(selects[1]).select_by_value('masculino') # Sexo

        # Preenche senhas
        password_fields = form.find_elements(By.CSS_SELECTOR, 'input[type="password"]')
        password_fields[0].send_keys('MotoristaTop1!')
        password_fields[1].send_keys('MotoristaTop1!')
        
        # Realiza o upload dos arquivos obrigatórios
        file_inputs = form.find_elements(By.CSS_SELECTOR, 'input[type="file"][required]')
        for file_input in file_inputs:
            file_input.send_keys(self.dummy_file_path)

        submit_button = form.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.assertEqual(submit_button.text.strip(), "Enviar Cadastro")
        
        print("\n[SUCESSO] Formulário do Motorista preenchido corretamente.")
        time.sleep(3)

    # --- 2. TESTES DE VALIDAÇÃO E ERROS ---

    def test_required_fields_validation(self):
        """Testa a validação de campos obrigatórios para ambos os formulários."""
        driver = self.driver
        
        # Teste para Passageiro
        passenger_form = driver.find_element(By.ID, 'passengerForm')
        driver.execute_script("arguments[0].click();",passenger_form.find_element(By.CSS_SELECTOR, 'button[type="submit"]'))
        name_input = passenger_form.find_element(By.CSS_SELECTOR, 'input[type="text"]')
        validation_msg = name_input.get_attribute("validationMessage")
        self.assertIn("Preencha este campo", validation_msg, "Falha na validação do nome do passageiro")
        print(f"\n[VALIDAÇÃO] Mensagem para passageiro: '{validation_msg}'")
        time.sleep(1)
        
        # Teste para Motorista
        driver.find_element(By.ID, 'driverRole').click()
        time.sleep(0.5)
        driver_form = driver.find_element(By.ID, 'driverForm')
        driver.execute_script("arguments[0].click();", driver_form.find_element(By.CSS_SELECTOR, 'button[type="submit"]'))
        driver_name_input = driver_form.find_element(By.CSS_SELECTOR, 'input[type="text"]')
        driver_validation_msg = driver_name_input.get_attribute("validationMessage")
        self.assertIn("Preencha este campo", driver_validation_msg, "Falha na validação do nome do motorista")
        print(f"[VALIDAÇÃO] Mensagem para motorista: '{driver_validation_msg}'")
        time.sleep(1)

    def test_invalid_email_format(self):
        """Testa a validação nativa do navegador para um e-mail com formato inválido."""
        driver = self.driver
        form = driver.find_element(By.ID, 'passengerForm')
        
        # Preenche os campos de texto
        form.find_element(By.CSS_SELECTOR, 'input[type="text"]:not(.cpf)').send_keys('Ana Silva')
        form.find_element(By.CLASS_NAME, 'cpf').send_keys('123.456.789-00')
        form.find_element(By.CSS_SELECTOR, 'input[type="date"]').send_keys('15/08/1995')
        form.find_element(By.CLASS_NAME, 'phone').send_keys('11987654321')
        email_input = form.find_element(By.CSS_SELECTOR, 'input[type="email"]')

        email_input.send_keys("email-invalido")

        driver.execute_script("arguments[0].click();", form.find_element(By.CSS_SELECTOR, 'button[type="submit"]'))
        
        validation_msg = email_input.get_attribute("validationMessage")
        print(validation_msg)
        self.assertTrue("Inclua um" in validation_msg or "Please include" in validation_msg)
        print(f"\n[VALIDAÇÃO] Mensagem para e-mail inválido: '{validation_msg}'")
        time.sleep(2)

    def test_password_mismatch_is_not_blocked_by_frontend(self):
        """Verifica que o formulário NÃO possui validação de front-end para senhas divergentes."""
        # Este teste serve para documentar uma validação ausente.
        # Ele passará se o formulário NÃO impedir o envio ou mostrar um alerta.
        driver = self.driver
        form = driver.find_element(By.ID, 'passengerForm')
        
        form.find_element(By.CSS_SELECTOR, 'input[type="password"].password').send_keys('SenhaForte123!')
        # Preenche a confirmação com uma senha diferente
        form.find_element(By.CSS_SELECTOR, 'input[type="password"]:not(.password)').send_keys('OutraSenha456!')
        
        driver.execute_script("arguments[0].click();", form.find_element(By.CSS_SELECTOR, 'button[type="submit"]'))
        
        # A asserção verifica que NENHUM alerta de erro apareceu.
        try:
            alert = driver.switch_to.alert
            alert.accept() # Se um alerta aparecer, o teste falha.
            self.fail("Um alerta de erro de senha apareceu, o que não era esperado.")
        except NoAlertPresentException:
            # Se nenhum alerta apareceu, a validação de front-end não existe, e o teste passa.
            print("\n[INFO] Teste de senhas divergentes concluiu: Nenhuma validação de front-end encontrada.")
            pass
        
    # --- 3. TESTES DE FUNCIONALIDADE DA INTERFACE ---

    def test_switch_between_forms(self):
        """Testa a alternância entre os formulários de passageiro e motorista."""
        driver = self.driver
        passenger_form = driver.find_element(By.ID, 'passengerForm')
        driver_form = driver.find_element(By.ID, 'driverForm')
        driver_role_btn = driver.find_element(By.ID, 'driverRole')
        
        self.assertTrue(passenger_form.is_displayed())
        self.assertFalse(driver_form.is_displayed())
        
        # Clica para mostrar o formulário de motorista
        driver_role_btn.click()
        time.sleep(0.5)
        
        self.assertFalse(passenger_form.is_displayed())
        self.assertTrue(driver_form.is_displayed())
        self.assertTrue('active' in driver_role_btn.get_attribute('class'))
        print("\n[FUNCIONALIDADE] Alternância para formulário de motorista OK.")
        time.sleep(1)

    def test_password_toggle_visibility(self):
        """Testa a funcionalidade de alternar a visibilidade da senha no formulário de passageiro."""
        driver = self.driver
        form = driver.find_element(By.ID, 'passengerForm')
        password_input = form.find_element(By.CSS_SELECTOR, '.password')
        toggle_button = form.find_element(By.CSS_SELECTOR, 'button[onclick^="togglePassword"]')
        
        self.assertEqual(password_input.get_attribute('type'), 'password', "Senha deveria iniciar oculta.")
        
        toggle_button.click()
        time.sleep(0.5)
        self.assertEqual(password_input.get_attribute('type'), 'text', "Senha deveria estar visível.")
        
        toggle_button.click()
        time.sleep(0.5)
        self.assertEqual(password_input.get_attribute('type'), 'password', "Senha deveria voltar a ficar oculta.")
        print("[FUNCIONALIDADE] Botão de visibilidade da senha OK.")
        time.sleep(1)

class DriverProfileTest(unittest.TestCase):

    def setUp(self):
        """Configuração inicial para cada teste."""
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless") # Descomente para rodar sem interface gráfica
        self.driver = webdriver.Chrome(options=options)
        # self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

        # Carrega a página de perfil do motorista
        file_path = os.path.abspath('driver_profile.html')
        self.driver.get(f'file:///{file_path}')

        # Cria um arquivo dummy para testes de upload
        self.dummy_file_path = os.path.abspath('dummy_profile_image.txt')
        with open(self.dummy_file_path, "w") as f:
            f.write("Este é um arquivo de imagem de teste.")

    def tearDown(self):
        """Finaliza o teste, fechando o navegador e limpando arquivos."""
        if os.path.exists(self.dummy_file_path):
            os.remove(self.dummy_file_path)
        self.driver.quit()

    def test_initial_state_is_disabled(self):
        """Verifica se a página carrega em modo de visualização com campos desabilitados."""
        nome_input = self.driver.find_element(By.ID, 'nome')
        editar_btn = self.driver.find_element(By.ID, 'editarBtn')
        salvar_btn = self.driver.find_element(By.ID, 'salvarBtn')

        self.assertFalse(nome_input.is_enabled(), "O campo 'Nome' deveria estar desabilitado no início.")
        self.assertTrue(editar_btn.is_displayed(), "O botão 'Alterar Dados' deveria estar visível.")
        self.assertFalse(salvar_btn.is_displayed(), "O botão 'Salvar' deveria estar oculto.")
        print("\n[SUCESSO] Estado inicial da página verificado.")

    def test_edit_mode_activation_and_cancellation(self):
        """
        Testa o ciclo completo: ativar modo de edição, alterar um valor e cancelar, 
        verificando se o valor original é restaurado.
        """
        editar_btn = self.driver.find_element(By.ID, 'editarBtn')
        nome_input = self.driver.find_element(By.ID, 'nome')
        original_nome = nome_input.get_attribute('value')

        # 1. Ativa o modo de edição
        editar_btn.click()
        self.wait.until(EC.element_to_be_clickable((By.ID, 'salvarBtn')))
        self.assertTrue(nome_input.is_enabled(), "O campo 'Nome' deveria ser habilitado após clicar em editar.")
        
        # 2. Altera o valor
        novo_nome = "Nome Alterado Para Teste"
        nome_input.clear()
        nome_input.send_keys(novo_nome)
        self.assertEqual(nome_input.get_attribute('value'), novo_nome)
        print(f"\n[INFO] Nome alterado para: '{novo_nome}'")

        # 3. Cancela a edição
        self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.ID, 'cancelarBtn'))
        self.wait.until(EC.element_to_be_clickable((By.ID, 'editarBtn')))

        # 4. Verifica se o valor original foi restaurado e os campos desabilitados
        self.assertFalse(nome_input.is_enabled(), "O campo 'Nome' deveria ser desabilitado após cancelar.")
        self.assertEqual(nome_input.get_attribute('value'), original_nome, "O nome original deveria ter sido restaurado.")
        print("[SUCESSO] Ciclo de Edição e Cancelamento funcionou corretamente.")

    def _wait_for_and_handle_alert(self, expected_text_fragment):
        """
        Espera por um alerta de forma explícita, verifica seu texto e o aceita.
        Retorna o texto do alerta para verificação adicional se necessário.
        """
        try:
            # A condição EC.alert_is_present() ainda é a melhor prática,
            # mas o tratamento de exceção torna o teste mais claro sobre o que falhou.
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            self.assertIn(expected_text_fragment, alert_text)
            alert.accept()
            return alert_text
        except TimeoutException:
            self.fail("O alerta esperado não apareceu dentro do tempo limite.")
        except NoAlertPresentException:
            self.fail("Nenhum alerta estava presente quando a verificação foi feita.")

            
    def test_save_with_email_mismatch_alert(self):
        """Verifica se um alerta é exibido ao tentar salvar com e-mails divergentes."""
        self.driver.find_element(By.ID, 'editarBtn').click()
        self.wait.until(EC.element_to_be_clickable((By.ID, 'email')))
        
        email_input = self.driver.find_element(By.ID, 'email')
        email_input.clear()
        email_input.send_keys("novo.email@teste.com")
        
        # O campo de confirmação deve aparecer
        confirm_email_div = self.driver.find_element(By.CLASS_NAME, 'confirm-email')
        self.wait.until(EC.visibility_of(confirm_email_div))

        # Preenche com e-mail errado
        self.driver.find_element(By.ID, 'confirmEmail').send_keys("email.errado@teste.com")
        self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.ID, 'salvarBtn'))
        
        # Verifica o alerta
        alert = self.wait.until(EC.alert_is_present())
        self.assertIn("Os emails não coincidem!", alert.text)
        print(f"\n[SUCESSO] Alerta de e-mail divergente exibido: '{alert.text}'")
        alert.accept()

    def test_deactivate_account_flow(self):
        """Testa o fluxo de desativação da conta, da abertura do modal à confirmação."""
        self.driver.find_element(By.ID, 'desativarBtn').click()
        
        # Verifica se o modal de confirmação aparece
        confirm_modal = self.wait.until(EC.visibility_of_element_located((By.ID, 'confirmModal')))
        self.assertTrue(confirm_modal.is_displayed())
        
        # Clica no botão para confirmar a desativação dentro do modal
        self.driver.execute_script("arguments[0].click();",self.driver.find_element(By.ID, 'confirmarDesativar'))
        
        # Espera o modal desaparecer
        self.wait.until(EC.invisibility_of_element_located((By.ID, 'confirmModal')))

        # Verifica se a situação e o estado dos botões foram atualizados
        situacao_input = self.driver.find_element(By.ID, 'situacao')
        editar_btn = self.driver.find_element(By.ID, 'editarBtn')
        
        self.assertEqual(situacao_input.get_attribute('value'), 'Inativo')
        self.assertFalse(editar_btn.is_enabled(), "Botão 'Editar' deveria ser desabilitado após desativação.")
        print("\n[SUCESSO] Fluxo de desativação de conta verificado com sucesso.")

class PassengerProfileTest(unittest.TestCase):
    """
    Suíte de testes para a página de perfil do passageiro (passenger_profile.html).
    """

    def setUp(self):
        """Configuração inicial para cada teste."""
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless") # Descomente para rodar sem interface gráfica
        self.driver = webdriver.Chrome(options=options)
        # self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)

        # Carrega a página de perfil do passageiro
        file_path = os.path.abspath('passenger_profile.html')
        self.driver.get(f'file:///{file_path}')

    def tearDown(self):
        """Finaliza o teste, fechando o navegador."""
        self.driver.quit()

    def _wait_for_and_handle_alert(self, expected_text_fragment):
        """
        Método auxiliar que espera por um alerta, verifica seu texto e o aceita.
        """
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            self.assertIn(expected_text_fragment, alert_text)
            alert.accept()
            return alert_text
        except TimeoutException:
            self.fail(f"Alerta contendo '{expected_text_fragment}' não apareceu no tempo esperado.")

    def test_initial_state_is_view_mode(self):
        """✔️ Verifica se a página carrega corretamente em modo de visualização."""
        nome_input = self.driver.find_element(By.ID, 'nome')
        editar_btn = self.driver.find_element(By.ID, 'editarBtn')
        salvar_btn = self.driver.find_element(By.ID, 'salvarBtn')

        self.assertFalse(nome_input.is_enabled(), "O campo 'Nome' deveria estar desabilitado no início.")
        self.assertTrue(editar_btn.is_displayed(), "O botão 'Alterar Dados' deveria estar visível.")
        self.assertFalse(salvar_btn.is_displayed(), "O botão 'Salvar' deveria estar oculto.")
        print("\n[PASS] Estado inicial da página verificado com sucesso.")

    def test_edit_and_cancel_flow(self):
        """✔️ Testa o ciclo de edição e cancelamento, revertendo os dados."""
        editar_btn = self.driver.find_element(By.ID, 'editarBtn')
        nome_input = self.driver.find_element(By.ID, 'nome')
        original_nome = nome_input.get_attribute('value')

        # 1. Ativa o modo de edição
        editar_btn.click()
        self.wait.until(EC.element_to_be_clickable((By.ID, 'salvarBtn')))
        self.assertTrue(nome_input.is_enabled(), "O campo 'Nome' deveria ser habilitado.")
        
        # 2. Altera o nome
        novo_nome = "Nome de Teste"
        nome_input.clear()
        nome_input.send_keys(novo_nome)
        
        # 3. Clica em Cancelar
        self.driver.find_element(By.ID, 'cancelarBtn').click()
        self.wait.until(EC.element_to_be_clickable((By.ID, 'editarBtn')))

        # 4. Verifica se o valor original foi restaurado
        self.assertEqual(nome_input.get_attribute('value'), original_nome, "O nome original deveria ser restaurado.")
        self.assertFalse(nome_input.is_enabled(), "O campo 'Nome' deveria voltar a ser desabilitado.")
        print("\n[PASS] Fluxo de Edição e Cancelamento funcionou como esperado.")

    def test_edit_and_save_successfully(self):
        """✔️ Testa a edição e o salvamento de um campo simples."""
        self.driver.find_element(By.ID, 'editarBtn').click()
        self.wait.until(EC.element_to_be_clickable((By.ID, 'telefone')))

        telefone_input = self.driver.find_element(By.ID, 'telefone')
        novo_telefone = "(99) 99999-9999"
        telefone_input.clear()
        telefone_input.send_keys(novo_telefone)

        # Clica em Salvar
        self.driver.find_element(By.ID, 'salvarBtn').click()

        # Lida com o alerta de sucesso
        self._wait_for_and_handle_alert("Dados atualizados com sucesso!")

        # Verifica se os dados foram salvos e a página voltou ao modo de visualização
        self.wait.until(EC.element_to_be_clickable((By.ID, 'editarBtn')))
        self.assertEqual(telefone_input.get_attribute('value'), novo_telefone)
        self.assertFalse(telefone_input.is_enabled())
        print("\n[PASS] Edição e salvamento de dados concluídos com sucesso.")

    def test_email_change_with_mismatch_alert(self):
        """✔️ Testa a validação de e-mails divergentes ao salvar."""
        self.driver.find_element(By.ID, 'editarBtn').click()
        self.wait.until(EC.element_to_be_clickable((By.ID, 'email')))
        
        email_input = self.driver.find_element(By.ID, 'email')
        email_input.clear()
        email_input.send_keys("novo@teste.com")
        
        # Espera o campo de confirmação aparecer
        confirm_email_div = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'confirm-email')))
        self.assertTrue(confirm_email_div.is_displayed())

        # Preenche com e-mail errado e tenta salvar
        self.driver.find_element(By.ID, 'confirmEmail').send_keys("email-diferente@teste.com")
        self.driver.find_element(By.ID, 'salvarBtn').click()
        
        # Verifica se o alerta de erro correto é exibido
        self._wait_for_and_handle_alert("Os emails não coincidem!")
        print("\n[PASS] Alerta de e-mails divergentes foi exibido corretamente.")

    def test_deactivate_account_flow(self):
        """✔️ Testa o fluxo completo de desativação da conta pelo modal."""
        self.driver.find_element(By.ID, 'desativarBtn').click()
        
        # Espera o modal de confirmação aparecer
        self.wait.until(EC.visibility_of_element_located((By.ID, 'confirmModal')))
        
        # Clica para confirmar a desativação
        self.driver.find_element(By.ID, 'confirmarDesativar').click()
        
        # Espera o modal desaparecer
        self.wait.until(EC.invisibility_of_element_located((By.ID, 'confirmModal')))

        # Verifica o resultado
        situacao_input = self.driver.find_element(By.ID, 'situacao')
        editar_btn = self.driver.find_element(By.ID, 'editarBtn')
        
        self.assertEqual(situacao_input.get_attribute('value'), 'Inativo')
        self.assertFalse(editar_btn.is_enabled(), "O botão 'Editar' deveria ser desabilitado após a desativação.")
        print("\n[PASS] Fluxo de desativação de conta verificado com sucesso.")

class AdminPanelTest(unittest.TestCase):
    """
    Suíte de testes para o Painel do Administrador (admin.html).
    """

    def setUp(self):
        """Configuração inicial para cada teste."""
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        #self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)

        # Carrega a página do painel de admin
        file_path = os.path.abspath('admin.html')
        self.driver.get(f'file:///{file_path}')

    def tearDown(self):
        """Finaliza o teste, fechando o navegador."""
        self.driver.quit()

    def _wait_for_and_handle_alert(self, expected_text_fragment):
        """Método auxiliar que espera por um alerta, verifica seu texto e o aceita."""
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            self.assertIn(expected_text_fragment, alert_text)
            alert.accept()
            return alert_text
        except TimeoutException:
            self.fail(f"Alerta contendo '{expected_text_fragment}' não apareceu no tempo esperado.")

    def test_view_user_data_modal(self):
        """✔️ Testa a abertura do modal de visualização de dados do usuário."""
        # Localiza o botão "Ver dados" do primeiro passageiro
        view_button = self.driver.find_element(By.CSS_SELECTOR, ".card:first-child .view-btn")
        view_button.click()

        # Espera o modal aparecer
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#viewUserModal.show')))
        modal_body = self.driver.find_element(By.ID, 'userDetails')
        
        # Verifica se o conteúdo (simulado pelo JS) foi carregado
        self.assertIn("Nome:", modal_body.text)
        self.assertIn("CPF:", modal_body.text)
        
        # Fecha o modal
        self.driver.find_element(By.CSS_SELECTOR, "#viewUserModal .btn-close").click()
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#viewUserModal.show')))
        print("\n[PASS] Modal de visualização de dados abriu e fechou corretamente.")

    def test_approve_driver_flow_and_ui_update(self):
        """✔️ Testa o fluxo de aprovação de um motorista pendente e a atualização da UI."""
        # Localiza o motorista pendente "Carlos Mendes"
        carlos_li = self.driver.find_element(By.XPATH, "//li[contains(., 'Carlos Mendes')]")
        
        # 1. Verifica estado inicial
        self.assertIn("Pendente", carlos_li.find_element(By.CLASS_NAME, 'badge').text)
        self.assertTrue(carlos_li.find_element(By.CLASS_NAME, 'approve-btn').is_displayed())

        print("\n[INFO] Iniciando fluxo de aprovação do motorista 'Carlos Mendes'.")
        # 2. Clica em "Aprovar"
        carlos_li.find_element(By.CLASS_NAME, 'approve-btn').click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#actionModal.show')))
        
        print("[INFO] Modal de ação de aprovação aberto.")
        # 3. Confirma a ação (justificativa não é necessária para aprovar)
        self.driver.find_element(By.ID, 'confirmAction').click()
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#actionModal.show')))

        print("[INFO] Ação de aprovação confirmada, aguardando atualização da UI.")
        # 4. Verifica a atualização da UI no item do "Carlos Mendes"
        # Re-localiza o elemento para evitar StaleElementReferenceException
        carlos_li = self.driver.find_element(By.XPATH, "//li[contains(., 'Carlos Mendes')]")
        new_badge = carlos_li.find_element(By.CLASS_NAME, 'badge')
        self.assertIn("Aprovado", new_badge.text)
        self.assertEqual("badge bg-success", new_badge.get_attribute('class'))

        print("[INFO] Verificando os botões de ação após aprovação.")
        # Verifica se os botões foram trocados
        with self.assertRaises(NoSuchElementException, msg="O botão 'Aprovar' não deveria mais existir"):
            carlos_li.find_element(By.CLASS_NAME, 'approve-btn')
        self.assertTrue(carlos_li.find_element(By.CLASS_NAME, 'block-btn').is_displayed(), "O botão 'Bloquear' deveria ter aparecido.")
        print("\n[PASS] Fluxo de aprovação de motorista e atualização da UI concluído.")
        
    def test_block_user_requires_justification(self):
        """✔️ Testa se a ação de bloquear exige uma justificativa, mostrando um alerta."""
        # Localiza o botão "Bloquear" do primeiro passageiro
        block_button = self.driver.find_element(By.CSS_SELECTOR, ".card:first-child .block-btn")
        block_button.click()

        # Espera o modal de ação aparecer
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#actionModal.show')))
        
        # Clica em confirmar sem preencher a justificativa
        self.driver.find_element(By.ID, 'confirmAction').click()
        
        # Verifica o alerta
        self._wait_for_and_handle_alert("Por favor, forneça uma justificativa")
        print("\n[PASS] Alerta de justificativa obrigatória foi exibido.")

    def test_block_user_with_justification_completes_flow(self):
        """✔️ Testa se o fluxo de bloqueio com justificativa é concluído sem erros."""
        block_button = self.driver.find_element(By.CSS_SELECTOR, ".card:first-child .block-btn")
        block_button.click()

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#actionModal.show')))
        
        # Preenche a justificativa
        self.driver.find_element(By.ID, 'justification').send_keys("Usuário violou os termos de serviço.")
        self.driver.find_element(By.ID, 'confirmAction').click()
        
        # Apenas verifica se o modal fecha, pois o JS não atualiza a UI neste caso
        self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#actionModal.show')))
        print("\n[PASS] Fluxo de bloqueio com justificativa foi concluído.")

if __name__ == '__main__':
    unittest.main(verbosity=2)