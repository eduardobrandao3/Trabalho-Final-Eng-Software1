// Máscaras de CPF e Telefone usando jQuery Mask
$(function () {
  $(".cpf").mask("000.000.000-00", { reverse: true });
  $(".phone").mask("(00) 00000-0000");
});

// Alternar visibilidade da senha
function togglePassword(button) {
  const input = button.closest(".input-group").querySelector(".password");
  const icon = button.querySelector("i");

  if (input.type === "password") {
    input.type = "text";
    icon.classList.replace("fa-eye", "fa-eye-slash");
  } else {
    input.type = "password";
    icon.classList.replace("fa-eye-slash", "fa-eye");
  }
}

// Alternar tema claro/escuro
const themeBtn = document.getElementById("themeToggle");
if (themeBtn) {
  themeBtn.addEventListener("click", () => {
    document.body.classList.toggle("theme-dark");
    const icon = themeBtn.querySelector("i");
    icon.classList.toggle("fa-moon");
    icon.classList.toggle("fa-sun");
  });
}

// Selecionar tipo de cadastro (passageiro ou motorista)
function selectRole(role) {
  const passengerBtn = document.getElementById("passengerRole");
  const driverBtn = document.getElementById("driverRole");
  const passengerForm = document.getElementById("passengerForm");
  const driverForm = document.getElementById("driverForm");

  if (!passengerBtn || !driverBtn || !passengerForm || !driverForm) return;

  passengerBtn.classList.toggle("active", role === "passenger");
  driverBtn.classList.toggle("active", role === "driver");

  passengerForm.classList.toggle("hidden", role !== "passenger");
  driverForm.classList.toggle("hidden", role !== "driver");
}

// Redirecionamento de login simulado
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const accountType = document.getElementById("accountType").value;

    if (accountType === "passenger") {
      window.location.href = "passenger_profile.html";
    } else if (accountType === "driver") {
      window.location.href = "driver_profile.html";
    } else if (accountType === "admin") {
      window.location.href = "admin.html";
    }
  });
}

// Redirecionamento dos botões da tela de seleção de login
const loginPassengerBtn = document.getElementById("loginPassengerBtn");
if (loginPassengerBtn) {
  loginPassengerBtn.addEventListener("click", () => {
    window.location.href = "login.html?type=passenger";
  });
}

const loginDriverBtn = document.getElementById("loginDriverBtn");
if (loginDriverBtn) {
  loginDriverBtn.addEventListener("click", () => {
    window.location.href = "login.html?type=driver";
  });
}

const loginAdminBtn = document.getElementById("loginAdminBtn");
if (loginAdminBtn) {
  loginAdminBtn.addEventListener("click", () => {
    window.location.href = "login.html?type=admin";
  });
}

// Redirecionamento da tela de perfil do passageiro/motorista
const backToLoginBtn = document.getElementById("backToLogin");
if (backToLoginBtn) {
  backToLoginBtn.addEventListener("click", () => {
    window.location.href = "index.html";
  });
}

