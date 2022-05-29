
booklet: final-test.ps
	psnup -2  -pa5 -Pa4 final-test.ps booklet.ps

final-test.ps: final-test.dvi
	dvips final-test.dvi
final-test.dvi: final-test.tex task.tex
	latex final-test.tex

clean:
	rm -rf final-test.dvi final-test.ps final-test.out final-test.log final-test.aux
