import argparse
from rouge_score import rouge_scorer

def calc_rouge(prediction_file, reference_file, stem, lang):
    print('calculating ROUGE')
    print('prediction file', prediction_file)
    print('reference file', reference_file)       
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=stem, lang=lang)
    scores = {'rouge1':[],'rouge2':[],'rougeL':[]}
    with open(prediction_file, encoding='utf-8') as pred_f,\
        open(reference_file, encoding='utf-8') as ref_f:
        predictions = pred_f.readlines()
        references = ref_f.readlines()
        assert len(predictions) == len(references)
        for i in range(len(predictions)):
            prediction = predictions[i].strip()
            reference = references[i].strip()
            score = scorer.score(target=reference, prediction=prediction)
            scores['rouge1'].append(score['rouge1'][2])
            scores['rouge2'].append(score['rouge2'][2])
            scores['rougeL'].append(score['rougeL'][2])
    return sum(scores['rouge1']) / 100*float(len(scores['rouge1'])), sum(scores['rouge2']) / 100*float(len(scores['rouge2'])), sum(scores['rougeL']) / 100*float(len(scores['rougeL']))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="summarization")
    parser.add_argument("--prediction_file", '-p', type=str, default='./data/test.target', help="Location of prediction file")
    parser.add_argument("--reference_file", '-r', type=str, default='./data/test.target', help="Location of reference file")
    parser.add_argument("--stem", action='store_true', help="Use stemming")
    parser.add_argument("--lang", '-l', type=str, default='english', help="Language")
    args = parser.parse_args()
    r1, r2, rl = calc_rouge(args.prediction_file, args.reference_file, args.stem, args.lang)
    print(f'\t R-1: {r1} | R-2: {r2} | R-L: {rl}')
    # r1, r2, rl, rlsum = calc_rouge_hack_for_ja(args.prediction_file, args.reference_file)
    # print(f'\t R-1: {r1} | R-2: {r2} | R-L: {rl} | R-Lsum: {rlsum}')
    # calc_rouge_1(args.prediction_file, args.reference_file)

   