// Funções específicas para passenger_profile.html
document.addEventListener("DOMContentLoaded", function () {
  // Verifica se estamos na página de perfil do passageiro
  if (document.getElementById("profileForm")) {
    const editarBtn = document.getElementById("editarBtn");
    const salvarBtn = document.getElementById("salvarBtn");
    const cancelarBtn = document.getElementById("cancelarBtn");
    const desativarBtn = document.getElementById("desativarBtn");
    const confirmarDesativar = document.getElementById("confirmarDesativar");
    const confirmModal = new bootstrap.Modal(
      document.getElementById("confirmModal")
    );
    const emailInput = document.getElementById("email");
    const confirmEmailDiv = document.querySelector(".confirm-email");

    // Máscaras para campos
    $(".cpf").mask("000.000.000-00", { reverse: true });
    $(".phone").mask("(00) 00000-0000");

    // Armazena os valores originais para possível cancelamento
    let originalValues = {};

    // Botão Editar
    editarBtn.addEventListener("click", function () {
      // Salva os valores atuais
      originalValues = {
        nome: document.getElementById("nome").value,
        dataNascimento: document.getElementById("dataNascimento").value,
        telefone: document.getElementById("telefone").value,
        email: emailInput.value,
      };

      // Habilita edição dos campos (exceto CPF e sexo)
      document.getElementById("nome").disabled = false;
      document.getElementById("dataNascimento").disabled = false;
      document.getElementById("telefone").disabled = false;
      emailInput.disabled = false;

      // Mostra/Esconde botões
      editarBtn.classList.add("hidden");
      salvarBtn.classList.remove("hidden");
      cancelarBtn.classList.remove("hidden");
    });

    // Botão Cancelar
    cancelarBtn.addEventListener("click", function () {
      // Restaura os valores originais
      document.getElementById("nome").value = originalValues.nome;
      document.getElementById("dataNascimento").value =
        originalValues.dataNascimento;
      document.getElementById("telefone").value = originalValues.telefone;
      emailInput.value = originalValues.email;

      // Desabilita os campos
      document.getElementById("nome").disabled = true;
      document.getElementById("dataNascimento").disabled = true;
      document.getElementById("telefone").disabled = true;
      emailInput.disabled = true;

      // Esconde confirmação de email se estiver visível
      confirmEmailDiv.classList.add("hidden");
      document.getElementById("confirmEmail").value = "";

      // Mostra/Esconde botões
      editarBtn.classList.remove("hidden");
      salvarBtn.classList.add("hidden");
      cancelarBtn.classList.add("hidden");
    });

    // Botão Desativar
    desativarBtn.addEventListener("click", function () {
      confirmModal.show();
    });

    // Confirmação de desativação
    confirmarDesativar.addEventListener("click", function () {
      document.getElementById("situacao").value = "Inativo";
      confirmModal.hide();

      // Desabilita todos os campos e botões
      document.getElementById("nome").disabled = true;
      document.getElementById("dataNascimento").disabled = true;
      document.getElementById("telefone").disabled = true;
      emailInput.disabled = true;

      editarBtn.disabled = true;
      salvarBtn.classList.add("hidden");
      cancelarBtn.classList.add("hidden");
    });

    // Verifica mudança no email para pedir confirmação
    emailInput.addEventListener("change", function () {
      if (emailInput.value !== originalValues.email) {
        confirmEmailDiv.classList.remove("hidden");
      } else {
        confirmEmailDiv.classList.add("hidden");
      }
    });

    // Validação do formulário
    document
      .getElementById("profileForm")
      .addEventListener("submit", function (e) {
        e.preventDefault();

        // Verifica se email foi alterado e se a confirmação bate
        if (emailInput.value !== originalValues.email) {
          const confirmEmail = document.getElementById("confirmEmail").value;
          if (emailInput.value !== confirmEmail) {
            alert("Os emails não coincidem!");
            return;
          }
        }

        // Aqui você pode adicionar código para salvar os dados no servidor

        // Desabilita os campos após salvar
        document.getElementById("nome").disabled = true;
        document.getElementById("dataNascimento").disabled = true;
        document.getElementById("telefone").disabled = true;
        emailInput.disabled = true;
        confirmEmailDiv.classList.add("hidden");

        // Mostra/Esconde botões
        editarBtn.classList.remove("hidden");
        salvarBtn.classList.add("hidden");
        cancelarBtn.classList.add("hidden");

        alert("Dados atualizados com sucesso!");
      });
  }
});

