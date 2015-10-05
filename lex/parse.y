%debug
%scanner Scanner.h
%scanner-token-function d_scanner.lex()

%polymorphic num: int; fl: float; str: string; stmt: StmtAst*; stmts: list<StmtAst*>*; exp: ExpAst*; exps: list<ExpAst*>*;

%token SIZEOF
%token <str> IDENTIFIER STRING_LITERAL
%token <fl> CONSTANT
%token <str> PTR_OP INC_OP DEC_OP LEFT_OP RIGHT_OP LE_OP GE_OP EQ_OP NE_OP
%token <str> AND_OP OR_OP MUL_ASSIGN DIV_ASSIGN MOD_ASSIGN ADD_ASSIGN
%token <str> SUB_ASSIGN LEFT_ASSIGN RIGHT_ASSIGN AND_ASSIGN
%token <str> XOR_ASSIGN OR_ASSIGN TYPE_NAME

%token TYPEDEF EXTERN STATIC AUTO REGISTER
%token CHAR SHORT INT LONG SIGNED UNSIGNED FLOAT DOUBLE CONST VOLATILE VOID
%token STRUCT UNION ENUM ELLIPSIS

%token CASE DEFAULT IF ELSE SWITCH WHILE DO FOR GOTO CONTINUE BREAK RETURN


%type <exp> primary_expression postfix_expression unary_expression cast_expression multiplicative_expression additive_expression
%type <exp> shift_expression relational_expression equality_expression and_expression exclusive_or_expression inclusive_or_expression
%type <exp> logical_and_expression logical_or_expression conditional_expression assignment_expression expression constant_expression
%type <exps> argument_expression_list
%type <str> unary_operator assignment_operator multiline_string
%type <stmt> statement labeled_statement compound_statement  expression_statement
%type <stmt> selection_statement iteration_statement jump_statement
%type <stmts> statement_list

%start statement_list
%%

primary_expression
	: IDENTIFIER
	{		
		$$ = new Identifier($1);
	}
	| CONSTANT
	{
		$$ = new Const($1);
	}
	| multiline_string
	{
		$$ = new StringConst($1);
	}
	| '(' expression ')'
	{
		$$ = $2;
	}
	;

multiline_string
	: STRING_LITERAL
	{
		$$ = $1;
	}
	| multiline_string STRING_LITERAL
	{
		$$ = $1 + $2;
	}
	;

postfix_expression
	: primary_expression
	| postfix_expression '[' expression ']'
	{
		$$ = new ArrayIndexAst($1,$3);
	}
	| postfix_expression '(' ')'
	{
		$$ = new FunCallExpAst($1);
	}
	| postfix_expression '(' argument_expression_list ')'
	{
		$$ = new FunCallExpAst($1,$3);	
	}
	| postfix_expression '.' IDENTIFIER
	{
		$$ = new DataMemberAst($1,$3);
	}
	| postfix_expression PTR_OP IDENTIFIER
	{
		$$ = new PointerDataMemberAst($1,$3);
	}
	| postfix_expression INC_OP
	{
		$$ = new UnaryOpAst($2,$1);
	}
	| postfix_expression DEC_OP
	{
		$$ = new UnaryOpAst($2,$1);
	}
	;

argument_expression_list
	: assignment_expression
	{
		$$ = new list<ExpAst*>();
		($$)->push_back($1);
	}
	| argument_expression_list ',' assignment_expression
	{
		($1)->push_back($3);
		$$ = $1;
	}
	;

unary_expression
	: postfix_expression
	| INC_OP unary_expression
	{
		$$ = new UnaryOpAst($1,$2);
	}
	| DEC_OP unary_expression
	{
		$$ = new UnaryOpAst($1,$2);
	}
	| unary_operator cast_expression
	{
		$$ = new UnaryOpAst($1,$2);
	}
	| SIZEOF unary_expression
	{
		$$ = new UnaryOpAst("sizeof",$2);
	}
	| SIZEOF '(' type_name ')'
	{
		$$ = new Const(4);
	}
	;

unary_operator
	: '&'
	| '*'
	| '+'
	| '-'
	| '~'
	| '!'
	;

cast_expression
	: unary_expression
	| '(' type_name ')' cast_expression
	{
		$$ = $4;
	}
	;

multiplicative_expression
	: cast_expression
	| multiplicative_expression '*' cast_expression
	{
		$$ = new BinaryOpAst("*",$1,$3);
	}
	| multiplicative_expression '/' cast_expression
	{
		$$ = new BinaryOpAst("/",$1,$3);
	}
	| multiplicative_expression '%' cast_expression
	{
		$$ = new BinaryOpAst("%",$1,$3);
	}
	;

additive_expression
	: multiplicative_expression
	| additive_expression '+' multiplicative_expression
	{
		$$ = new BinaryOpAst("+",$1,$3);
	}
	| additive_expression '-' multiplicative_expression
	{
		$$ = new BinaryOpAst("-",$1,$3);
	}
	;

