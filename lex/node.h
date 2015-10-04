#ifndef Node_h_included
#define Node_h_included

#include <fstream>
#include <string>
#include <list>
#include <map>
using namespace std;


/****************************************************************************************/
//#undef AbstractASTNode
class AbstractASTNode
{
    public:
        virtual void print () = 0;
};


class StmtAst: public AbstractASTNode{

};

class ExpAst: public AbstractASTNode{
    public:
};

class EmptyStmtAst: public StmtAst{
    public:
        void print();
};

class ExpStmtAst: public StmtAst{
    protected:
        ExpAst* exp;
    public:
        ExpStmtAst(ExpAst* exp);
        void print();
};

class BlockStmtAst: public StmtAst{
    protected:
        list<StmtAst*> statement_list;

    public:
        BlockStmtAst(list<StmtAst*>* statement_list);
        void print();
};

class JumpStmtAst: public StmtAst{
    protected:
        string stmt_type;
    public:
        JumpStmtAst(string stmt_type);
        void print();    
};

class ReturnStmtAst: public StmtAst{
    protected:
        ExpAst *exp;

    public:
        ReturnStmtAst(ExpAst *exp);
        void print();
};

class IfStmtAst: public StmtAst{
    protected:
        ExpAst *exp;
        StmtAst *stmt1,*stmt2;

    public:
        IfStmtAst( ExpAst *exp, StmtAst *stmt1,StmtAst *stmt2);
        void print();
};

class SwitchStmtAst: public StmtAst{
    protected:
        ExpAst *exp;
        StmtAst *stmt;

    public:
        SwitchStmtAst( ExpAst *exp, StmtAst *stmt);
        void print();
};

class WhileStmtAst: public StmtAst{
    protected:
        ExpAst *exp;
        StmtAst *stmt;

    public:
        WhileStmtAst(ExpAst *exp,StmtAst *stmt);
        void print();
};

class ForStmtAst: public StmtAst{
    protected:
        StmtAst *stmt1, *stmt2;
        ExpAst *exp3;
        StmtAst *body_stmt;

    public:
        ForStmtAst(StmtAst *stmt1, StmtAst *stmt2, ExpAst *exp3, StmtAst *body_stmt);
        void print();
};


class BinaryOpAst: public ExpAst{
    protected:
        string b_op;
        ExpAst *exp1,*exp2;

    public:
        BinaryOpAst (string b_op, ExpAst* exp1, ExpAst* exp2);
        void print();
};

class UnaryOpAst: public ExpAst{
    protected:
        string u_op;
        ExpAst *exp;

    public:
        UnaryOpAst(string u_op, ExpAst *exp);
        void print();
};

class FunCallExpAst: public ExpAst{
    protected:
        ExpAst *function;
        list<ExpAst*> expression_list;
    public:
        FunCallExpAst(ExpAst* function, list<ExpAst*>* expression_list);
        FunCallExpAst(ExpAst* function);
        void print();
};

class ConditionalExpAst : public ExpAst{
    protected:
        ExpAst *exp1, *exp2, *exp3;
    public: 
        ConditionalExpAst(ExpAst *exp1, ExpAst *exp2, ExpAst *exp3 );
        void print();  
};

class DataMemberAst: public ExpAst{
    protected:
        ExpAst *instance;
        string member_name;
    public:
        DataMemberAst(ExpAst* instance, string member_name);
        void print();
};

class PointerDataMemberAst: public ExpAst{
    protected:
        ExpAst* instance_pointer;
        string member_name;
    public:
        PointerDataMemberAst(ExpAst* exp, string member_name);
        void print();
};

class Const: public ExpAst{
    protected:
        float value;
    public:
        Const(float value);
        void print();
};


class StringConst: public ExpAst{
    protected:
        string value;
    public:
        StringConst(string value);
        void print();
};

class Identifier: public ExpAst{
    protected:
        string value;
    public:
        Identifier(string value);
        void print();
};


class ArrayIndexAst: public ExpAst{
    protected:
        ExpAst *array_ref;
        ExpAst *index_exp;
    public:
        ArrayIndexAst(ExpAst *array_ref, ExpAst *exp);
        void print();
};

#endif

