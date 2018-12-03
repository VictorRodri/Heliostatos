%.pdf:  %.tex
	(export TEXINPUTS=${TEXINPUTS}; pdflatex $*)
	(export BIBINPUTS=${BIBINPUTS}; bibtex $*)
	(export TEXINPUTS=${TEXINPUTS}; pdflatex $*)
	@while ( grep "Rerun to get" $*.log > /dev/null ); do \
				echo '** Re-running LaTeX **'; \
				makeglossaries $*; \
				(export TEXINPUTS=${TEXINPUTS}; pdflatex --interaction errorstopmode $*); \
		done
default: main.pdf
main.pdf: main.tex main.bib *.tex
clean:
	rm -f *.aux *.bbl *.blg *.log *.toc *.acn *.acr *.alg *.glg *.glo *.gls *.ist *.out main.pdf