shift_expression
	: additive_expression
	| shift_expression LEFT_OP additive_expression
	{
		$$ = new BinaryOpAst("<<",$1,$3);
	}
	| shift_expression RIGHT_OP additive_expression
	{
		$$ = new BinaryOpAst(">>",$1,$3);
	}
	;

relational_expression
	: shift_expression
	| relational_expression '<' shift_expression
	{
		$$ = new BinaryOpAst("<",$1,$3);
	}
	| relational_expression '>' shift_expression
	{
		$$ = new BinaryOpAst(">",$1,$3);
	}
	| relational_expression LE_OP shift_expression
	{
		$$ = new BinaryOpAst("<=",$1,$3);
	}
	| relational_expression GE_OP shift_expression
	{
		$$ = new BinaryOpAst(">=",$1,$3);
	}
	;

equality_expression
	: relational_expression
	| equality_expression EQ_OP relational_expression
	{
		$$ = new BinaryOpAst("==",$1,$3);
	}
	| equality_expression NE_OP relational_expression
	{
		$$ = new BinaryOpAst("!=",$1,$3);
	}
	;

and_expression
	: equality_expression
	| and_expression '&' equality_expression
	{
		$$ = new BinaryOpAst("&",$1,$3);
	}
	;

exclusive_or_expression
	: and_expression
	| exclusive_or_expression '^' and_expression
	{
		$$ = new BinaryOpAst("^",$1,$3);
	}
	;

inclusive_or_expression
	: exclusive_or_expression
	| inclusive_or_expression '|' exclusive_or_expression
	{
		$$ = new BinaryOpAst("|",$1,$3);
	}
	;

logical_and_expression
	: inclusive_or_expression
	| logical_and_expression AND_OP inclusive_or_expression
	{
		$$ = new BinaryOpAst("&&",$1,$3);
	}
	;

logical_or_expression
	: logical_and_expression
	| logical_or_expression OR_OP logical_and_expression
	{
		$$ = new BinaryOpAst("||",$1,$3);
	}
	;

conditional_expression
	: logical_or_expression
	| logical_or_expression '?' expression ':' conditional_expression
	{
		$$ = new ConditionalExpAst($1, $3, $5);
	}
	;

assignment_expression
	: conditional_expression
	| unary_expression assignment_operator assignment_expression
	{
		$$ = new BinaryOpAst($2,$1,$3);
	}
	;

assignment_operator
	: '='
	{
		$$ = "=";
	}
	| MUL_ASSIGN
	| DIV_ASSIGN
	| MOD_ASSIGN
	| ADD_ASSIGN
	| SUB_ASSIGN
	| LEFT_ASSIGN
	| RIGHT_ASSIGN
	| AND_ASSIGN
	| XOR_ASSIGN
	| OR_ASSIGN
	;

expression
	: assignment_expression
	| expression ',' assignment_expression
	{
		$$ = new BinaryOpAst(",",$1,$3);
	}
	;

constant_expression
	: conditional_expression
	;

//------------------------------------------------------------------------------------------------------------------

/*declaration
	: declaration_specifiers ';'
	| declaration_specifiers init_declarator_list ';'
	;*/

declaration
	: type_specifier ';'
	| type_specifier init_declarator_list ';'
	;
declaration_specifiers
	: storage_class_specifier
	| storage_class_specifier declaration_specifiers
	| type_specifier
	| type_specifier declaration_specifiers
	| type_qualifier
	| type_qualifier declaration_specifiers
	;

init_declarator_list
	: init_declarator
	| init_declarator_list ',' init_declarator
	;

init_declarator
	: declarator
	| declarator '=' initializer
	;

storage_class_specifier
	: TYPEDEF
	| EXTERN
	| STATIC
	| AUTO
	| REGISTER
	;

type_specifier
	: VOID
	| CHAR
	| SHORT
	| INT
	| LONG
	| FLOAT
	| DOUBLE
	| SIGNED
	| UNSIGNED
	| struct_or_union_specifier
	| enum_specifier
	| IDENTIFIER
	;

struct_or_union_specifier
	: struct_or_union IDENTIFIER '{' struct_declaration_list '}'
	| struct_or_union '{' struct_declaration_list '}'
	| struct_or_union IDENTIFIER
	;

struct_or_union
	: STRUCT
	| UNION
	;

struct_declaration_list
	: struct_declaration
	| struct_declaration_list struct_declaration
	;

struct_declaration
	: specifier_qualifier_list struct_declarator_list ';'
	;

specifier_qualifier_list
	: type_specifier specifier_qualifier_list
	| type_specifier
	| type_qualifier specifier_qualifier_list
	| type_qualifier
	;

struct_declarator_list
	: struct_declarator
	| struct_declarator_list ',' struct_declarator
	;

struct_declarator
	: declarator
	| ':' constant_expression
	| declarator ':' constant_expression
	;

enum_specifier
	: ENUM '{' enumerator_list '}'
	| ENUM IDENTIFIER '{' enumerator_list '}'
	| ENUM IDENTIFIER
	;

enumerator_list
	: enumerator
	| enumerator_list ',' enumerator
	;

enumerator
	: IDENTIFIER
	| IDENTIFIER '=' constant_expression
	;

