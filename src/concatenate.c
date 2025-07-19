#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

void Concatenate_arrays(uint8_t *input1_ptr, uint8_t *input2_ptr, uint16_t *output_ptr, int size)
{
	for (int i=0; i<size; i++)
	{
		*output_ptr = ((uint16_t)*input1_ptr<<8) | *input2_ptr;
		output_ptr++; input1_ptr++; input2_ptr++;
	}
}

int main(void)
{
	uint8_t input1[5] = {0x12, 0x13, 0x14, 0x15, 0x16};
	uint8_t input2[5] = {0x17, 0x18, 0x19, 0x20, 0xBB};
	
	int size = (sizeof(input1)/sizeof(input1[0]));
	uint16_t output[size];
	for (int i=0; i<size; i++)
	{
		output[i] = 0x0000;
	}

	Concatenate_arrays(input1, input2, output, size);
	
	for (int i=0; i<size; i++)
	{
		printf("Value of output[%d] is 0x%04x \n", i, output[i]);
	}
	return 0;
}
