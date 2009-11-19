#
# Compilación del latex.
#

design.pdf: design.tex
	pdflatex \\nonstopmode\\input design.tex

vision.pdf: vision.tex
	pdflatex \\nonstopmode\\input vision.tex

plan.pdf: vision.tex
	pdflatex \\nonstopmode\\input plan.tex

pdf: design.pdf vision.pdf plan.pdf

cleantmp:
	rm -f *.out *.log *.toc *.idx *~ *#

cleanout:
	rm -f *.pdf *.dvi *.tar.gz

clean: cleantmp cleanout

dist: 
	tar czvf design.tar.gz makefile *.tex *.sty *.pdf
