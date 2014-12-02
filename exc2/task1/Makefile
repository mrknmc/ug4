# Produce PDFs from all Markdown files in a directory
# Lincoln Mullen | http://lincolnmullen.com | lincoln@lincolnmullen.com

# List files to be made by finding all *.md files and appending .pdf

TASKS := $(wildcard task*)

# The all rule makes all the PDF files listed
all : $(TASKS)

# This generic rule accepts PDF targets with corresponding Markdown
# source, and makes them using pandoc
%.pdf: %.md lists.png results.png
		pandoc --from=markdown --to=latex --template=template.tex --filter=pandoc-citeproc --mathjax --number-sections -o $@ $<

lists.png: lists.gp
		gnuplot lists.gp

results.png: results.gp
		gnuplot results.gp

# Remove all PDF outputs
clean :
		rm $(PDFS)

# Remove all PDF outputs then build them again
rebuild : clean all
