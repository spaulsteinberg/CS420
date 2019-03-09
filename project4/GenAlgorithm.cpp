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
		vector<double> normal_fitness_total;
		vector <vector <int> > bit_s;
		void Init_Bitstring();
		void calc_fitness();
		void select_parents();
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
/* March 9 update: Check on fitness vals. Different than write up. everything else is good. */
void GEN::calc_fitness()
{
	unsigned int i, j;
	int index;
	int bit_sum = 0;
	double fit_level = 0;
	double total_fit_count = 0;
	double normal_fit_sum = 0;
	
	Init_Bitstring();
	fitness.resize(pop_size);
	total_fitness.resize(pop_size);
	normal_fitness.resize(pop_size);
	normal_fitness_total.resize(pop_size);

	for (i = 0; i < bit_s.size(); i++)
	{
		index = gene - 1;
		bit_sum = 0;
		for (j = 0; j < bit_s[i].size(); j++)
		{
			if (bit_s[i][j] == 1) bit_sum += pow(2, index);
			index--;
		}
		/*Fitness value */
		fit_level = pow( ( (1.0*bit_sum) / (pow(2,gene)) ), 10 );	
		fitness[i] = fit_level;
		/*Total fitness value*/
	
		total_fit_count += fitness[i];
		total_fitness[i] = total_fit_count;
	
		
	}
	/*Normalized fitness and its running total */
	for (int k = 0; k < pop_size; k++)
	{
		normal_fitness[k] = fitness[k] / total_fit_count;
		normal_fit_sum += normal_fitness[k];
		normal_fitness_total[k] = normal_fit_sum;
	}

}

void GEN::select_parents()
{
	srand(time(NULL));
	calc_fitness();
	double parent1 = ((double)rand() / (RAND_MAX));
	double parent2 = ((double)rand() / (RAND_MAX));
	//for populationsize/2 do this
}

/* For testing purposes only. */
void GEN::print()
{
	calc_fitness();
	cout << "Individual " << setw(17) << "Fitness Value " << setw(20) << right << "Normalized Fitness" << setw(15) << "Running Total" << endl;
	for (unsigned int i = 0; i < fitness.size(); i++)
	{
		cout << setw(5) << i << setw(20)<<right<<fixed<< fitness[i] << setw(20) << normal_fitness[i] << setw(15) << right << normal_fitness_total[i] << endl; 
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
