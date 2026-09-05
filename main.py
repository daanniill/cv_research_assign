import csv
from pathlib import Path
from focus_detect_alg import process_data

def main():
  src = Path("dataset")
  results = process_data(src)

  # print the results
  ground_truth = {}

  with open("ground_truth_files.csv", newline="") as f:
    for row in csv.DictReader(f):
      key = (row["folder"], row["quadrant"])
      ground_truth[key] = row["ground_truth_filename"]

  correct = 0
  total = 0


  for img_set, quadrants in results.items():
    for quadrant, variances in quadrants.items():
      pred_file, highest_var = max(variances, key=lambda item: item[1])

      true_file = ground_truth[(img_set, quadrant)]
      is_correct = pred_file == true_file

      correct += int(is_correct)
      total += 1

  success_rate = correct / total * 100

  print(f"\nCorrect: {correct}/{total}")
  print(f"Incorrect: {total - correct}/{total}")
  print(f"Success rate: {success_rate:.1f}%")

if __name__ == "__main__":
    main()