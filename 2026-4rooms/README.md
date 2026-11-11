# Стаття «Моделювання мультиагентної оркестрації "Чотири кімнати": системно-аналітичний підхід до завдань проектування»

В директорії міститься рукопис статті, оформлений згідно з шаблоном «Журналу обчислювальної та прикладної математики» (`article-template/template_ua.tex`) та вимогами щодо розкриття використання інструментів ШІ (`article-requirements-ai.txt`):

- `4_rooms_systems_analysis_article.pdf` - скомпільований PDF-файл статті (16 сторінок, клас `amsart`, формат текстового поля `13.1 x 21 см`, структура IMRAD).
- `4_rooms_systems_analysis_article.tex` - вихідний код рукопису в кодуванні UTF-8 (для збирання через `pdflatex`).
- `4_rooms_systems_analysis_article_cp1251.tex` - вихідний код рукопису в кодуванні Windows-1251 (ідентично до кодування `article-template/template_ua.tex`, для збирання через `latex + dvips + ps2pdf` або `pdflatex`).
- `fig_4rooms_src.tex`, `fig_4rooms.eps`, `fig_4rooms.pdf`, `fig_4rooms-eps-converted-to.pdf` - вихідний TikZ-код та векторні файли рисунка 1 (схема переходів станів моделі «Чотири кімнати»).

## Збирання PDF

Через `pdflatex` (UTF-8):

```bash
pdflatex 4_rooms_systems_analysis_article.tex
pdflatex 4_rooms_systems_analysis_article.tex
```

Через класичний конвеєр `latex + dvips + ps2pdf` (Windows-1251):

```bash
latex 4_rooms_systems_analysis_article_cp1251.tex
latex 4_rooms_systems_analysis_article_cp1251.tex
dvips 4_rooms_systems_analysis_article_cp1251.dvi -o 4_rooms_systems_analysis_article_cp1251.ps
ps2pdf 4_rooms_systems_analysis_article_cp1251.ps 4_rooms_systems_analysis_article.pdf
```
