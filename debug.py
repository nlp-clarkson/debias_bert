#!/usr/bin/env python3

import tensorflow as tf

checkpoint = '/tmp/MRPC/model.ckpt-343'

saver = tf.train.Saver()

with tf.Session() as sess:
    saver.restore(sess, checkpoint)
    print(sess)

