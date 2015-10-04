all:    clean lex.cc parse.cc main.cc Scanner.h Scannerbase.h Scanner.ih Parser.h Parserbase.h Parser.ih node.cc
	./sedscript
	g++   --std=c++11 -g lex.cc parse.cc main.cc node.cc;
	# ./a.out < testprogram.c > junk;


lex.cc: lex.l Scanner.ih
	flexc++ lex.l;

parse.cc: parse.y Parser.ih Parser.h Parserbase.h
	bisonc++  parse.y;

clean:
	rm -f Scanner* a.out lex.cc parse.cc junk graph* Parser.ih Parserbase.h



Parser.ih: parse.y
Parser.h:  parse.y
Parserbase.h: parse.y
Scanner.ih: lex.l
Scanner.h: lex.l
Scannerbase.h: lex.l
