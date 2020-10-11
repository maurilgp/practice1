#Calcula el Análisis de Varianza entre varios grupos de muestras.
import pandas, os, logging, sys

class Anova:

    def _sum(self, sample):
        sum = 0
        for value in sample:
            sum += value
        return sum

    def _mean(self, sample):
        return self._sum(sample) / len(sample)

    def _variance(self, sample):
        mean = self._mean(sample)
        variance = 0
        for value in sample:
            variance += (mean - value) ** 2
        return variance / (len(sample)-1)

    #Between samples
    def _square_sum_between(self, n, sample):
        ssb = 0
        mean = self._mean(sample)
        for value in sample:
            ssb += n * (value - mean) ** 2
        return ssb

    #Within samples
    def _square_sum_within(self, n, sample):
        ssw = 0
        for value in sample:
            ssw += (n - 1) * value
        return ssw


    def __init__(self):
        SAMPLE_SIZE = "Sample Size"
        SAMPLE_MEAN = "Sample Mean"
        SAMPLE_VARIANCE = "Sample Variance"
        SSW = "SSW"
        SSB = "SSB"

        df_data = pandas.read_excel(os.path.abspath("tempfiles\\ANOVA Data.xlsx"))
        print("----------------------------------------------------")
        print("Samples")
        print("----------------------------------------------------")
        print(df_data)

        results_table = []
        k_samples = len(df_data.columns)
        sample_size = len(df_data[df_data.columns[0]])
        for c in df_data.columns:
            result_row = []
            result_row.append(len(df_data[c]))
            result_row.append(self._mean(df_data[c]))
            result_row.append(self._variance(df_data[c]))
            results_table.append(result_row)
        row_names = df_data.columns
        column_names = [SAMPLE_SIZE, SAMPLE_MEAN, SAMPLE_VARIANCE]
        df_results = pandas.DataFrame(results_table, row_names, column_names)

        total_sample_size = self._sum(df_results[SAMPLE_SIZE])
        mean_sample_mean = self._mean(df_results[SAMPLE_MEAN])
        mean_sample_variance = self._mean(df_results[SAMPLE_VARIANCE])
        print("\n----------------------------------------------------")
        print("Means and Variance")
        print("----------------------------------------------------")

        #row = {"Sample Size":total_sample_size,
        #       "Sample Mean":mean_sample_mean,
        #       "Sample Variance":mean_sample__variance
        #       }

        #df_results = df_results.append(row,ignore_index=True)
        print(df_results)
        print("----------------------------------------------------")
        print("Total/Mean\t"+str(total_sample_size)+"\t"+str(mean_sample_mean)+"\t"+str(mean_sample_variance))

        print("\n----------------------------------------------------")
        print("Analysis of Variance")
        print("----------------------------------------------------")
        #Between samples
        bdf = k_samples - 1
        ssb = self._square_sum_between(n=sample_size, sample=df_results[SAMPLE_MEAN])
        msb = ssb / bdf
        #Within samples
        sdf = total_sample_size - k_samples
        ssw = self._square_sum_within(n=sample_size, sample=df_results[SAMPLE_VARIANCE])
        msw = ssw / sdf
        #Total row
        tdf = total_sample_size - 1
        tss = ssb + ssw
        #Fstatistic
        f_statistic = msb / msw

        anova_results_dict = {
            "Source"  : ["Between samples","Within samples","Total"],
            "Sum of squares" : [ssb, ssw, tss],
            "Degrees of freedom" : [bdf, sdf, tdf],
            "Mean Square" : [msb, msw, None],
            "F-statistic" : [f_statistic, None, None]
        }

        anova_df = pandas.DataFrame(anova_results_dict)
        print(anova_df)
