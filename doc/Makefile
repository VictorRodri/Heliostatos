default:	main.pdf

main.pdf:	main.tex main.bib Capitulo*.tex
		pdflatex main
		@if grep "Warning: Citation" main.log; then bibtex main; \
		  pdflatex main; \
		fi;
		@while grep Rerun main.log; do \
		  pdflatex main; \
		done;

clean:
	rm *.aux *.bbl *.blg *.log *.toc main.pdf