type_qualifier
	: CONST
	| VOLATILE
	;

declarator
	: pointer direct_declarator
	| direct_declarator
	;

direct_declarator
	: IDENTIFIER
	| '(' declarator ')'
	| direct_declarator '[' constant_expression ']'
	| direct_declarator '[' ']'
	| direct_declarator '(' parameter_type_list ')'
	| direct_declarator '(' identifier_list ')'
	| direct_declarator '(' ')'
	;

pointer
	: '*'
	| '*' type_qualifier_list
	| '*' pointer
	| '*' type_qualifier_list pointer
	;

type_qualifier_list
	: type_qualifier
	| type_qualifier_list type_qualifier
	;


parameter_type_list
	: parameter_list
	| parameter_list ',' ELLIPSIS
	;

parameter_list
	: parameter_declaration
	| parameter_list ',' parameter_declaration
	;

parameter_declaration
	: declaration_specifiers declarator
	| declaration_specifiers abstract_declarator
	| declaration_specifiers
	;

identifier_list
	: IDENTIFIER
	| identifier_list ',' IDENTIFIER
	;

type_name
	: specifier_qualifier_list
	| specifier_qualifier_list abstract_declarator
	;

abstract_declarator
	: pointer
	| direct_abstract_declarator
	| pointer direct_abstract_declarator
	;

direct_abstract_declarator
	: '(' abstract_declarator ')'
	| '[' ']'
	| '[' constant_expression ']'
	| direct_abstract_declarator '[' ']'
	| direct_abstract_declarator '[' constant_expression ']'
	| '(' ')'
	| '(' parameter_type_list ')'
	| direct_abstract_declarator '(' ')'
	| direct_abstract_declarator '(' parameter_type_list ')'
	;

initializer
	: assignment_expression
	| '{' initializer_list '}'
	| '{' initializer_list ',' '}'
	;

initializer_list
	: initializer
	| initializer_list ',' initializer
	;

//--------------------------------------------------------------------------------------------

statement
	: labeled_statement
	| compound_statement
	| expression_statement
	| selection_statement
	| iteration_statement
	| jump_statement
	;

labeled_statement
	: IDENTIFIER ':' statement
	{
		$$ = $3;
	}
	| CASE constant_expression ':' statement
	{
		$$ = $4;
	}
	| DEFAULT ':' statement
	{
		$$ = $3;
	}
	;

compound_statement
	: '{' '}'
	{
		$$ = new BlockStmtAst(new list<StmtAst*>());
	}
	| '{' statement_list '}'
	{
		$$ = new BlockStmtAst($2);
	}
	| '{' declaration_list '}'
	{
		$$ = new BlockStmtAst(new list<StmtAst*>());
	}
	| '{' declaration_list statement_list '}'
	{
		$$ = new BlockStmtAst($3);
	}
	;

declaration_list
	: declaration
	| declaration_list declaration
	;

statement_list
	: statement
	{  		
  		$$ = new list<StmtAst*>();  		
  		($$)->push_back($1);
  	}
	| statement_list statement
	{
		($1)->push_back($2);
  		$$ = $1;
	}
	;

expression_statement
	: ';'
	{
		$$ = new EmptyStmtAst();
	}
	| expression ';'
	{
		$$ = new ExpStmtAst($1); 
	}
	;

selection_statement
	: IF '(' expression ')' statement
	{
		$$ = new IfStmtAst($3,$5, NULL);
	}
	| IF '(' expression ')' statement ELSE statement
	{
		$$ = new IfStmtAst($3,$5,$7);
	}
	| SWITCH '(' expression ')' statement
	{
		$$ = new SwitchStmtAst($3, $5); 
	}
	;

iteration_statement
	: WHILE '(' expression ')' statement
	{
		$$ = new WhileStmtAst($3,$5);
	}
	| DO statement WHILE '(' expression ')' ';'
	{
		$$ = new WhileStmtAst($5,$2);
	}
	| FOR '(' expression_statement expression_statement ')' statement
	{
		$$ = new ForStmtAst($3,$4,NULL, $6);
	}
	| FOR '(' expression_statement expression_statement expression ')' statement
	{
		$$ = new ForStmtAst($3,$4,$5,$7);
	}
	;

jump_statement
	: GOTO IDENTIFIER ';'
	{
		$$ = new JumpStmtAst("goto");
	}
	| CONTINUE ';'
	{
		$$ = new JumpStmtAst("continue");
	}
	| BREAK ';'
	{
		$$ = new JumpStmtAst("break");
	}
	| RETURN ';'
	{
		$$ = new JumpStmtAst("return");
	}
	| RETURN expression ';'
	{
		$$ = new ReturnStmtAst($2);	
	}
	;

translation_unit
	: external_declaration
	| translation_unit external_declaration
	;

external_declaration
	: function_definition
	| declaration
	;

function_definition
	: declaration_specifiers declarator declaration_list compound_statement
	| declaration_specifiers declarator compound_statement
	| declarator declaration_list compound_statement
	| declarator compound_statement
	;