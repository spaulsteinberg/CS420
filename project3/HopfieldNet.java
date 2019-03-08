/*
    Author: Samuel Steinberg
    Date: February 27th, 2019
    This program simulates a Hopfield Network. The program takes a single argument that specifies the
    number of times the program is executed.
 */

import java.io.*;
import java.util.*;
public class HopfieldNet
{
    private int[][] chart = new int[50][100]; //main chart
    private static int N = 100;
    private float[][] weights = new float[100][100]; //weight chart
    private int[] neural_net = new int[100]; //neural network array
    private float[] stable_state = new float[50]; //stable state array
    private float[] unstable_state = new float[50];
    private float[] unstable_prob = new float[50];
    private int num_sims;

    public HopfieldNet(int n)
    {
        this.num_sims = n;
    }

    private void SetChart() {
        /*Set chart to random numbers */
        for (int i = 0; i < chart.length; i++) {
            for (int j = 0; j < chart[i].length; j++) {
                int temp = (int) Math.round(Math.random());
                if (temp == 0) temp = -1;
                chart[i][j] = temp;
            }
        }

    }
    /*Initializes stabilization chart */
    private void Initialize_Stable()
    {
        for (int i = 0; i < 50; i++)
        {
            stable_state[i] = 0;
            unstable_state[i] = 0;
        }

    }
    /*Calculate weights for each vector */
    private void Calculate_Weights(int p)
    {
        /*Initialize the weights 2D array to 0 */
        for (int i = 0; i < weights.length; i++)
        {
            for (int j = 0; j < weights[i].length; j++)
            {
                weights[i][j] = 0;
            }
        }

        for (int i = 0; i < 100; i++)
        {
            for (int j = 0; j < 100; j++)
            {
                if (i==j) weights[i][j] = 0;
                else {
                    for (int k = 0; k < p; k++)
                        weights[i][j] += ((1.0 / N) * (float) (chart[k][i] * chart[k][j]));
                }
            }
        }
    }

    private void SetUp_Neural(int p)
    {
        float[] stable_prob = new float[50];
        float count = 0;
        int update_value = 0;
        float h = 0;
        for (int p1 = 0; p1 < p; p1++) //pattern wrapper
        {
            neural_net = chart[p1];
            for (int i = 0; i < 100; i++)
            {
                h = 0;
                for (int j = 0; j < 100; j++)
                {
                    h += weights[i][j]*((float)neural_net[j]);
                }
                if (h >= 0) update_value = 1;
                else update_value = -1;
                if (update_value != neural_net[i])
                {
                    count++;
                    break;
                }
            }

        }
        stable_state[p-1] += p - count;
        stable_prob[p-1] = stable_state[p-1] / p;
        unstable_prob[p-1] = 1 - stable_prob[p-1];
    }

    private void Imprint_and_Stabilize()
    {

        float[] stable_average = new float[50];
        float[] unstable_prob_avg = new float[50];
        float[] stable_count_avg = new float[50];
        for (int n = 0; n < num_sims; n++)
        {
            SetChart();
            Initialize_Stable();
            for (int p = 1; p <= 50; p++) //wrapper for 50 vectors
            {
                Calculate_Weights(p);
                SetUp_Neural(p);
            }
            for (int i = 0; i < stable_state.length; i++)
            {
                stable_average[i] += stable_state[i];
                unstable_prob_avg[i] += unstable_prob[i];
            }

        }
        for (int i = 0; i < stable_average.length; i++)
        {
            stable_count_avg[i] = stable_average[i] / num_sims;
            unstable_prob_avg[i] /= num_sims;
        }
       // Write_to_CSV(unstable_prob_avg, stable_count_avg);

    }

    private void Write_to_CSV(float[] unstable_prob_avg, float[] stable_count_avg)
    {
        int iter;
        try
        {
            File f =new File("HopfieldMaster.csv");
            FileOutputStream fstr = new FileOutputStream(f);
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(fstr));
            bw.write("Name: , Samuel Steinberg \n");
            bw.write("CS420, Project 3 Hopfield Network\n\n");
            bw.write("p , Stable States, Probability Unstable \n");
            for (int p = 0; p < 50; p++)
            {
                iter = p + 1;
                bw.write(iter + "," + stable_count_avg[p] + "," + unstable_prob_avg[p] + "\n");
            }
            bw.flush();
            bw.close();
        }
        catch(IOException err)
        {
            err.getStackTrace();
        }
    }

    public void run()
    {
        Imprint_and_Stabilize();
    }

    public static void main(String[] args)
    {
        HopfieldNet hfn = new HopfieldNet(Integer.parseInt(args[0])); //can be changed in run->edit configs
        hfn.run();
    }
}
