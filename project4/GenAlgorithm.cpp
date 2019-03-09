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
#include <cmath>
#include <iomanip>
using namespace std;

class GEN
{
	private:
		int gene, pop_size, num_gens;
		double mutate_prob, cross_p;
		vector <double> fitness;
		vector<double> total_fitness;
		vector<double> normal_fitness;
		vector <vector <int> > bit_s;
		void Init_Bitstring();
		void calc_fitness();
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

void GEN::Init_Bitstring()
{
	srand(time(NULL));
	bit_s.resize(pop_size);
	for (int i = 0; i < pop_size; i++)
	{
		bit_s[i].resize(gene);
		for (int j = 0; j < gene; j++)
		{
			bit_s[i][j] = rand() % 2;
		}
	}
}
/* March 8 update: Check on fitness vals. Messing everything else up. */
void GEN::calc_fitness()
{
	unsigned int i, j;
	int index;
	int bit_sum = 0;
	double fit_level = 0;
	double total_fit_count = 0;
	double normal_fit_sum = 0;
	
	Init_Bitstring();
	fitness.resize(bit_s.size());
	total_fitness.resize(fitness.size());
	normal_fitness.resize(total_fitness.size());
	
	for (i = 0; i < bit_s.size(); i++)
	{
		index = gene - 1;
		bit_sum = 0;
		for (j = 0; j < bit_s[i].size(); j++)
		{
			if (bit_s[i][j] == 1) bit_sum += pow(2, index);
			else bit_sum += 1;
			index--;
		}
		fit_level = pow( ((double)bit_sum/(pow(2,gene))), 10);	
		fitness[i] = fit_level;

		total_fit_count += fit_level;
		total_fitness[i] = total_fit_count;
		normal_fitness[i] = fitness[i] / total_fitness[i];
		normal_fit_sum += normal_fitness[i];
	}

}

/* For testing purposes only. I know its ugly lol. */
void GEN::print()
{
	calc_fitness();
	cout << "Individual " << setw(17) << "Fitness Value " << setw(20) << right << "Normalized Fitness" << setw(15) << "Running Total" << endl;
	for (unsigned int i = 0; i < fitness.size(); i++)
	{
		cout << setw(5) << i << setw(20)<<right<<fixed<< fitness[i] << setw(20) << normal_fitness[i] << setw(15) << right << total_fitness[i] << endl; 
	}
	cout << endl;
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
