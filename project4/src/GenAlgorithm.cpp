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
#include <fstream>
#include <ctime>
#include <sstream>
#include <iterator>
#include <ostream>

using namespace std;

/*GEN class contains data needed by algorithms --> constructor takes the gene length, population size, number of generations,
  probability of mutation, crossover probability, the number of runs for each sim, and an simulation ID */
class GEN
{
	private:
		int gene, pop_size, num_gens, runs, sim_id;
		double mutate_prob, cross_p, total_fit_count, normal_fit_sum;
		vector<double> avg_fitness;
		vector <double> fitness;
		vector<double> total_fitness;
		vector<double> normal_fitness;
		vector<double> normal_fitness_total;
		vector <vector <int> > bit_s;
		vector <vector <int> > offspring;
		void init_bitstring();
		void calc_fitness();
		void run();
		vector<vector<int> > update(vector< vector<int> >, vector<vector<int> >);
		int most_fit(vector<double>);
	public:
		GEN(int, int, int, double, double, int, int);
		void show();

};

/* In addition to the program args, the constructor also resizes necessary vectors and initializes the random number generator */
GEN::GEN(int g, int ps, int ng, double mp, double cp, int ru, int si)
{
	gene = g;
	pop_size = ps;
	num_gens = ng;
	mutate_prob = mp;
	cross_p  = cp;
	runs = ru;
	sim_id = si;
	fitness.resize(pop_size);
	total_fitness.resize(pop_size);
	normal_fitness.resize(pop_size);
	normal_fitness_total.resize(pop_size);
	srand(time(NULL));
}
/* This function takes two 2D vectors and copies the source to dest */
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
/*Run through fitness vector and find the max. Return the index. */
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
/*Initialize bit string to random */
void GEN::init_bitstring()
{
	bit_s.resize(pop_size);
	offspring.resize(pop_size);
	avg_fitness.resize(num_gens);
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
/*This function calculates fitness. */
void GEN::calc_fitness()
{
	unsigned int i, j;
	int index;
	unsigned long bit_sum = 0;
	double fit_level = 0;
	total_fit_count = 0;
	normal_fit_sum = 0;
	
	/*Go through strings and find bit sum */
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
		fit_level = pow( ( (1.0*bit_sum) / (pow(2,(1.0)*gene)) ), 10 );	
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

/*This function runs the sim*/
void GEN::run()
{
	double crossover, mutation, range1, range2;
	int k, i, cross_iterations, parent_one = 0, parent_two = 0;
	
	stringstream ss;
	ofstream os;
	/*Open file, give error is a failure, if the file is empty write the header...if not just print some new lines between sims */
	string filename = "GenMaster" + to_string(sim_id) + ".csv";
	/* --------------- Add desired file name below ----------------- */
	os.open(filename, ios::app);
	/* ------------------------------------------------------------- */

	if (os.fail()) cerr << "Error opening file..." << endl;
	if (os.tellp() == 0)
	{
		os << "Name: Samuel Steinberg\n";
		os << "CS420 Project 4: Genetic Algorithms\n";
		os << "Experiments are conducted with the parameters listed above the runs\n\n";
	}
	else os << "\n\n";
	
	/* Vital info about what the following runs represent*/
	os << "Number of Genes:,," << gene << "\n";
	os << "Population Size:,," << pop_size << "\n";
	os << "Number of Generations:,," << num_gens << "\n";
	os << "Mutation Probability:,," << mutate_prob << "\n";
	os << "Crossover Probability:,," << cross_p << "\n";
	os << "Number of Runs:,," << runs << "\n\n";
	
	for (int r = 0; r < runs; r++) 
	{
		os << "Run " << (r+1) << "\n";
		init_bitstring();
		os << "Generation,Average Fitness,Best Fit,Correct Bits,Best String\n";
		for (int gener = 0; gener < num_gens; gener++)
		{
			calc_fitness();
			
			/*Find two distinct parents to mate*/
			for (i = 0; i < (pop_size/2); i++)
			{
				range1 = ((double)rand() / (RAND_MAX));
				range2 = ((double)rand() / (RAND_MAX));
				parent_one = 0; parent_two = 0;
				
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
			auto ind_string = bit_s.at(max_index);
		
			/*Get number of correct bits in most fit string*/
			for (unsigned int j = 0; j < ind_string.size(); j++)
			{
				if (ind_string[j] == 1) bit_count++;
			}
			
			/*Calculate average fitness for each generation and get the bit string of the most fit */
			avg_fitness[gener] = total_fit_count / (1.0*pop_size);
			copy(ind_string.begin(), ind_string.end(), ostream_iterator<int>(ss,""));
			string best = ss.str();
			/*Write the generation, average fitness, best fitness, correct bits, and most fit string....then clear stringstream*/
			os  <<  gener << "," << avg_fitness[gener] << "," <<  fitness[max_index] << "," << bit_count << "," << "'" + best << "\n";
			ss.str("");			
		}//gener
	} //runs

	os.close();
}

/* Show is public. Everything else private.*/
void GEN::show()
{
	run();
}

int main(int argc, char *argv[])
{
	if (argc != 8) fprintf(stderr, "Wrong arguments: L | N | G | Pm | Pc | R | ID"); 
	int genes = atoi(argv[1]);
	int pop_size = atoi(argv[2]);
	int num_gens = atoi(argv[3]);
	double mutation_prob = atof(argv[4]);
	double cross_prob = atof(argv[5]);
	int runs = atoi(argv[6]);
	int sim_ = atoi(argv[7]);
	GEN g(genes, pop_size, num_gens, mutation_prob, cross_prob, runs, sim_);
	g.show();
	
	return 0;
}
