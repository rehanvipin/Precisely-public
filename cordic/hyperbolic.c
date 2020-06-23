#include<stdio.h>

float rotation(float x, float y, float z)
{
	// calculate hyperbolic values for sine and cosine
	// returns e^z
	float inv2pws[] = {0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125, 0.00390625};
	float tanangs[] = {0.54931, 0.25541, 0.12566, 0.06258, 0.03126, 0.01563, 0.00781, 0.00391};
	float atable[] = {0.86603, 0.83853, 0.83195, 0.83032, 0.82992, 0.82982, 0.82979, 0.82978};
	int len = 8, d;
	float x_, y_, z_;
	float x0 = x, y0 = y;

	for(int i=0; i<len; i++)
	{
		d = (z<0)?-1:1;
		x_ = x + y*d*inv2pws[i];
		y_ = y + x*d*inv2pws[i];
		z_ = z - d*tanangs[i];
		x = x_;
		y = y_;
		z = z_;
	}
	// Normalize x and y
	x = (x/atable[len-1]);
	y = (y/atable[len-1]);

	printf("xn: %f, yn: %f, zn: %f\n", x, y, z);
	
	return x+y;
}

int main()
{
	float pow = 1; // In degrees
	printf("Evaluating for %f\n", pow);
	// This call evaluates hyperbolic sine and cosine for the angle
	float exp = rotation(1, 0, pow);
	printf("e^z is %f\n", exp);
	return 0;
}
