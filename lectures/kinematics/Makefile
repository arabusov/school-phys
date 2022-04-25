kinematics.ps: kinematics.dvi
	dvips kinematics.dvi
kinematics.dvi: kinematics.tex
	latex kinematics.tex
	latex kinematics.tex
book: kinematics.ps
	psbook -q kinematics.ps kinematics-book.ps
	psnup -q -pa4 -Pa5 -d -2 kinematics-book.ps kinematics-sig.ps
	rm kinematics-book.ps
clean:
	rm -f kinematics.aux
	rm -f kinematics.log
	rm -f kinematics.dvi
	rm -f kinematics-book.ps
	rm -f kinematics-sig.ps