// Funções específicas para driver_profile.html
document.addEventListener("DOMContentLoaded", function () {
  // Verifica se estamos na página de perfil do motorista
  if (
    document.getElementById("profileForm") &&
    document.getElementById("cnh")
  ) {
    const editarBtn = document.getElementById("editarBtn");
    const salvarBtn = document.getElementById("salvarBtn");
    const cancelarBtn = document.getElementById("cancelarBtn");
    const desativarBtn = document.getElementById("desativarBtn");
    const confirmarDesativar = document.getElementById("confirmarDesativar");
    const confirmModal = new bootstrap.Modal(
      document.getElementById("confirmModal")
    );
    const docsModal = new bootstrap.Modal(document.getElementById("docsModal"));
    const emailInput = document.getElementById("email");
    const confirmEmailDiv = document.querySelector(".confirm-email");
    const documentosSection = document.getElementById("documentosSection");
    const profileImageUpload = document.getElementById("profileImageUpload");
    const profileImageInput = document.getElementById("profileImageInput");
    const profileImage = document.getElementById("profileImage");
    const validadeCnhInput = document.getElementById("validadeCnh");
    const categoriaCnhSelect = document.getElementById("categoriaCnh");
    const cnhFotoInput = document.getElementById("cnhFoto");

    // Máscaras para campos
    $(".cpf").mask("000.000.000-00", { reverse: true });
    $(".phone").mask("(00) 00000-0000");

    // Armazena os valores originais para possível cancelamento
    let originalValues = {};
    let precisaEnviarDocs = false;

    // Botão Editar
    editarBtn.addEventListener("click", function () {
      // Salva os valores atuais
      originalValues = {
        nome: document.getElementById("nome").value,
        dataNascimento: document.getElementById("dataNascimento").value,
        telefone: document.getElementById("telefone").value,
        email: emailInput.value,
        validadeCnh: validadeCnhInput.value,
        categoriaCnh: categoriaCnhSelect.value,
      };

      // Habilita edição dos campos permitidos
      document.getElementById("nome").disabled = false;
      document.getElementById("dataNascimento").disabled = false;
      document.getElementById("telefone").disabled = false;
      emailInput.disabled = false;
      validadeCnhInput.disabled = false;
      categoriaCnhSelect.disabled = false;
      profileImageUpload.classList.remove("hidden");

      // Mostra/Esconde botões e seções
      editarBtn.classList.add("hidden");
      salvarBtn.classList.remove("hidden");
      cancelarBtn.classList.remove("hidden");
      documentosSection.classList.remove("hidden");
    });

    // Botão Cancelar
    cancelarBtn.addEventListener("click", function () {
      // Restaura os valores originais
      document.getElementById("nome").value = originalValues.nome;
      document.getElementById("dataNascimento").value =
        originalValues.dataNascimento;
      document.getElementById("telefone").value = originalValues.telefone;
      emailInput.value = originalValues.email;
      validadeCnhInput.value = originalValues.validadeCnh;
      categoriaCnhSelect.value = originalValues.categoriaCnh;

      // Desabilita os campos
      document.getElementById("nome").disabled = true;
      document.getElementById("dataNascimento").disabled = true;
      document.getElementById("telefone").disabled = true;
      emailInput.disabled = true;
      validadeCnhInput.disabled = true;
      categoriaCnhSelect.disabled = true;
      profileImageUpload.classList.add("hidden");

      // Esconde confirmação de email se estiver visível
      confirmEmailDiv.classList.add("hidden");
      document.getElementById("confirmEmail").value = "";
      documentosSection.classList.add("hidden");

      // Mostra/Esconde botões
      editarBtn.classList.remove("hidden");
      salvarBtn.classList.add("hidden");
      cancelarBtn.classList.add("hidden");
    });

    // Botão Desativar
    desativarBtn.addEventListener("click", function () {
      confirmModal.show();
    });

    // Confirmação de desativação
    confirmarDesativar.addEventListener("click", function () {
      document.getElementById("situacao").value = "Inativo";
      confirmModal.hide();

      // Desabilita todos os campos e botões
      document.getElementById("nome").disabled = true;
      document.getElementById("dataNascimento").disabled = true;
      document.getElementById("telefone").disabled = true;
      emailInput.disabled = true;
      validadeCnhInput.disabled = true;
      categoriaCnhSelect.disabled = true;

      editarBtn.disabled = true;
      salvarBtn.classList.add("hidden");
      cancelarBtn.classList.add("hidden");
    });

    // Fechar modal quando clicar em NÃO (CORREÇÃO ADICIONADA)
    document.querySelector('#confirmModal .btn-secondary').addEventListener('click', function() {
      confirmModal.hide(); // Fecha o modal corretamente
    });

    // Verifica mudança no email para pedir confirmação
    emailInput.addEventListener("change", function () {
      if (emailInput.value !== originalValues.email) {
        confirmEmailDiv.classList.remove("hidden");
      } else {
        confirmEmailDiv.classList.add("hidden");
      }
    });

    // Verifica mudanças na CNH para exigir envio de documentos
    validadeCnhInput.addEventListener("change", checkCnhChanges);
    categoriaCnhSelect.addEventListener("change", checkCnhChanges);

    function checkCnhChanges() {
      precisaEnviarDocs =
        validadeCnhInput.value !== originalValues.validadeCnh ||
        categoriaCnhSelect.value !== originalValues.categoriaCnh;

      if (precisaEnviarDocs) {
        cnhFotoInput.required = true;
      } else {
        cnhFotoInput.required = false;
      }
    }

    // Visualização da imagem de perfil antes do upload
    profileImageInput.addEventListener("change", function (e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
          profileImage.src = event.target.result;
        };
        reader.readAsDataURL(file);
      }
    });

    // Validação do formulário
    document
      .getElementById("profileForm")
      .addEventListener("submit", function (e) {
        e.preventDefault();

        // Verifica se email foi alterado e se a confirmação bate
        if (emailInput.value !== originalValues.email) {
          const confirmEmail = document.getElementById("confirmEmail").value;
          if (emailInput.value !== confirmEmail) {
            alert("Os emails não coincidem!");
            return;
          }
        }

        // Verifica se CNH foi alterada e se documentos foram enviados
        if (precisaEnviarDocs && !cnhFotoInput.files.length) {
          alert(
            "Você deve enviar uma nova foto da CNH para alterar validade ou categoria!"
          );
          return;
        }

        // Aqui você pode adicionar código para salvar os dados no servidor

        // Se houve alteração na CNH ou documentos foram enviados
        if (
          precisaEnviarDocs ||
          cnhFotoInput.files.length ||
          document.getElementById("comprovanteResidencia").files.length ||
          document.getElementById("atestadoAntecedentes").files.length
        ) {
          document.getElementById("situacao").value = "Pendente";
          docsModal.show();
        }

        // Desabilita os campos após salvar
        document.getElementById("nome").disabled = true;
        document.getElementById("dataNascimento").disabled = true;
        document.getElementById("telefone").disabled = true;
        emailInput.disabled = true;
        validadeCnhInput.disabled = true;
        categoriaCnhSelect.disabled = true;
        confirmEmailDiv.classList.add("hidden");
        profileImageUpload.classList.add("hidden");
        documentosSection.classList.add("hidden");

        // Mostra/Esconde botões
        editarBtn.classList.remove("hidden");
        salvarBtn.classList.add("hidden");
        cancelarBtn.classList.add("hidden");
      });
  }
});

