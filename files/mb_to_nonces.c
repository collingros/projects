#include <stdio.h>
void conversionMB(float *mb, float *n);
void conversionN(float *mb, float *n);

int main()
{
	float mb;
	float n;
	
	printf("[M]B to Nonce\n[N]once to MB\n");
	char response;
	scanf("%c", &response);

	if (response == 'M')
	{
		printf("Enter MB: \n");
		scanf("%f", &mb);
		printf("mb: %f\n&mb: %f\n", mb, &mb);
		conversionMB(&mb, &n);
		printf("Nonces: %f\n", n);
	}
	else if (response == 'N')
	{
		printf("Enter N: \n");
		scanf("%f", &n);
		printf("n: %f\n&n: %f\n", n, &n);
		conversionN(&mb, &n);
		printf("MB: %f\n", mb);
	}
	
	printf("program end\n");
	return 0;
}

void conversionMB(float *mb, float *n)
{
	// 1000 MB = 3814 Nonces
	*n = *mb * 3.814;
	return;
}

void conversionN(float *mb, float *n)
{
	*mb = *n / 3.814;
	return;
}