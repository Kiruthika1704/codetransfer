import os
import sys

from src.logger import create_logger
from src.data.dictionary import Dictionary


if __name__ == '__main__':

    logger = create_logger(None, 0)

    voc_path = sys.argv[1]
    txt_path = sys.argv[2]
    bin_path = sys.argv[2] + '.pth'
    assert os.path.isfile(voc_path)
    assert os.path.isfile(txt_path)

    dico = Dictionary.read_vocab(voc_path)
    logger.info("")

    data = Dictionary.index_data(txt_path, bin_path, dico)
    logger.info("%i words (%i unique) in %i sentences." % (
        len(data['sentences']) - len(data['positions']),
        len(data['dico']),
        len(data['positions'])
    ))
    if len(data['unk_words']) > 0:
        logger.info("%i unknown words (%i unique), covering %.2f%% of the data." % (
            sum(data['unk_words'].values()),
            len(data['unk_words']),
            sum(data['unk_words'].values()) * 100. /
            (len(data['sentences']) - len(data['positions']))
        ))
        if len(data['unk_words']) < 30000:
            for w, c in sorted(data['unk_words'].items(), key=lambda x: x[1])[::-1][:30]:
                logger.info("%s: %i" % (w, c))