// Funções para o painel de admin
document.addEventListener("DOMContentLoaded", function () {
  // Configura busca por CPF
  setupSearch();

  // Configura botões de ação
  setupActionButtons();
});

function setupSearch() {
  document.querySelectorAll(".search-cpf").forEach((input) => {
    input.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase();
      const listItems =
        this.closest(".card-body").querySelectorAll(".list-group-item");

      listItems.forEach((item) => {
        const userName = item
          .querySelector("span:first-child")
          .textContent.toLowerCase();
        const cpf = item.dataset.cpf || ""; // Você precisará adicionar data-cpf nos itens
        const showItem =
          userName.includes(searchTerm) || cpf.includes(searchTerm);
        item.style.display = showItem ? "block" : "none";
      });
    });
  });
}

function setupActionButtons() {
  // Botão de visualizar
  document.querySelectorAll(".view-btn").forEach((btn) => {
    btn.addEventListener("click", function () {
      const userType = this.getAttribute("data-user-type");
      const userName =
        this.closest(".list-group-item").querySelector(
          "span:first-child"
        ).textContent;

      // Simulação de dados - na prática você buscaria esses dados do backend
      const userData = {
        passenger: {
          name: userName,
          cpf: "123.456.789-00",
          email: `${userName.toLowerCase().replace(" ", ".")}@email.com`,
          phone: "(11) 98765-4321",
          status:
            this.closest(".list-group-item").querySelector(".badge")
              .textContent,
        },
        driver: {
          name: userName,
          cpf: "987.654.321-00",
          email: `${userName.toLowerCase().replace(" ", ".")}@email.com`,
          phone: "(11) 91234-5678",
          cnh: "12345678900",
          plate: "ABC1D23",
          status:
            this.closest(".list-group-item").querySelector(".badge")
              .textContent,
        },
      };

      displayUserDetails(userData[userType], userType);
    });
  });

  // Botões de ação (bloquear/aprovar/recusar)
  document
    .querySelectorAll(".block-btn, .approve-btn, .reject-btn")
    .forEach((btn) => {
      btn.addEventListener("click", function () {
        const action = this.classList.contains("block-btn")
          ? "bloquear"
          : this.classList.contains("approve-btn")
          ? "aprovar"
          : "recusar";
        const userType = this.getAttribute("data-user-type");
        const userName =
          this.closest(".list-group-item").querySelector(
            "span:first-child"
          ).textContent;

        showActionModal(action, userType, userName, this);
      });
    });
}

