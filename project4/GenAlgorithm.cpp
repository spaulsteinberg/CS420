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
#include <algorithm>

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
		vector <vector <int> > offspring;
		void Init_Bitstring();
		void calc_fitness();
		void run();
		vector<vector<int> > update(vector< vector<int> >, vector<vector<int> >);
		int most_fit(vector<double>);
	public:
		GEN(int, int, int, double, double);
		void show();

};

GEN::GEN(int g, int ps, int ng, double mp, double cp)
{
	gene = g;
	pop_size = ps;
	num_gens = ng;
	mutate_prob = mp;
	cross_p  = cp;
}

vector<vector<int> > GEN::update(vector< vector<int> > source, vector< vector<int> > dest)
{
	for (unsigned int i = 0; i < source.size(); i++)
	{
		for (unsigned int j = 0; j < source[i].size(); j++)
		{
			dest[i][j] = source[i][j];
		}
	}
	return dest;
}

int GEN::most_fit(vector<double> fitness)
{
	double max = -1.0;
	int max_index = 0;
	for (int i = 0; i < pop_size; i++)
	{
		if (fitness[i] > max)
		{
			max = fitness[i];
			max_index = i;
		}
	}
	return max_index;
}

void GEN::Init_Bitstring()
{
	srand(time(NULL));
	bit_s.resize(pop_size);
	offspring.resize(pop_size);
	for (int i = 0; i < pop_size; i++)
	{
		bit_s[i].resize(gene);
		offspring[i].resize(gene);
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

void GEN::run()
{
	/*****************when done add a wrapper around this for the number of generations!!!!***************/
	double crossover, mutation, range1, range2;
	int k, i, cross_iterations, parent_one = 0, parent_two = 0;
	srand(time(NULL));
	calc_fitness();
	range1 = ((double)rand() / (RAND_MAX));
	range2 = ((double)rand() / (RAND_MAX));
	for (i = 0; i < (pop_size/2); i++)
	{
		for (k = 1; k < pop_size; k++)
		{
			if ( (range1 > normal_fitness_total[k-1]) && (range1 <= normal_fitness_total[k]) )
			{
				if (parent_two != k) parent_one = k;
			}
			if ( (range2 > normal_fitness_total[k-1]) && (range2 <= normal_fitness_total[k]) )
			{
				if (parent_one != k) parent_two = k;
			}
			if ( ((parent_one != 0) && (parent_two != 0)) && (parent_one != parent_two) ) break;
		}

/*---------------------------------- No idea if anything below this line works -----------------------------------*/

		/*cross over calcs */
		crossover = ((double)rand() / (RAND_MAX));
		/*If cross_p is greater perform crossover(on a bit flip --> explains why pop/2 iterations... or else just copy them over */
		if (crossover <= cross_p)
		{
			cross_iterations = rand() % gene;
			for (int j = 0; j < cross_iterations; j++)
			{
				offspring[i*2][j] = bit_s[parent_one][j];
				offspring[(i*2)+1][j] = bit_s[parent_two][j];
			}
			for (int n = cross_iterations; n < gene; n++)
			{
				offspring[i*2][n] = bit_s[parent_two][n];
				offspring[(i*2)+1][n] = bit_s[parent_one][n];
			}
		}
		else
		{
			for (int j = 0; j < gene; j++)
			{
				offspring[i*2][j] = bit_s[parent_one][j];
				offspring[(i*2)+1][j] = bit_s[parent_two][j];
			}
		}
		/*Mutation calcs*/
		for (int j = 0; j < gene; j++)
		{
			mutation = ((double)rand() / (RAND_MAX)); //first offspring
			if (mutation <= mutate_prob)
			{
				if (offspring[i*2][j] == 1) offspring[i*2][j] = 0;
				else offspring[i*2][j] = 1;
			}
			
			mutation = ((double)rand() / (RAND_MAX)); //second offspring
			if (mutation <= mutate_prob)
			{
				if (offspring[(i*2)+1][j] == 1) offspring[(i*2)+1][j] = 0;
				else offspring[(i*2)+1][j] = 1;
			}
		}
	}
	
	/*update function*/
	bit_s = update(offspring, bit_s);
	
	int max_index = most_fit(fitness);
	
	int bit_count = 0;
	vector<int> ind_string = bit_s.at(max_index);
	for (unsigned int j = 0; j < ind_string.size(); j++)
	{
		if (ind_string[j] == 1) bit_count++;
	}
	cout << "Max index is: " << max_index << endl;
	cout << "Max index 1's: " << bit_count << endl;
}

/* For testing purposes only. */
void GEN::show()
{
	run();
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
	g.show();
	
	return 0;
}
