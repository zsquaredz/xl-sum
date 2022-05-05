import argparse
from rouge_score import rouge_scorer
import tempfile

def calc_rouge(prediction_file, reference_file):
    print('calculating ROUGE')
    print('prediction file', prediction_file)
    print('reference file', reference_file)       

    with tempfile.TemporaryDirectory() as directory:
        # print('The created temporary directory is %s' % directory)
        with open(prediction_file, encoding='utf-8') as pred_f:
            predictions = pred_f.readlines()
            count = 1
            for line in predictions:
                with open(directory + '/'+str(count)+'.decodes', 'w', encoding='utf-8') as ff:
                    ff.write(line + "\n")
                count += 1

        with open(reference_file, encoding='utf-8') as ref_f:
            references = ref_f.readlines()
            count = 1
            for line in references:
                with open(directory + '/'+str(count)+'.targets', 'w', encoding='utf-8') as ff:
                    ff.write(line + "\n")
                count += 1

            

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="summarization")
    parser.add_argument("--prediction_file", type=str, default='./data/test.target', help="Location of prediction file")
    parser.add_argument("--reference_file", type=str, default='./data/test.target', help="Location of reference file")
    args = parser.parse_args()
    calc_rouge(args.prediction_file, args.reference_file)
    # print(f'\t R-1: {r1} | R-2: {r2} | R-L: {rl} | R-Lsum: {rlsum}')
    # r1, r2, rl, rlsum = calc_rouge_hack_for_ja(args.prediction_file, args.reference_file)
    # print(f'\t R-1: {r1} | R-2: {r2} | R-L: {rl} | R-Lsum: {rlsum}')
    # calc_rouge_1(args.prediction_file, args.reference_file)

   