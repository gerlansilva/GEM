/* ==========================================================
   GEM UFSCar — main.js
   ========================================================== */
(function () {
  'use strict';

  var EMAIL_COORDENACAO = 'carmen@ufscar.br';

  /* --- Menu recolhível (telas pequenas) --- */
  function initNav() {
    var toggle = document.querySelector('.nav-toggle');
    var list = document.querySelector('.nav-list');
    if (!toggle || !list) return;

    function fechar(devolverFoco) {
      toggle.setAttribute('aria-expanded', 'false');
      list.classList.remove('open');
      if (devolverFoco) toggle.focus();
    }

    toggle.addEventListener('click', function () {
      var aberto = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!aberto));
      list.classList.toggle('open', !aberto);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && list.classList.contains('open')) fechar(true);
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 991) fechar(false);
    });
  }

  /* --- Linha sob o menu quando ele gruda no topo --- */
  function initNavSticky() {
    var nav = document.querySelector('.site-nav');
    if (!nav) return;
    function atualizar() {
      nav.classList.toggle('is-stuck', nav.getBoundingClientRect().top <= 0 && window.scrollY > 0);
    }
    atualizar();
    window.addEventListener('scroll', atualizar, { passive: true });
  }

  /* --- Voltar ao topo --- */
  function initBackToTop() {
    var btn = document.querySelector('.back-to-top');
    if (!btn) return;
    function atualizar() { btn.classList.toggle('visible', window.scrollY > 500); }
    atualizar();
    window.addEventListener('scroll', atualizar, { passive: true });
    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* --- Filtros da Produção Científica: tipo e orientadora --- */
  function initFilters() {
    var tipos = document.querySelectorAll('[data-filter]');
    var orients = document.querySelectorAll('[data-orient]');
    if (!tipos.length) return;
    var estado = { tipo: (document.querySelector('[data-filter].active') || tipos[0]).getAttribute('data-filter'), orient: 'all' };

    function aplicar(escopo) {
      escopo.querySelectorAll('[data-category]').forEach(function (item) {
        var ok = (estado.tipo === 'all' || item.getAttribute('data-category') === estado.tipo) &&
                 (estado.orient === 'all' || item.getAttribute('data-orientadora') === estado.orient);
        item.style.display = ok ? '' : 'none';
      });
      escopo.querySelectorAll('[data-filter-section]').forEach(function (sec) {
        var alvo = sec.getAttribute('data-filter-section');
        var temItem = Array.prototype.some.call(
          escopo.querySelectorAll('[data-category="' + alvo + '"]'),
          function (i) { return i.style.display !== 'none'; });
        sec.style.display = ((estado.tipo === 'all' || estado.tipo === alvo) && temItem) ? '' : 'none';
      });
    }

    function ligar(botoes, chave, attr) {
      botoes.forEach(function (btn) {
        btn.addEventListener('click', function () {
          botoes.forEach(function (b) { b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); });
          btn.classList.add('active');
          btn.setAttribute('aria-pressed', 'true');
          estado[chave] = btn.getAttribute(attr);
          aplicar(btn.closest('[data-page]') || document);
        });
      });
    }
    ligar(tipos, 'tipo', 'data-filter');
    ligar(orients, 'orient', 'data-orient');
    aplicar(document);
  }

  /* --- Formulário de contato: valida e abre o e-mail já preenchido --- */
  function initContactForm() {
    var form = document.getElementById('contact-form');
    if (!form) return;
    var status = form.parentElement.querySelector('.form-status');

    function mostrar(tipo, texto) {
      if (!status) return;
      status.className = 'alert alert-' + tipo + ' form-status';
      status.textContent = texto;
      status.hidden = false;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var valido = true;

      form.querySelectorAll('[required]').forEach(function (campo) {
        var grupo = campo.closest('.form-group');
        var vazio = !campo.value.trim();
        var emailOk = campo.type !== 'email' || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(campo.value);
        var erro = vazio || !emailOk;
        if (grupo) grupo.classList.toggle('form-error', erro);
        if (erro) valido = false;
      });

      if (!valido) {
        mostrar('danger', 'Preencha os campos obrigatórios para continuar.');
        var primeiro = form.querySelector('.form-error .form-control');
        if (primeiro) primeiro.focus();
        return;
      }

      var dados = new FormData(form);
      var assunto = '[Site GEM] ' + dados.get('assunto');
      var corpo = [
        'Nome: ' + dados.get('nome'),
        'E-mail: ' + dados.get('email'),
        'Instituição: ' + (dados.get('instituicao') || '—'),
        '',
        dados.get('mensagem')
      ].join('\n');

      window.location.href = 'mailto:' + EMAIL_COORDENACAO +
        '?subject=' + encodeURIComponent(assunto) +
        '&body=' + encodeURIComponent(corpo);

      mostrar('success', 'Abrimos o seu aplicativo de e-mail com a mensagem pronta. Basta enviar.');
    });

    form.querySelectorAll('.form-control').forEach(function (campo) {
      campo.addEventListener('input', function () {
        var grupo = campo.closest('.form-group');
        if (grupo) grupo.classList.remove('form-error');
      });
    });
  }

  /* --- Capas de livros: sem a imagem, aparece a capa tipográfica --- */
  function initCapas() {
    document.querySelectorAll('.capa-img').forEach(function (img) {
      function semImagem() { img.parentElement.classList.add('sem-imagem'); }
      img.addEventListener('error', semImagem);
      if (img.complete && img.naturalWidth === 0) semImagem();
    });
  }

  /* --- Ano do rodapé --- */
  function initYear() {
    document.querySelectorAll('[data-year]').forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  function init() {
    initNav();
    initNavSticky();
    initBackToTop();
    initFilters();
    initContactForm();
    initYear();
    initCapas();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
