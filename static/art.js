
var brush_size = 50;

var color_r = 0;
var color_g = 0;
var color_b = 0;

var brush_strokes = [];
var last_stroke = [];

function setup() {
  createCanvas(windowWidth, 0.8*windowHeight);
  background(200);

  fill(color_r, color_g, color_b);
  noStroke();
}

function draw() {

}

function touchStarted() {
  last_stroke = [];
  if (is_drawing()) {
    return false;
  }
}

function touchMoved() {
  if (is_drawing()) {
    ellipse(mouseX, mouseY, brush_size, brush_size);
    last_stroke.push([mouseX, mouseY]);
    return false;
  }
}

function touchEnded() {
  if (last_stroke.length > 0) {
    brush_strokes.push([color_r, color_g, color_b, brush_size, last_stroke]);
    return false;
  }
}

function is_drawing() {
  if (last_stroke.length == 0 || dist(last_stroke[last_stroke.length - 1][0], last_stroke[last_stroke.length - 1][1], mouseX, mouseY) > 0.1*brush_size) {
    if (mouseY > 0) {
      return true;
    }
  }
  return false;
}


function redraw_painting() {
  background(200);
  push();
  for (var i = 0; i < brush_strokes.length; i++) {
    fill(brush_strokes[i][0], brush_strokes[i][1], brush_strokes[i][2]);
    let size = brush_strokes[i][3];
    let stroke = brush_strokes[i][4];
    for (var j = 0; j < stroke.length; j++) {
      ellipse(stroke[j][0], stroke[j][1], size, size);
    }
  }
  pop();
}

function clear_last_stroke() {
  brush_strokes.pop();
  redraw_painting();
}

function set_brush_size(size) {
  brush_size = size;
}

function set_color(r, g, b) {
  color_r = r;
  color_g = g;
  color_b = b;
  fill(color_r, color_g, color_b);
}
