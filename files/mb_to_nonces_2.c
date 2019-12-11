#include <stdio.h>
float conversionMB(float mb);
float conversionN(float n);

int main()
{
	printf("[M]B to Nonce\n[N]once to MB\n");
	char response;
	scanf("%c", &response);
	printf("entered: %c\n", response);
	if (response == 'M')
	{
		printf("Enter MB: \n");
		float mb;
		scanf("%f", &mb);
		float n;
		n = conversionMB(mb);
		printf("Nonces: %f\n", n);
	}
	else if (response == 'N')
	{
		printf("Enter N: \n");
		float n;
		scanf("%f", &n);
		float mb;
		mb = conversionN(n);
		printf("MB: %f\n", mb);
	}
	
	printf("program end\n");
	return 0;
}

float conversionMB(float mb)
{
	// 1000 MB = 3814 Nonces
	float n;
	n = mb * 3.814;
	return n;
}

float conversionN(float n)
{
	float mb;
	mb = n / 3.814;
	return mb;
}