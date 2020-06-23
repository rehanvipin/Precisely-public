#include<stdio.h>

int steps(int angle)
{
	// Calculate no of steps required to get angle to 0, using binsearch
	// Angle must be between 0 and 90
	// Recreate angle with a tracker
	int count=0, track=0;
	int table[] = {45, 22, 11, 5, 2, 1, 1}, ti=0, tn=6;
	while(angle != 0)
	{
		printf("%d ",table[ti]);
		if(angle>0)
		{
			angle = angle-table[ti];
			track += table[ti];
		}
		else
		{
			angle = angle+table[ti];
			track -= table[ti];
		}
		count++;
		if(ti == tn)
			break;
		ti++;
	}
	printf(":%d: ", track);
	return count;
}

float arctan(float x, float y)
{
	float costable[] = {0.7071, 0.9272, 0.9816, 0.9962, 0.9994, 0.9998, 0.9998};
	float sintable[] = {0.7071, 0.3746, 0.1908, 0.0872, 0.0349, 0.0175, 0.0175};
	float xnew, ynew;
	float retangle=0, angle=45;
	int index=0;
	while(y != 0 && index < 7)
	{
		printf("%f & %f\n", x, y);
		if(y < 0)
		{
			xnew = x*costable[index] - y*sintable[index];
			ynew = y*costable[index] + x*sintable[index];
			retangle -= angle;
		}
		else
		{
			xnew = x*costable[index] + y*sintable[index];
			ynew = y*costable[index] - x*sintable[index];
			retangle += angle;
		}
		x = xnew;
		y = ynew;
		angle /= 2;
		index++;
	}
	printf("Hypotenuse: %f\n", x);
	return retangle;
}

float tanarctan(float  x, float y)
{
	float tantable[] = {1.0, 0.404, 0.1944, 0.0875, 0.0349, 0.0175, 0.0175};
	float xnew, ynew;
	float retangle = 0, angle = 45;
	int index = 0;
	while(y != 0 && index<7)
	{
		if(y < 0)
		{
			xnew = x - y*tantable[index];
			ynew = y + x*tantable[index];
			retangle += angle;
		}
		else
		{
			xnew = x + y*tantable[index];
			ynew = y - x*tantable[index];
			retangle -= angle;
		}
		angle /= 2;
		index++;
		x = xnew;
		y = ynew;
	}
	return -retangle;
}

float cordicarctan(float x, float y)
{
	float angtable[] = {45.0, 26.5651, 14.0362, 7.125, 3.5763, 1.7899, 0.8952};
	int index = 0;
	float xnew, ynew, retangle = 0;
	while(y != 0 && index < 7)
	{
		printf("x:%f, y:%f\n", x, y);
		if(y > 0)
		{
			xnew = x + ((int)y >> index);
			ynew = y - ((int)x >> index);
			retangle += angtable[index];
		}
		else
		{
			xnew = x - ((int)y >> index);
			ynew = y + ((int)x >> index);
			retangle -= angtable[index];
		}
		index++;
		x = xnew;
		y = ynew;
	}
	return retangle;
}

int main()
{
	float x, y;
	/*
	for(x=0; x<=90; x++)
	{
		y = steps(x);
		printf("%d for %d\n", y, x);
	}
	*/

	x = 100;
	y = 200;
	float theta = cordicarctan(x, y);
	printf("Angle of vector wrt x-axis is %f \n", theta);

	return 0;
}
