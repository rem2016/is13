import re
import json
import data.load as ml
import random


def random_digit(n):
    num = list(range(10))
    ans = ''.join([str(random.choice(num)) for _ in range(n)])
    return ans


text = []
entities = []

for i in range(5):
    w2ne, w2la = {}, {}
    train, _, test, dic = ml.atisfold(2)

    w2idx, ne2idx, labels2idx = dic['words2idx'], dic['tables2idx'], dic['labels2idx']

    idx2w = dict((v, k) for k, v in w2idx.iteritems())
    idx2ne = dict((v, k) for k, v in ne2idx.iteritems())
    idx2la = dict((v, k) for k, v in labels2idx.iteritems())

    test_x, test_ne, test_label = test
    train_x, train_ne, train_label = train
    wlength = 35

    for e in ['train', 'test']:
        for sw, se, sl in zip(eval(e + '_x'), eval(e + '_ne'), eval(e + '_label')):
            text.append(' '.join([idx2w[wx] for wx in sw]))
            this_entities = []
            for wx, la in zip(sw, sl):
                entity_name, entity_type = idx2w[wx], idx2la[la]
                digits = re.findall('DIGIT', entity_name)
                if digits:
                    entity_name = random_digit(len(digits))
                if entity_type == 'O':
                    continue
                this_entities.append({
                    'text': entity_name,
                    'entity': entity_type
                })
            entities.append(this_entities)

sentences = [{
    'intent': 'TEST',
    'text': t,
    'entities': e
} for t, e in zip(text, entities)]

out = {
    'sentences': sentences
}
with open('ATIS.json', 'w') as f:
    json.dump(out, f)
