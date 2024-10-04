import scipy.cluster
import sklearn.cluster
import numpy
from PIL import Image


def get_clusters(path, num_colors):  # path to file, number of colors to output

    image = Image.open(path)  # create Image object
    image = image.resize((150, 150))  # resize image for efficiency
    ar = numpy.asarray(image)  # convert image into a numpy array
    shape = ar.shape  # get the dimensions of the 3-D array (usual row x column with each grid having 3 values (RGB))
    ar = ar.reshape(numpy.prod(shape[:2]), shape[2]).astype(float)  # converts into a 2-D array with each row being a
    # combination of rows * columns

    kmeans = sklearn.cluster.MiniBatchKMeans(
        n_clusters=num_colors,
        init="k-means++",
        max_iter=20,
        random_state=1000
    ).fit(ar)
    codes = kmeans.cluster_centers_

    vecs, _dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, _bins = numpy.histogram(vecs, len(codes))    # count occurrences

    hex_codes = []
    percentages = []
    size = numpy.prod(shape[:2])
    for index in numpy.argsort(counts)[::-1]:
        color = (tuple([int(code) for code in codes[index]]))
        hex_codes.append("#{:02x}{:02x}{:02x}".format(*color))
        percent = round((counts[index] / size) * 100, 2)
        percentages.append(percent.item())
    return list(zip(hex_codes, percentages))