function displayUserDetails(user, userType) {
  const modalTitle = document.querySelector("#viewUserModal .modal-title");
  modalTitle.textContent = `Detalhes do ${
    userType === "passenger" ? "Passageiro" : "Motorista"
  }`;

  let detailsHTML = `
    <p><strong>Nome:</strong> ${user.name}</p>
    <p><strong>CPF:</strong> ${user.cpf}</p>
    <p><strong>E-mail:</strong> ${user.email}</p>
    <p><strong>Telefone:</strong> ${user.phone}</p>
    <p><strong>Status:</strong> <span class="badge ${getStatusBadgeClass(
      user.status
    )}">${user.status}</span></p>
  `;

  if (userType === "driver") {
    detailsHTML += `
      <p><strong>CNH:</strong> ${user.cnh}</p>
      <p><strong>Placa do Veículo:</strong> ${user.plate}</p>
    `;
  }

  document.getElementById("userDetails").innerHTML = detailsHTML;
  const modal = new bootstrap.Modal(document.getElementById("viewUserModal"));
  modal.show();
}

function showActionModal(action, userType, userName, buttonElement) {
  const modalTitle = document.getElementById("actionModalTitle");
  modalTitle.textContent = `${
    action.charAt(0).toUpperCase() + action.slice(1)
  } ${userType === "passenger" ? "Passageiro" : "Motorista"}`;

  const justificationField = document.getElementById("justification");
  justificationField.required = action !== "aprovar";

  const modal = new bootstrap.Modal(document.getElementById("actionModal"));
  modal.show();

  document.getElementById("confirmAction").onclick = function () {
    const justification = justificationField.value;

    if (justificationField.required && !justification) {
      alert("Por favor, forneça uma justificativa");
      return;
    }

    // Aqui você faria a requisição para o backend
    console.log(`Ação: ${action} ${userType} ${userName}`);
    console.log(`Justificativa: ${justification}`);

    // Atualiza a interface
    if (action === "aprovar") {
      const badge = buttonElement
        .closest(".list-group-item")
        .querySelector(".badge");
      badge.className = "badge bg-success";
      badge.textContent = "Aprovado";

      // Remove botões de aprovar/recusar e adiciona o de bloquear
      const actionsDiv = buttonElement.closest(".user-actions");
      actionsDiv.innerHTML = `
        <button class="btn btn-sm btn-info view-btn" data-user-type="${userType}">Ver dados</button>
        <button class="btn btn-sm btn-warning block-btn" data-user-type="${userType}">Bloquear</button>
      `;
      setupActionButtons(); // Reconfigura os listeners
    }

    modal.hide();
  };
}

function getStatusBadgeClass(status) {
  switch (status.toLowerCase()) {
    case "ativo":
    case "aprovado":
      return "bg-success";
    case "inativo":
    case "recusado":
      return "bg-danger";
    case "pendente":
      return "bg-warning text-dark";
    default:
      return "bg-secondary";
  }
}

// Adicione esta função no final do arquivo
// Função para inicializar máscaras de placa e RENAVAM
function initVehicleMasks() {
  // Máscara para placa (AAA-0000 ou AAA0A00)
  $(".placa").mask("SSS-0000", {
    translation: {
      'S': { pattern: /[A-Za-z]/ }
    },
    placeholder: "ABC-1234"
  });

  // Máscara para RENAVAM (11 dígitos)
  $(".renavam").mask("00000000000");
}

// Chame esta função quando a página for carregada
$(function() {
  // ... código existente ...
  
  // Inicializa máscaras se estiver na página de cadastro de veículo
  if (document.getElementById('vehicleForm')) {
    initVehicleMasks();
  }
});