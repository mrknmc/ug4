#!/bin/tcsh -f

set dir = $1

if ("$dir" == "") then
    echo "USAGE: $0 tts1"
    exit
endif

if (! -e $dir) then
    echo "ERROR: $dir does not exist"
    exit
endif

set sz = `du -sm $dir | gawk '{print $1}'`

if ($sz > 10) then
    echo "ERROR: $dir exceeds 10Mb limit"
endif

foreach file ($dir/{overlap,tfidf,best,test}.top)
  if (! -f $file) then
    echo "ERROR: $file is missing"
  else
    set n = `gawk 'NF != 6 || $2 || $4 || $6 || $1<1 || $1>32 || $3<1 || $3>3204' $file | wc -l`
    if ($n > 0) then
	echo "ERROR: $file has incorrectly formatted lines:"
	gawk 'NF != 6 || $2 || $4 || $6 || $1<1 || $1>32 || $3<1 || $3>3204' $file | head -5
    endif
    set n = `gawk '{print $1}' $file | sort | uniq | wc -l`
    if ($n != 32) then
	echo "ERROR: $file contains output for $n queries instead of 32"
    endif
    set n = `gawk '{print $1,$3}' $file | sort | uniq -c | gawk '$1 > 1' | wc -l`
    if ($n > 0) then
	echo "ERROR: $file contains duplicate scores:"
	gawk '{print "query:", $1,"document:",$3}' $file | sort | uniq -c | gawk '$1 > 1' | head -5
    endif
  endif
end

foreach file ($dir/{overlap,tfidf,best}.py $dir/best.id $dir/report.pdf)
    if (! -f $file) then
	echo "ERROR: $file is missing"
    endif
end

echo "Done."
