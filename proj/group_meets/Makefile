HTMLS := $(patsubst %.md, %.html, $(wildcard *.md))

# The all rule makes all the HTML files listed
all : $(HTMLS)

# This generic rule accepts PDF targets with corresponding Markdown
# source, and makes them using pandoc
%.html : %.md
		pandoc -s -f markdown -t revealjs -V theme=moon -V center=false -V transition=linear -o $@ $< > /dev/null

# Remove all HTML outputs
clean :
		rm $(HTMLS)

# Remove all HTML outputs then build them again
rebuild : clean all
