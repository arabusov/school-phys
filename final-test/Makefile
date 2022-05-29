
booklet: joined.ps
	psnup -2 -Pa5 -pa4 -s1 joined.ps booklet.ps
joined.ps: final-test.ps
	psjoin final-test.ps final-test.ps > joined.ps

final-test.ps: final-test.dvi
	dvips final-test.dvi
final-test.dvi: final-test.tex task.tex
	latex final-test.tex

clean:
	rm -rf final-test.dvi final-test.ps final-test.out final-test.log final-test.aux joined.ps
