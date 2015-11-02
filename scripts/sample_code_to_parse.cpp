for(int i=0; i<5; i++)
{
	//detecting array references in the same line
	A[i] = B[i] + A[i+1]*2;  		

	//detecting array references in conditionals
	if(A[i] == B[i-1])
	{
		//detecting array references in function calls
		s = sum(A[i],B[i-1]);
		//detecting array references inside array references
		A[B[i]] = 1;
		//detecting array refs in arithmatico assignment operations
		A[i] += 5;	
		++A[i];			
	}
	while(A[i] >= B[i])
	{
		A[i]--;
		//detecting array references as pointers and data objects
		C[i]->x = D[i].y;
		D[i].x = A[i];
		//detecting array references during dereferencing
		a = *C[i];
		*C[i] = b;
	}
	for(int j=0; j<i; j+=1, i--)
	{
		//detecting array references in nested array references
		E[2*i][j*2] = A[2*i] + B[i];
	}
	//TODO: detecting multiline statements as same statement
	B[i] = C[i]
			+ D[i];
}
