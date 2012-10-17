
SIZES=003 010 020 030 060 100
SOLNS=$(patsubst %,soln_maze_%.txt,$(SIZES))

all: $(SOLNS)

wtd: $(WTD)

soln_maze_%.txt: wtd_maze_%.txt ../find_distance
	../find_distance < wtd_maze_$*.txt > soln_maze_$*.txt

clean:
	rm -f *~ soln_*
