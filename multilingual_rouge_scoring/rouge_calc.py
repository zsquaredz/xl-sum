import argparse
from rouge_score import rouge_scorer
import tempfile

def calc_rouge(prediction_file, reference_file):
    print('calculating ROUGE')
    print('prediction file', prediction_file)
    print('reference file', reference_file)       
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True, lang="arabic")
    scores = {'rouge1':[],'rouge2':[],'rougeL':[]}
    with open(prediction_file, encoding='utf-8') as pred_f,\
        open(reference_file, encoding='utf-8') as ref_f:
        predictions = pred_f.readlines()
        references = ref_f.readlines()
        assert len(predictions) == len(references)
        for i in len(predictions):
            prediction = predictions[i].strip()
            reference = references[i].strip()
            score = scorer.score(target=reference, prediction=prediction)
            print(score['rouge1'])
            print(score['rouge1'][1])
            exit()
            
          

            

        

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

   