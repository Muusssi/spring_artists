

static final float scale = 0.1;

String paintings_url = "http://localhost:8888/data/paintings";

PImage background;
HashMap<Integer,Painting> paintings = new HashMap<Integer,Painting>();

boolean debug = true;

void setup() {
  //size(1000, 800, P2D);
  fullScreen(P2D);
  frameRate(30);
  background = loadImage("xp_hills.jpg");
  update_paintings_data();
}

void draw() {
  pushStyle();
  tint(255, 40);
  image(background, 0, 0, width, height);
  popStyle();
  for (Painting painting : paintings.values()) {
    painting.draw();
  }
  if (frameCount%1000 == 0) {
    update_paintings_data();
  }
}

void keyPressed() {
  if (keyCode == ' ') {
    update_paintings_data();
  }
  else if (keyCode == 'B') {
    debug = !debug;
  }
}


void update_paintings_data() {
  JSONArray paintings_list = loadJSONObject(paintings_url).getJSONArray("paintings");
  for (int i = 0; i < paintings_list.size(); ++i) {
    JSONObject painting_data = paintings_list.getJSONObject(i);
    if (!paintings.containsKey(painting_data.getInt("id"))) {
      new Painting(painting_data);
    }

  }

}



public class Painting {

  int id;
  int painting_width, painting_height;
  int x, y;
  JSONArray strokes;

  PGraphics canvas;
  int stroke_index = 0;
  int cirle_index = 0;
  int life_counter = 0;

  public Painting (JSONObject data) {
    this.id = data.getInt("id");
    this.painting_width = data.getInt("width");
    this.painting_height = data.getInt("height");
    this.reset_canvas();
    this.strokes = data.getJSONArray("strokes");
    paintings.put(this.id, this);
  }

  void reset_canvas() {
    this.canvas = createGraphics(this.painting_width, this.painting_height, P2D);
    this.canvas.beginDraw();
    this.canvas.endDraw();
    this.x = int(random(0, width - this.painting_width*scale));
    this.y = int(random(height/4, height - this.painting_height*scale));
    this.life_counter = 0;
    this.stroke_index = 0;
    this.cirle_index = 0;
  }

  void paint() {
    if (stroke_index < this.strokes.size()) {
      JSONObject stroke = this.strokes.getJSONObject(stroke_index);
      JSONArray circles = stroke.getJSONArray("circles");
      if (cirle_index < circles.size()) {
        this.canvas.beginDraw();
        this.canvas.noStroke();
        this.canvas.fill(stroke.getInt("r"), stroke.getInt("g") ,stroke.getInt("b"));
        this.canvas.ellipse(circles.getJSONArray(cirle_index).getFloat(0),
                            circles.getJSONArray(cirle_index).getFloat(1),
                            stroke.getInt("size"), stroke.getInt("size"));
        this.canvas.endDraw();
        cirle_index++;
      }
      else {
        stroke_index++;
        cirle_index = 0;
      }
    }
    else {
      life_counter++;
      if (life_counter > 1000) {
        this.reset_canvas();
      }
    }
  }

  void draw() {
    this.paint();
    if (debug) {
      text(this.id, this.x, this.y);
    }
    image(this.canvas, this.x, this.y, this.painting_width*scale, this.painting_height*scale);
  }

}
