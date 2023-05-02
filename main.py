import train_test
import scipy.stats as stats
import numpy as np

data = train_test.data
correct = train_test.correct
predicted_und, predicted_d, actual_d, actual_und = train_test.predicted_und, train_test.predicted_d, train_test.actual_d, train_test.actual_und
fn, tn, fp, tp = train_test.fn, train_test.tn, train_test.fp, train_test.tp

print(f"Percent correct: {correct / len(data) * 100}%")
print(f"Total datapoints: {len(data)}")

print(f"Actual Positives: {actual_d} | Actual Negatives: {actual_und} | Predicted Positives: {predicted_d} | Predicted Negatives: {predicted_und}")
print(f"True Positives: {tp} | False Negatives: {fn} | False Positives: {fp} | True Negatives: {tn}")

chi_square_test_statistic, p_value = stats.chisquare([predicted_und, predicted_d], [actual_und, actual_d])
print(f'Chi square test statistic: {str(chi_square_test_statistic)}')
print(f'p-value: {str(p_value)}')
print(f'Critical value: {stats.chi2.ppf(1 - 0.05, df=1)}')
