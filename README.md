# GEM UFSCar — Grupo de Estudos e Pesquisas em Educação Matemática

Site institucional do **Grupo de Estudos e Pesquisas em Educação Matemática (GEM)** da Universidade Federal de São Carlos (UFSCar). O grupo atua na pesquisa e na formação de professores que ensinam matemática desde 2003.

**Site publicado:** <https://gemufscar.pages.dev>

## Conteúdo

- **O GEM** — história, linhas de pesquisa e atividades do grupo;
- **Equipe** — pesquisadores, orientandos e colaboradores;
- **Produção científica** — artigos, capítulos e trabalhos apresentados;
- **Livros** — publicações organizadas pelo grupo;
- **Eventos** — encontros, seminários e defesas;
- **Contato** e **Visitantes**.

## Estrutura do repositório

| Caminho | Descrição |
|---|---|
| `index.html` | Página inicial |
| `o-gem.html`, `equipe.html`, `producao-cientifica.html` | Seções institucionais |
| `livros.html`, `eventos.html`, `contato.html`, `visitantes.html` | Demais seções |
| `css/` | Estilos (base, componentes e responsividade) |
| `js/` | Navegação e interações |
| `assets/` | Logos, fontes e imagens |
| `staticwebapp.config.json` | Configuração de publicação |

O site é estático e não exige etapa de compilação: basta publicar a raiz do repositório em um serviço de hospedagem estática, como Azure Static Web Apps, Netlify ou Cloudflare Pages.

## Publicação

O projeto inclui `staticwebapp.config.json`, preparado para **Azure Static Web Apps**. Para outros serviços, use a raiz do repositório como diretório de saída e não configure comando de build.

## Créditos

Grupo de Estudos e Pesquisas em Educação Matemática — UFSCar.
