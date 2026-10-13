#!/usr/bin/env python3
"""Aplica as alterações da equipe e produção científica no site GEM.
Execute na raiz do projeto: python3 aplicar_alteracoes_gem.py
"""
from pathlib import Path
import re, shutil, sys

root=Path.cwd()
team=root/'equipe.html'
pubs=root/'producao-cientifica.html'
css=root/'css'/'components.css'
photos=root/'assets'/'images'
source=Path(__file__).resolve().parent/'assets'/'images'
for p in (team,pubs,css):
    if not p.is_file():
        sys.exit(f'Arquivo não encontrado: {p}. Execute o script na pasta raiz do repositório GEM.')
for slug in ('carmen','keli','everaldo'):
    if not (source/f'{slug}-gem.jpg').is_file():
        sys.exit(f'Fotografia não encontrada no pacote: {slug}-gem.jpg')

original_team=team.read_text(encoding='utf-8')
original_pubs=pubs.read_text(encoding='utf-8')
original_css=css.read_text(encoding='utf-8')

people=[('carmen','Cármen Lúcia Brancaglion Passos','Coordenadora','2297203444364327'),('keli','Keli Cristina Conti','Coordenadora','5426381590352588'),('everaldo','Everaldo Gomes Leandro','Coordenador','8396222420157779')]
html='        <div class="coordenadores-grid">\n'
for slug,name,role,lattes in people:
    html+=f'''          <article class="coordenador-card">
            <div class="coordenador-visual coordenador-visual--{slug}">
              <span class="coordenador-mancha" aria-hidden="true"></span>
              <img class="coordenador-foto" src="assets/images/{slug}-gem.jpg" alt="Fotografia de {name}" width="220" height="220" loading="lazy">
            </div>
            <h3>{name}</h3>
            <p class="pessoa-papel">{role}</p>
            <a href="http://lattes.cnpq.br/{lattes}" target="_blank" rel="noopener noreferrer">Currículo Lattes</a>
          </article>
'''
html+='        </div>\n'

if '<div class="coordenadores-grid">' in original_team:
    team_updated=original_team
else:
    begin=original_team.find('        <div class="pessoas">',original_team.find('<h2>Coordenadores</h2>'))
    end=original_team.find('        <div class="section-intro" style="margin-top:',begin)
    if begin<0 or end<0:sys.exit('Não localizei a seção dos coordenadores, evitando alterações inseguras.')
    team_updated=original_team[:begin]+html+original_team[end:]
team_updated=team_updated.replace('<div class="section-intro">\n          <h2>Coordenadores</h2>', '<div class="section-intro section-intro--centro">\n          <h2>Coordenadores</h2>')
# Centraliza os títulos e o conjunto de participantes ativos na página Equipe.
team_updated=team_updated.replace('<h2>Participantes ativos</h2>', '<h2>Participantes ativos</h2>')
team_updated=team_updated.replace('<div class="section-intro" style="margin-top: var(--space-2xl);">', '<div class="section-intro section-intro--centro" style="margin-top: var(--space-2xl);">')
# Classe exclusiva para não alterar listas semelhantes em outras páginas.
team_updated=re.sub(r'(<h2>Participantes ativos</h2>.*?</div>\s*)<div class="pessoas">',r'\1<div class="pessoas pessoas--centralizadas">',team_updated,count=1,flags=re.DOTALL)

# Retira todos os filtros visuais da produção científica, preservando as listas.
selector=r'<div class="filters" role="group" aria-label="Filtrar por (?:tipo|orientadora)">.*?</div>'
pubs_updated,n=re.subn(selector,'',original_pubs,flags=re.DOTALL)
if re.search(r'<div class="filters"',pubs_updated):
    sys.exit('Há filtros com outro formato na página; revise antes de publicar.')

marker='/* GEM — layout fotográfico da coordenação (2026) */'
style='''
/* GEM — layout fotográfico da coordenação (2026) */
.coordenadores-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:clamp(1.25rem,3vw,3rem); justify-items:center; align-items:start; margin-bottom:var(--space-xl); }
.coordenador-card { min-width:0; width:100%; display:flex; flex-direction:column; align-items:center; text-align:center; }
.coordenador-visual { width:min(100%,290px); aspect-ratio:1; position:relative; display:grid; place-items:center; margin-bottom:1.1rem; }
.coordenador-mancha { position:absolute; inset:2%; background:var(--cor-mancha); border-radius:48% 52% 44% 56% / 55% 43% 57% 45%; transform:rotate(-9deg); }
.coordenador-visual--carmen { --cor-mancha:#f58e8e; }
.coordenador-visual--keli { --cor-mancha:#ffd063; }
.coordenador-visual--keli .coordenador-mancha { transform:rotate(10deg); }
.coordenador-visual--everaldo { --cor-mancha:#9cb5a0; }
.coordenador-visual--everaldo .coordenador-mancha { transform:rotate(-4deg); }
.coordenador-foto { position:relative; z-index:1; width:78%; aspect-ratio:1; height:auto; object-fit:cover; object-position:center; border-radius:50%; display:block; border:4px solid var(--papel); }
.coordenador-card h3 { font-size:clamp(1.3rem,2vw,1.85rem); line-height:1.2; margin:0 0 .45rem; max-width:18ch; }
.coordenador-card .pessoa-papel { font-weight:500; margin-bottom:.65rem; }
.coordenador-card a { font-weight:700; text-decoration-color:var(--laranja); text-decoration-thickness:2px; text-underline-offset:5px; }
@media (max-width:850px) { .coordenadores-grid { grid-template-columns:repeat(2,minmax(0,1fr)); row-gap:2.5rem; } }
@media (max-width:560px) { .coordenadores-grid { grid-template-columns:1fr; } .coordenador-visual { max-width:260px; } }
/* Participantes ativos: cartões, textos e manchas centralizados. */
.pessoas--centralizadas { justify-items:center; gap:2rem; }
.pessoas--centralizadas .pessoa { display:flex; flex-direction:column; align-items:center; text-align:center; width:100%; max-width:340px; gap:.35rem; }
.pessoas--centralizadas .pessoa .avatar { width:110px; height:106px; margin-bottom:.6rem; flex-shrink:0; }
.pessoas--centralizadas .pessoa > div:last-child { width:100%; text-align:center; }
.pessoas--centralizadas .pessoa h3 { margin-inline:auto; }
.pessoas--centralizadas .pessoa a { display:inline-block; margin-top:.3rem; }
@media (max-width:720px) { .pessoas--centralizadas { grid-template-columns:1fr; } }
'''
css_updated=original_css if marker in original_css else original_css.rstrip()+'\n'+style

# All checks passed: now write the three edited files and photos.
for file,content in [(team,team_updated),(pubs,pubs_updated),(css,css_updated)]:
    if file.read_text(encoding='utf-8')!=content:
        file.with_suffix(file.suffix+'.bak').write_text(file.read_text(encoding='utf-8'),encoding='utf-8')
        file.write_text(content,encoding='utf-8')
        print('Atualizado:',file.relative_to(root))
    else:print('Já atualizado:',file.relative_to(root))
photos.mkdir(parents=True,exist_ok=True)
for slug in ('carmen','keli','everaldo'):
    filename=f'{slug}-gem.jpg'
    if (source/filename).resolve() != (photos/filename).resolve():
        shutil.copy2(source/filename,photos/filename)
    print('Fotografia:',(photos/filename).relative_to(root))
print('Concluído. Confira equipe.html e producao-cientifica.html antes de publicar.')
