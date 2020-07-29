# makeenv optional file for additional setting
# LATEXARGS additional flags to latex to be set in makeenv
# LATEXMK latex compilation defaulting to latexmk, can be changed in makeenv
# POST_CMD additional action after latexmk
# Example: insert LATEXARGS=-file-line-error into makeenv
# Example: insert POST_CMD=&& /bin/cp -fv $(TRGT).pdf ~/win/Documents/

-include makeenv
TRGT=Robust\ CLSP-AAAI

LATEXMK?=latexmk

all:
	$(LATEXMK) -pdf $(LATEXARGS) $(TRGT) $(POST_CMD)

clean:
	@latexmk -c $(TRGT)

allclean: clean
	$(LATEXMK) -C "$(TRGT)"
