#include<stdio.h>

float sigmoid(float z)
{
	// calculate hyperbolic values for sine and cosine
	// returns 1/(1+e^-z)
	float inv2pws[] = {0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125,\
	       	0.00390625, 0.001953125, 0.0009765625, 0.00048828125, 0.000244140625, 0.0001220703125};
	float tanangs[] = {0.5493061, 0.2554128, 0.1256572, 0.0625816, 0.0312602, \
		0.0156263, 0.0078127, 0.0039063, 0.0019531, 0.0009766, 0.0004883, 0.0002441, 0.0001221};
	float atable[] = {0.866025404, 0.838525492, 0.831948719, 0.83032223, 0.8299167, 0.829815386, \
		0.829790061, 0.82978373, 0.829782148, 0.829781752, 0.829781653, 0.829781628, 0.829781622};
	int len = 13, d;
	float x = 1, y = 0, x_, y_, z_;

	z = -z;

	for(int i=0; i<len; i++)
	{
		d = (z<0)?-1:1;
		x_ = x + y*d*inv2pws[i];
		y_ = y + x*d*inv2pws[i];
		z_ = z - d*tanangs[i];
		x = x_;
		y = y_;
		z = z_;

		// extra iterations at 3i+1 for convergence
		if(i==4 || i==13 || i==40)
		{
			d = (z<0)?-1:1;
			x_ = x + y*d*inv2pws[i];
			y_ = y + x*d*inv2pws[i];
			z_ = z - d*tanangs[i];
			x = x_;
			y = y_;
			z = z_;
		}
	}
	// Normalize x and y
	x = (x/atable[len-1]);
	y = (y/atable[len-1]);

	printf("xn: %f, yn: %f, zn: %f\n", x, y, z);
	
	return 1/(1+x+y);
}

int main()
{
	float pow = 1; // In degrees
	printf("Enter value: ");
	scanf("%f",&pow);
	printf("Evaluating for %f\n", pow);
	// This call evaluates hyperbolic sine and cosine for the angle
	float exp = sigmoid(pow);
	printf("sigmoid(z) is %f\n", exp);
	return 0;
}
