#include<iostream>
#include<vector>
#include "node.h"

using namespace std;


void EmptyStmtAst::print(){
    cout<<"(Empty)";
}

ExpStmtAst::ExpStmtAst(ExpAst* exp){
    this->exp = exp;
}

void ExpStmtAst::print(){
    exp->print();
}

BlockStmtAst::BlockStmtAst(list<StmtAst* >* statement_list){
    this->statement_list = *statement_list;
}

void BlockStmtAst::print(){
    cout<<"(Block\n";
    list<StmtAst*>::iterator it;
    for(it = statement_list.begin(); it != statement_list.end(); it++){
        (*it)->print(); 
    }
    cout<<")\n";
}

JumpStmtAst::JumpStmtAst(string stmt_type){
    this->stmt_type = stmt_type;
}

void JumpStmtAst::print(){
    cout<<"(" << stmt_type << ")\n";
}


ReturnStmtAst::ReturnStmtAst(ExpAst* exp){
    this->exp=exp;
}
void ReturnStmtAst::print(){
    cout<<"(return ";
    exp->print();
    cout<<")\n";
}


IfStmtAst::IfStmtAst(ExpAst* exp, StmtAst* stmt1, StmtAst* stmt2){
    this->exp = exp;
    this->stmt1 = stmt1;
    this->stmt2 = stmt2;
}

void IfStmtAst::print(){
    cout<<"( if ";
    exp->print();
    cout << " "; 
    stmt1->print();
    cout << " "; 
    if(stmt2 != NULL)
        stmt2->print();
    cout<<" )\n";
}

SwitchStmtAst::SwitchStmtAst(ExpAst* exp, StmtAst* stmt){
    this->exp = exp;
    this->stmt = stmt;
}

void SwitchStmtAst::print(){
    cout<<"( Switch ";
    exp->print();
    cout << " "; 
    stmt->print();
    cout<<" )\n";
}

WhileStmtAst::WhileStmtAst(ExpAst* exp, StmtAst* stmt){
    this->exp = exp;
    this->stmt = stmt;
}
void WhileStmtAst::print(){
    cout<<"( while ";
    exp->print();
    cout << " "; 
    stmt->print();
    cout<<" )\n";
}


ForStmtAst::ForStmtAst(StmtAst* stmt1, StmtAst* stmt2, ExpAst* exp3, StmtAst* body_stmt){
    this->stmt1 = stmt1;
    this->stmt2 = stmt2;
    this->exp3 = exp3;
    this->body_stmt = body_stmt;
}
void ForStmtAst::print(){
    cout<<"(for ";
    stmt1->print();
    cout << " "; 
    stmt2->print();
    cout << " "; 
    if(exp3 != NULL)
        exp3->print();
    cout << " "; 
    body_stmt->print();
    cout<<" )";
}


BinaryOpAst::BinaryOpAst(string b_op, ExpAst* exp1, ExpAst* exp2){  
    this->b_op = b_op;
    this->exp1 = exp1;
    this->exp2 = exp2;
}

void BinaryOpAst::print(){
    cout<<"( " << b_op << " ";
    exp1->print();
    cout << " ";
    exp2->print();
    cout<<" )";
}


UnaryOpAst::UnaryOpAst(string u_op, ExpAst* exp){
    this->u_op = u_op;
    this->exp = exp;
}
void UnaryOpAst::print(){
    cout<<"( "<< u_op;
    exp->print();
    cout << " )";
}

FunCallExpAst::FunCallExpAst(ExpAst* function, list<ExpAst* >* expression_list){
    this->function = function;
    this->expression_list = *expression_list;
}

FunCallExpAst::FunCallExpAst(ExpAst* function){
    this->function = function;
    this->expression_list = list<ExpAst*>();
}

void FunCallExpAst::print(){
    list<ExpAst*>::iterator it;
    cout << "(FunCallExpAst " ;
    function->print();
    for(it = expression_list.begin(); it != expression_list.end(); it++){
        (*it)->print();
        cout<<" ";
    }
    cout << ")";
}

ConditionalExpAst::ConditionalExpAst(ExpAst *exp1, ExpAst *exp2, ExpAst *exp3){
    this->exp1 = exp1;
    this->exp2 = exp2;
    this->exp3 = exp3;
}

void ConditionalExpAst::print(){
    cout << "(Conditional ";
    exp1->print();
    exp2->print();
    exp3->print();
    cout << " )\n" ;    
}


DataMemberAst::DataMemberAst(ExpAst* instance, string member_name){
    this->instance = instance;
    this->member_name = member_name;
}

void DataMemberAst::print(){
    cout << "(DataMember ";
    instance->print();
    cout << member_name << ")\n" ;    
}

PointerDataMemberAst::PointerDataMemberAst(ExpAst* exp, string member_name){
    this->instance_pointer = exp;
    this->member_name = member_name;
}

void PointerDataMemberAst::print(){
    cout << "(PointerDataMember ";
    instance_pointer->print();
    cout << member_name  << ")\n";    
}

Const::Const(float value){
    this->value = value;
}
void Const::print(){
    cout<<"( FloatConst "<<value<<" )";
}

StringConst::StringConst(string value){
    this->value = value;
}

void StringConst::print(){
    cout<<"( StringLiteral \""<<value<<"\" )";
}

Identifier::Identifier(string value){
    this->value = value;
}
void Identifier::print(){
    cout<<"(Id: "<<value<<" )";
}

ArrayIndexAst::ArrayIndexAst(ExpAst* array_ref, ExpAst* exp){
    this->array_ref = array_ref;
    this->index_exp = exp;
}

void ArrayIndexAst::print(){
    cout << "( ArrayIndex ";
    array_ref->print();
    cout << " ";
    index_exp->print();
    cout<<" )";
}