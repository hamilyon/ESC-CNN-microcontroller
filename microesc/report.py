
import os.path
import sys

import numpy
import seaborn as sns
import matplotlib.pyplot as plt     

#from . import common
import urbansound8k
import common

def plot_confusion(cm, classnames, normalize=False):

    if normalize:
        cm = cm_normalize(cm)

    fig, ax = plt.subplots(1, figsize=(10,8))
    sns.heatmap(cm, annot=True, ax=ax);

    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix') 
    ax.xaxis.set_ticklabels(classnames, rotation=60)
    ax.yaxis.set_ticklabels(classnames, rotation=0)
    return fig

def cm_normalize(cm):
    rel = cm.astype('float') / cm.sum(axis=1)[:, numpy.newaxis]
    return rel

def cm_class_accuracy(cm):
    rel = cm_normalize(cm)
    return numpy.diag(rel)

def cm_accuracy(cm):
    correct = numpy.sum(numpy.diag(cm))
    total = numpy.sum(numpy.sum(cm, axis=1))
    return correct/total

def parse(args):

    import argparse

    parser = argparse.ArgumentParser(description='Test trained models')
    a = parser.add_argument

    common.add_arguments(parser)

    a('--out', dest='results_dir', default='./data/results',
        help='%(default)s')


    parsed = parser.parse_args(args)

    return parsed


def main():

    args = parse(None)

    cm = numpy.load(os.path.join(args.results_dir, '{}'.format(args.experiment), 'confusion.npz'))
    val, test = cm['val'], cm['test']


    classnames = urbansound8k.classnames
    val_fig = plot_confusion(100*numpy.mean(val, axis=0), classnames, normalize=True)
    test_fig = plot_confusion(100*numpy.mean(test, axis=0), classnames, normalize=True) 

    c_acc = cm_class_accuracy(numpy.mean(val, axis=0))
    print('test_acc', numpy.mean(c_acc), c_acc) 

    folds_acc = [ cm_accuracy(val[f]) for f in range(0, len(val)) ]

    print('val_acc', numpy.mean(folds_acc), folds_acc)

    val_fig.savefig('val.cm.png')
    test_fig.savefig('test.cm.png')

    print('wrote')

if __name__ == '__main__':
    main()
