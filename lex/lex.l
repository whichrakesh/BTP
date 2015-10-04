
// There may be some flexer directives here

D			[0-9]
L			[a-zA-Z_]
H			[a-fA-F0-9]
E			[Ee][+-]?{D}+
FS			(f|F|l|L)
IS			(u|U|l|L)*

%%
\/\*[^*]*(\*([^/*][^*]*)?)*\*\/				{std::cout << "comment:" << std::string(matched());}
\/\/.+ 			{  std::cout << "comment:" << std::string(matched());}
"auto"			{  return Parser::AUTO; }
"break"			{  return Parser::BREAK; }
"case"			{  return Parser::CASE; }
"char"			{  return Parser::CHAR; }
"const"			{  return Parser::CONST; }
"continue"		{  return Parser::CONTINUE; }
"default"		{  return Parser::DEFAULT; }
"do"			{  return Parser::DO; }
"double"		{  return Parser::DOUBLE; }
"else"			{  return Parser::ELSE; }
"enum"			{  return Parser::ENUM; }
"extern"		{  return Parser::EXTERN; }
"float"			{  return Parser::FLOAT; }
"for"			{  return Parser::FOR; }
"goto"			{  return Parser::GOTO; }
"if"			{  return Parser::IF; }
"int"			{  return Parser::INT; }
"long"			{  return Parser::LONG; }
"register"		{  return Parser::REGISTER; }
"return"		{  return Parser::RETURN; }
"short"			{  return Parser::SHORT; }
"signed"		{  return Parser::SIGNED; }
"sizeof"		{  return Parser::SIZEOF; }
"static"		{  return Parser::STATIC; }
"struct"		{  return Parser::STRUCT; }
"switch"		{  return Parser::SWITCH; }
"typedef"		{  return Parser::TYPEDEF; }
"union"			{  return Parser::UNION; }
"unsigned"		{  return Parser::UNSIGNED; }
"void"			{  return Parser::VOID; }
"volatile"		{  return Parser::VOLATILE; }
"while"			{  return Parser::WHILE; }

{L}({L}|{D})*		{  Parser::d_val__ = std::string(matched()); return Parser::IDENTIFIER;}

0[xX]{H}+{IS}?		{  Parser::d_val__ = (float) atoi(matched().c_str()); return Parser::CONSTANT; }
0{D}+{IS}?		{  Parser::d_val__ = (float) atoi(matched().c_str()); return Parser::CONSTANT; }
{D}+{IS}?		{  Parser::d_val__ = (float) atoi(matched().c_str()); return Parser::CONSTANT; }
L?'(\\.|[^\\'])+'	{  Parser::d_val__ = (float)atof(matched().c_str()); return Parser::CONSTANT; }

{D}+{E}{FS}?		{  Parser::d_val__ = (float)atof(matched().c_str()); return Parser::CONSTANT; }
{D}*"."{D}+({E})?{FS}?	{  Parser::d_val__ = (float)atof(matched().c_str()); return Parser::CONSTANT; }
{D}+"."{D}*({E})?{FS}?	{  Parser::d_val__ = (float)atof(matched().c_str()); return Parser::CONSTANT; }

L?\"(\\.|[^\\"])*\"	{  Parser::d_val__ = std::string(matched()); }

"..."			{  Parser::d_val__ = std::string(matched()); return Parser::ELLIPSIS;}
">>="			{ Parser::d_val__ = std::string(matched());  return Parser::RIGHT_ASSIGN; }
"<<="			{ Parser::d_val__ = std::string(matched());  return Parser::LEFT_ASSIGN; }
"+="			{ Parser::d_val__ = std::string(matched());  return Parser::ADD_ASSIGN; }
"-="			{ Parser::d_val__ = std::string(matched());  return Parser::SUB_ASSIGN; }
"*="			{ Parser::d_val__ = std::string(matched());  return Parser::MUL_ASSIGN; }
"/="			{ Parser::d_val__ = std::string(matched());  return Parser::DIV_ASSIGN; }
"%="			{ Parser::d_val__ = std::string(matched());  return Parser::MOD_ASSIGN; }
"&="			{ Parser::d_val__ = std::string(matched());  return Parser::AND_ASSIGN; }
"^="			{ Parser::d_val__ = std::string(matched());  return Parser::XOR_ASSIGN; }
"|="			{ Parser::d_val__ = std::string(matched());  return Parser::OR_ASSIGN; }
">>"			{ Parser::d_val__ = std::string(matched());  return Parser::RIGHT_OP; }
"<<"			{ Parser::d_val__ = std::string(matched());  return Parser::LEFT_OP; }
"++"			{ Parser::d_val__ = std::string(matched());  return Parser::INC_OP; }
"--"			{ Parser::d_val__ = std::string(matched());  return Parser::DEC_OP; }
"->"			{ Parser::d_val__ = std::string(matched());  return Parser::PTR_OP; }
"&&"			{ Parser::d_val__ = std::string(matched());  return Parser::AND_OP; }
"||"			{ Parser::d_val__ = std::string(matched());  return Parser::OR_OP; }
"<="			{ Parser::d_val__ = std::string(matched());  return Parser::LE_OP; }
">="			{ Parser::d_val__ = std::string(matched());  return Parser::GE_OP; }
"=="			{ Parser::d_val__ = std::string(matched());  return Parser::EQ_OP; }
"!="			{ Parser::d_val__ = std::string(matched());  return Parser::NE_OP; }
";"			{ Parser::d_val__ = std::string(matched());  return ';'; }
("{"|"<%")		{ Parser::d_val__ = std::string(matched());  return '{'; }
("}"|"%>")		{ Parser::d_val__ = std::string(matched());  return '}'; }
","			{ Parser::d_val__ = std::string(matched());  return ','; }
":"			{ Parser::d_val__ = std::string(matched());  return ':'; }
"="			{ Parser::d_val__ = std::string(matched());  return '='; }
"("			{ Parser::d_val__ = std::string(matched());  return '('; }
")"			{ Parser::d_val__ = std::string(matched());  return ')'; }
("["|"<:")		{ Parser::d_val__ = std::string(matched());  return '['; }
("]"|":>")		{ Parser::d_val__ = std::string(matched());  return ']'; }
"."			{ Parser::d_val__ = std::string(matched());  return '.'; }
"&"			{ Parser::d_val__ = std::string(matched());  return '&'; }
"!"			{ Parser::d_val__ = std::string(matched());  return '!'; }
"~"			{ Parser::d_val__ = std::string(matched());  return '~'; }
"-"			{ Parser::d_val__ = std::string(matched());  return '-'; }
"+"			{ Parser::d_val__ = std::string(matched());  return '+'; }
"*"			{ Parser::d_val__ = std::string(matched());  return '*'; }
"/"			{ Parser::d_val__ = std::string(matched());  return '/'; }
"%"			{ Parser::d_val__ = std::string(matched());  return '%'; }
"<"			{ Parser::d_val__ = std::string(matched());  return '<'; }
">"			{ Parser::d_val__ = std::string(matched());  return '>'; }
"^"			{ Parser::d_val__ = std::string(matched());  return '^'; }
"|"			{ Parser::d_val__ = std::string(matched());  return '|'; }
"?"			{ Parser::d_val__ = std::string(matched());  return '?'; }

[ \t\v\n\f]		{  }
'^'+			{ std::cout << "endfor";}
.			{ /* ignore bad characters */ }
%%

