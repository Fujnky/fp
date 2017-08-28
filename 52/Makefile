ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build/main.pdf

# hier Python-Skripte:
build/alpha.pdf: auswertung/alpha.py | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/alpha.py

build/rlcg.pdf build/rlcg.tex: auswertung/rlcg.py | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/rlcg.py

build/langes_kabel_kurzgeschlossen.pdf: auswertung/laufzeit.py | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/laufzeit.py

build/bauteil3.5.pdf: auswertung/bauteile.py | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/bauteile.py

build/mehrfach1.pdf: auswertung/mehrfach.py | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/mehrfach.py

build/impuls.pdf: auswertung/impuls.py | build
	TEXINPUTS="$(pwd):$(pwd)/../latex-template/:" PYTHONPATH="../" python auswertung/impuls.py

# hier weitere Abhängigkeiten für build/main.pdf deklarieren:
build/main.pdf: build/alpha.pdf build/rlcg.tex build/rlcg.pdf build/langes_kabel_kurzgeschlossen.pdf build/bauteil3.5.pdf build/mehrfach1.pdf build/impuls.pdf

build/main.pdf: FORCE | build
	  TEXINPUTS="$(call translate,build:)" \
	  BIBINPUTS=build: \
	  max_print_line=1048576 \
	latexmk \
	  --lualatex \
	  --output-directory=build \
	  --interaction=nonstopmode \
	  --halt-on-error \
	main.tex

build:
	mkdir -p build

clean:
	rm -rf build

FORCE:

.PHONY: all clean
