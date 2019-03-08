/*
	Author: Samuel Steinberg
	Date: March 7th, 2019
	CS420 - Project 4 Genetic Algorithm
*/
#include <iostream>
#include <cstdio>
#include <string>
#include <cstdlib>
#include <vector>
using namespace std;

class GEN
{
	private:
		int gene, pop_size, num_gens;
		double mutate_prob, cross_p;
		vector< vector<int> > Init_Bitstring();
	public:
		GEN(int, int, int, double, double);
		void print();

};

GEN::GEN(int g, int ps, int ng, double mp, double cp)
{
	gene = g;
	pop_size = ps;
	num_gens = ng;
	mutate_prob = mp;
	cross_p  = cp;
}

vector<vector<int> > GEN::Init_Bitstring()
{
	srand(time(NULL));
	vector< vector<int> > bit_strings;
	bit_strings.resize(pop_size);
	for (int i = 0; i < pop_size; i++)
	{
		bit_strings[i].resize(gene);
		for (int j = 0; j < gene; j++)
		{
			bit_strings[i][j] = rand() % 2;
		}
	}
	return bit_strings;
}

void GEN::print()
{
	printf("%d %d %d %f %f\n", gene, pop_size, num_gens, mutate_prob, cross_p);
	vector< vector<int> > bit_strings = Init_Bitstring();
	for (unsigned int i = 0; i < bit_strings.size(); i++)
	{
		for (unsigned int j = 0; j < bit_strings[i].size(); j++)
		{
			cout << bit_strings[i][j] << " ";
		}
		cout << endl;
	}
}

int main(int argc, char *argv[])
{
	if (argc != 6) fprintf(stderr, "Wrong arguments: L | N | G | Pm | Pc "); 
	int genes = atoi(argv[1]);
	int pop_size = atoi(argv[2]);
	int num_gens = atoi(argv[3]);
	double mutation_prob = atof(argv[4]);
	double cross_prob = atof(argv[5]);

	GEN g(genes, pop_size, num_gens, mutation_prob, cross_prob);
	g.print();

	return 0;
}
