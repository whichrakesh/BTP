// Generated by Bisonc++ V4.05.00 on Wed, 28 Jan 2015 16:41:50 +0530

#ifndef Parser_h_included
#define Parser_h_included

// $insert baseclass
#include "Parserbase.h"
// $insert scanner.h
#include "Scanner.h"
#include <iostream>
#include <fstream>
#include <list>
#include "node.h"
using namespace std;
#undef Parser

class Parser: public ParserBase
{
    // $insert scannerobject
    int count = 0;
    Scanner d_scanner;
    ofstream fout;
    public:
        int parse();
    private:
        void error(char const *msg);    // called on (syntax) errors
        int lex();                      // returns the next token from the
                                        // lexical scanner.
        void print();                   // use, e.g., d_token, d_loc

    // support functions for parse():
        void executeAction(int ruleNr);
        void errorRecovery();
        int lookup(bool recovery);
        void nextToken();
        void print__();
        void exceptionHandler__(std::exception const &exc);

};


#endif
