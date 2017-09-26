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
is_train = []

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
            start_index = 0
            this_text = []
            this_entities = []
            for wx, la in zip(sw, sl):
                entity_name, entity_type = idx2w[wx], idx2la[la]
                digits = re.findall('DIGIT', entity_name)
                if digits:
                    entity_name = random_digit(len(digits))

                this_text.append(entity_name)
                start_index += len(entity_name) + 1

                if entity_type == 'O':
                    continue
                elif entity_type.startswith('B'):
                    this_entities.append({
                        'text': entity_name,
                        'entity': entity_type[2:],
                        'start': start_index,
                        'end': start_index + len(entity_name)
                    })
                elif entity_type.startswith('I'):
                    this_entities[-1]['end'] = start_index + len(entity_name)
                    this_entities[-1]['text'] += ' ' + entity_name

            entities.append(this_entities)
            text.append(' '.join(this_text))
            is_train.append(e == 'train')

sentences = [{
    'intent': 'TEST',
    'text': t,
    'entities': e,
    'train_set': is_train
} for t, e, is_train in zip(text, entities, is_train)]

out = {
    'sentences': sentences
}
with open('ATIS.json', 'w') as f:
    json.dump(out, f)
