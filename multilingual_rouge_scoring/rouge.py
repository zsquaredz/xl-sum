# coding=utf-8
# Copyright 2020 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""Main routine to calculate ROUGE scores across text files.

Designed to replicate scores computed by the ROUGE perl implementation as
closely as possible.

Output is a text file in CSV format.

Sample usage:

rouge ---rouge_types=rouge1,rouge2,rougeL \
    --target_filepattern=*.targets \
    --prediction_fliepattern=*.decodes \
    --output_filename=scores.csv \
    --use_stemmer

Which is equivalent to calling the perl ROUGE script as:

ROUGE-1.5.5.pl -m -e ./data -n 2 -a /tmp/rouge/settings.xml

Where settings.xml provides target and decode text.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
from rouge_score import io
from rouge_score import rouge_scorer
from rouge_score import scoring
import tempfile

flags.DEFINE_string("target_filepattern", None,
                    "Files containing target text.")
flags.DEFINE_string("target_file", None,
                    "File containing target texts.")
flags.DEFINE_string("prediction_filepattern", None,
                    "Files containing prediction text.")
flags.DEFINE_string("prediction_file", None,
                    "Files containing prediction texts.")
flags.DEFINE_string("output_filename", None,
                    "File in which to write calculated ROUGE scores as a CSV.")
flags.DEFINE_string("delimiter", "\n",
                    "Record delimiter  in files.")
flags.DEFINE_list("rouge_types", ["rouge1", "rouge2", "rougeL"],
                  "List of ROUGE types to calculate.")
flags.DEFINE_boolean("use_stemmer", False,
                     "Whether to use Porter stemmer to remove common suffixes.")
flags.DEFINE_boolean("aggregate", True,
                     "Write aggregates if this is set to True")
flags.DEFINE_string("lang", None,
                    "Language to be used for rouge calculation.")

FLAGS = flags.FLAGS


def main(argv):
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  with tempfile.TemporaryDirectory() as directory:
    # print('The created temporary directory is %s' % directory)
    with open(FLAGS.prediction_file, encoding='utf-8') as pred_f:
      predictions = pred_f.readlines()
      count = 1
      for line in predictions:
        with open(directory + '/'+str(count)+'.decodes', 'w', encoding='utf-8') as ff:
          ff.write(line + "\n")
        count += 1

    with open(FLAGS.target_file, encoding='utf-8') as ref_f:
      references = ref_f.readlines()
      count = 1
      for line in references:
        with open(directory + '/'+str(count)+'.targets', 'w', encoding='utf-8') as ff:
          ff.write(line + "\n")
        count += 1
        
    scorer = rouge_scorer.RougeScorer(FLAGS.rouge_types, use_stemmer=FLAGS.use_stemmer, lang=FLAGS.lang)
    aggregator = scoring.BootstrapAggregator() if FLAGS.aggregate else None
    io.compute_scores_and_write_to_csv(
        directory+'/'+FLAGS.target_filepattern,
        directory+'/'+FLAGS.prediction_filepattern,
        FLAGS.output_filename,
        scorer,
        aggregator,
        delimiter=FLAGS.delimiter)


if __name__ == "__main__":
  flags.mark_flag_as_required("target_filepattern")
  flags.mark_flag_as_required("prediction_filepattern")
  flags.mark_flag_as_required("output_filename")
  app.run(main)

  # python -m rouge \
  # --target_filepattern=*.targets \
  # --prediction_filepattern=*decodes \
  # --output_filename=zz.csv \
  # --use_stemmer=true \
  # --lang='english' \
  # --target_file=/home/hpczhao1/rds/hpc-work/multilingual_adapters/predictions/mBART/wikilingual/mbart_large_cc25_bz4_lr1e-5_ja-en.gold.txt.val \
  # --prediction_file=/home/hpczhao1/rds/hpc-work/multilingual_adapters/predictions/mBART/wikilingual/mbart_large_cc25_bz4_lr1e-5_ja-en.txt.val
