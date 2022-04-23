
import psycopg2


def crop_painting(strokes):
    max_x, max_y, min_x, min_y = 0, 0, 1000000, 1000000
    for stroke in strokes:
        radius = stroke[3]/2
        for circle in stroke[4]:
            max_x = max(max_x, circle[0] + radius)
            min_x = min(min_x, circle[0] - radius)
            max_y = max(max_y, circle[1] + radius)
            min_y = min(min_y, circle[1] - radius)
    return max_x, max_y, min_x, min_y


class Database():
    def __init__(self, config):
        self.config = config
        self._conn = None
        self._connect()

    def _connect(self):
        self._conn = psycopg2.connect(
            dbname=self.config['database'],
            user=self.config['user'],
            password=self.config['password'],
            host=self.config['host'])

    def _cursor(self):
        return self._conn.cursor()

    def _close_connection(self):
        self._conn.close()

    def _commit(self):
        self._conn.commit()

    def reconnect(self):
        self._close_connection()
        self._connect()

    def store_painting(self, strokes):
        max_x, max_y, min_x, min_y = crop_painting(strokes)
        cursor = self._cursor()
        cursor.execute(INSERT_PAINTING, (max_x - min_x, max_y - min_y))
        (painting_id,) = cursor.fetchone()
        for stroke in strokes:
            values = (painting_id, stroke[3], stroke[0], stroke[1], stroke[2])
            cursor.execute(INSERT_STROKE, values)
            (stroke_id,) = cursor.fetchone()
            for circle in stroke[4]:
                values = (stroke_id, circle[0] - min_x, circle[1] - min_y)
                cursor.execute(INSERT_CIRCLE, values)
        self._commit()
        cursor.close()
        return painting_id

    def paintings(self):
        painting_list = []
        painting = None
        cursor = self._cursor()
        cursor.execute(STROKES)
        for painting_id, width, height, size, r, g, b, x, y in cursor.fetchall():
            if not painting:
                painting = {'id': painting_id, 'width': width, 'height': height, 'strokes': []}
            if painting['id'] != painting_id:
                painting_list.append(painting)
                painting = {'id': painting_id, 'width': width, 'height': height, 'strokes': []}
            painting['strokes'].append({'size': size, 'r': r, 'g': g, 'b': b,
                                        'circles': list(zip(x, y))})
        if painting:
            painting_list.append(painting)
        cursor.close()
        return painting_list



INSERT_PAINTING = 'INSERT INTO painting(width, height) VALUES (%s, %s) RETURNING id'

INSERT_STROKE = """
INSERT INTO brush_stroke(painting, size, r, g, b)
VALUES (%s,%s,%s,%s,%s)
RETURNING id
"""

INSERT_CIRCLE = "INSERT INTO circle(stroke, x, y) VALUES (%s,%s,%s)"


STROKES = """
SELECT painting.id, width, height, size, r, g, b,
       array_agg(x), array_agg(y)
FROM painting
JOIN brush_stroke ON brush_stroke.painting=painting.id
JOIN circle ON circle.stroke=brush_stroke.id
GROUP BY painting.id, width, height, size, r, g, b, stroke
ORDER BY painting.id, stroke;
"""