#!/usr/bin/env python2
#-*- coding: utf-8 -*-

import cv
import datetime
import optparse
import os
import os.path
import time

if __name__ == '__main__':
    # get first webcam
    cam = cv.CaptureFromCAM(-1)
    cascade = cv.Load('frontal.xml')

    # for now we've seen nobody
    someone = False

    parser = optparse.OptionParser()
    parser.add_option('-d', '--delay', dest='delay', help='Delay between two iterations.', type='int', default=1)
    parser.add_option('-f', '--format', dest='format', help='Output format of images.', type='string', default='.png')
    parser.add_option('-o', '--output', dest='output', help='Output dir.', type='string', default='out/')

    (o, _) = parser.parse_args()

    # create output dir if necessary
    if not os.path.exists(o.output):
        os.makedirs(o.output)

    while True:
        # request an image from the webcam
        im = cv.QueryFrame(cam)
        faces = cv.HaarDetectObjects(im, cascade, cv.CreateMemStorage(0), 1.5, 2, 0, (20, 20))

        if not someone:
            # there was nobody and we've seen at least one person
            if len(faces) != 0:
                someone = True

                # show all faces (not so useful)
                for m in faces:
                    (x, y, w, h), _ = m
                    cv.Rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # save images to an unique file
                filename = os.path.join(o.output, datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p') + o.format)
                cv.SaveImage(filename, im)

        # nobody ?
        elif len(faces) == 0:
            someone = False

        # wait between iterations
        time.sleep(o.delay)

