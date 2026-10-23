import json
import os
import re

SRC = '/app/memory/idcap/source.html'
OUT = '/app/frontend/public/idcap'
os.makedirs(OUT, exist_ok=True)

s = open(SRC, encoding='utf-8').read()

styles = [m.group(1) for m in re.finditer(r'<style>(.*?)</style>', s, re.S)][:3]
css = '\n'.join(styles)
css = re.sub(r'/\*!.*?\*/', '', css, flags=re.S)
fonts = re.findall(r'@font-face\{[^}]*\}', css)
css = re.sub(r'@font-face\{[^}]*\}', '', css)

css = css.replace('body:not(.home)', '.sfbody')
css = re.sub(r'(^|[}\s,>])html(?=[\s,{:.\[>])', r'\1:host', css)
css = re.sub(r'(^|[}\s,>])body(?=[\s,{:.\[>])', r'\1.sfbody', css)
css = css.replace(':root', ':host')
css += '''
:host{display:block}
.sfbody{font-family:"Silka",sans-serif;font-size:16px;line-height:1.5;color:#212529;background:#fff;text-align:left}
.sfbody a{text-decoration:none}
.sfbody .site__header{position:relative}
.sfbody .site__footer{margin-top:0}
a[href="#"]{cursor:default}
@media (min-width:992px) and (max-width:1199px){.site__header .container-fluid{padding:0 16px!important}.site__header .header__logo img{height:52px!important}.site__header .header__menu{padding:0 10px!important}.site__header .header__menu>ul{gap:14px!important}.site__header .header__menu>ul>li>a{font-size:12px!important}.site__header .header__panel .default__btn{font-size:12px!important;padding-left:14px!important;padding-right:14px!important;white-space:nowrap}}
.menu-on .header__toggle{opacity:1!important;visibility:visible!important}
.menu-on .header__toggle .toggle__content{margin:0!important}
'''

open(f'{OUT}/fonts.css', 'w', encoding='utf-8').write('\n'.join(fonts))
open(f'{OUT}/chrome.css', 'w', encoding='utf-8').write(css)

header = re.search(r'<header class=site__header>.*?</header>', s, re.S).group(0)
footer = re.search(r'<footer class="site__footer naoimprimir">.*?</footer>', s, re.S).group(0)


def fix_links(h):
    h = h.replace('<a href=https://idcap.selecao.net.br/painel/ class=default__btn>',
                  '<a href=/minhas-inscricoes.html class="default__btn header__action-follow-button" data-testid=header-minhas-inscricoes-btn>')
    h = h.replace('<a href=https://idcap.selecao.net.br/painel/>', '<a href=/minhas-inscricoes.html>')
    h = h.replace('<a href=https://idcap.selecao.net.br/>', '<a href=/>')
    h = h.replace('<a class=header__btn>', '<a class=header__btn id=idcap-menu-btn data-testid=mobile-menu-toggle>')
    h = re.sub(r'\s*target=_blank', '', h)
    h = re.sub(r'href="?https?://[^\s>"]+"?', 'href=#', h)
    return h


parts = {'h': fix_links(header), 'f': fix_links(footer), 'cls': 'idcap'}
json.dump(parts, open(f'{OUT}/parts.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('css', len(css), 'fonts', len(fonts), 'header', len(parts['h']), 'footer', len(parts['f']))
print('left external:', re.findall(r'https?://(?!www\.w3\.org)[^\s"\'>]+', parts['h'] + parts['f']))
