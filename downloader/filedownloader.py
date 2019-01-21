from cache import lrucache


def download():
    f = open("input_file", "r")
    cache_size = None
    num_inputs = None
    for line in f:
        if cache_size is None:
            cache_size = int(line)
            c = lrucache.ImageLRU(cache_size)
            continue
        if num_inputs is None:
            num_inputs = int(line)
            continue

        c.insert(str(line))

