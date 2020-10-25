PFont mastheadFont;
int colorMode = 0;

void setup() {
  size(880, 528);
  mastheadFont = loadFont("OldEnglishTextMT-36.vlw");
  textAlign(CENTER, CENTER);
}

void drawBlack() {
  // black layer
  fill(0);
  stroke(0);
  textFont(mastheadFont);
  text("Meysenburg Press", width / 2, 20);
  line(width / 4, 5, width / 4, 35);
  line(3 * width / 4, 5, 3 * width / 4, 35);
  
  line(width / 3, 54, width / 3, 395);
  line(2 * width / 3, 54, 2 * width / 3, 395);
  
  line(0, 400, width, 400);
  for(int i = 1; i <= 4; i++) {
    line(i * width / 5, 405, i * width / 5, 495);
  }
}

void drawRed() {
  // red layer
  stroke(255, 0, 0);
  fill(255, 0, 0);
  strokeWeight(5);
  line(0, 42, width, 42);
  strokeWeight(1);
  line(0, 49, width, 49);
  
  strokeWeight(1);
  line(0, 500, width, 500);
}

void draw() {
  background(255);
  switch(colorMode) {
    case 0:
      drawBlack();
      drawRed();
      break;
    case 1:
      drawBlack();
      break;
    case 2:
      drawRed();
      break;
  }
}

void keyPressed() {
  switch(key) {
    case 'r':
    case 'R':
      colorMode = 2;
      break;
    case 'b':
    case 'B':
      colorMode = 1;
      break;
    case 's':
    case 'S':
      if(colorMode == 1) {
        save("blackLayer.bmp");
      } else if(colorMode == 2) {
        save("redLayer.bmp");
      } else {
        save("combined.bmp");
      }
      break;
    default:
      colorMode = 0;
  }
}
