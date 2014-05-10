import pygmaps

not_accepted = ['rent allowance not', 'rent allowance cannot', 'no rent allowance']

accepted = ['rent allowance accepted']

considered = ['rent allowance considered', 'rent allowance will be considered']


def clean_json(fname):
    """ Turn the output of scrapy into valid JSON. """
    clean_name = fname.split('.json')[0] + '-fixed.json'
    lines=[]
    with open(fname, 'r') as infile, open(clean_name, 'w') as outfile:
        outfile.write('[')
        for line in infile:
            lines.append(line)
        outfile.write(','.join(lines))
        outfile.write(']')      

    print "Cleaned JSON file: " + clean_name

def create_map(zoom=13):
    gmap = pygmaps.maps(53, -8, zoom)
    return gmap

def add_points(gmap, points, colour):
    for point in points:
        lat = point[0]
        lng = point[1]
        gmap.addpoint(lat, lng, colour)

def draw_map(gmap, fname = './map.html'):
    gmap.draw(fname)
