from spy_eye_app import db
from spy_eye_app.models import Coor

from pylab import *

def run():
    coors = db.session().query(Coor).filter_by(oper_id=846).all()
    data_x = [coor.x for coor in coors]
    data_y = [coor.y for coor in coors]

    figure(figsize=(19.2, 10.8))
    scatter(data_x, data_y, cmap=cm.get_cmap('spring'))
    savefig("test.png")
