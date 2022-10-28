var x = 50;
var b = 200;

function setup() {
  createCanvas(600, 400);
  background(55);
}

function draw() {

}
// draw rectangle the size of x(50) at position mouseX and mouseY
function mousePressed() {
  fill(100);
  circle(mouseX, mouseY, x);

}
