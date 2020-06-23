#include<stdio.h>

void rotation(float x, float y, float z)
{
	float inv2pws[] = {1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125};
	float tanangs[] = {45.0, 26.5651, 14.0362, 7.125, 3.5763, 1.7899, 0.8952, 0.4476};
	float atable[] = {1, 1.41421, 1.58114, 1.6298, 1.64248, 1.64569, 1.64649, 1.64669};
	int len = 3, d;
	float x_, y_, z_;

	for(int i=0; i<len; i++)
	{
		d = (z<0)?-1:1;
		x_ = x - y*d*inv2pws[i];
		y_ = y + x*d*inv2pws[i];
		z_ = z - d*tanangs[i];
		x = x_;
		y = y_;
		z = z_;
	}
	// Normalize x and y
	x = x/atable[len-1];
	y = y/atable[len-1];

	printf("xn: %f, yn: %f, zn: %f\n", x, y, z);
}

int main()
{
	float angle = 60; // In degrees
	printf("Evaluating for %f\n", angle);
	// This call evaluates sine and cosine for the angle
	rotation(1, 0, angle);
	return 0;
}
