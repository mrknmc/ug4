# Produce PDFs from all Markdown files in a directory
# Lincoln Mullen | http://lincolnmullen.com | lincoln@lincolnmullen.com

# List files to be made by finding all *.md files and appending .pdf

TASKS := $(wildcard task*)

# The all rule makes all the PDF files listed
all : clean
				$(foreach task,$(TASKS),./$(task)/run.sh);

clean :
				hadoop dfs -rmr /user/s1140740/*

