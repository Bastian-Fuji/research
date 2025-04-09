//
// Set constants
const float RATE = 2.2;
const int AM_PIN_1 = 3;
const int AM_PIN_2 = 5;
const int AM_PIN_3 = 6;
const int AM_PIN_4 = 9;
const int LEG_PIN_1 = 10;
const int LEG_PIN_2 = 11;

int cor[6] = {0};

// Define output levels
const float outputLevels[] = {98.96, 110.66, 114.26, 117.40, 120.81, 124.00, 126.12, 128.91, 132.08};

void setup() {
  // Set pin modes
  pinMode(AM_PIN_1, OUTPUT);
  pinMode(AM_PIN_2, OUTPUT);
  pinMode(AM_PIN_3, OUTPUT);
  pinMode(AM_PIN_4, OUTPUT);
  pinMode(LEG_PIN_1, OUTPUT);
  pinMode(LEG_PIN_2, OUTPUT);
  
  // Initialize serial communication
  Serial.begin(9600);
  
  // Initialize the artificial muscles to 0
  setForward(0, 0, 0, 0, 0, 0);
}

void setAM(int v0, int v1, int v2, int v3){
  // Write values to artificial muscle control pins
  analogWrite(AM_PIN_1, v0);
  analogWrite(AM_PIN_2, v1);
  analogWrite(AM_PIN_3, v2);
  analogWrite(AM_PIN_4, v3);
}

void setAMLeg(int v0, int v1){
  // Write values to leg muscle control pins
  analogWrite(LEG_PIN_1, v0);
  analogWrite(LEG_PIN_2, v1);
}

int mapInputToPWM(int input) {
  if (input >= 1 && input <= 9) {
    // Map input 1-9 directly to the output levels array
    return static_cast<int>(outputLevels[input - 1]);
  } else {
    return 0; // Return 0 if input is out of range
  }
}

void setForward(int x, int y, int r, int T, int front_leg, int back_leg){
    // Declare variables for the muscle activation values
    int chestL = 0, chestR = 0, backL = 0, backR = 0;

    // Map the x, y, r, T values to the muscle activations
    if (T == 0) { // r 0	0	r Twist Right
        chestL = 1;
        backR = 1;
    } else if (T == 2) { // 0	r	r	0 Twist Left
        chestR = 1;
        backL = 1;
    } else if (x == 2 && T == 1) { // 0	0	r	r Bending Front
        backL = 1;
        backR = 1;
    } else if (x == 0 && T == 1) { // r	r	0	0 Bending Back
        chestL = 1; 
        chestR = 1;
    } else if (x == 1 && y == 0 && T == 1) { // 0	r	0	r Bend Left
        chestR = 1;
        backR = 1;
    } else if (x == 1 && y == 1 && T == 1) { // 0	0	0	0 Neutral Position
    } else if (x == 1 && y == 2 && T == 1) { // r	0	r	0 Bend Right
        chestL = 1;
        backL = 1;
    }

    // Set the values for the artificial muscles
    r = mapInputToPWM(r);
    setAM(chestL * r, chestR * r, backL * r, backR * r);
    setAMLeg(mapInputToPWM(front_leg), mapInputToPWM(back_leg)); // 
}


// Function to print the coordinates for debugging
void printCoordinates(const int* cor) {
  Serial.println("Printing coordinates ...");
  for (int j = 0; j < 6; j++) {
    Serial.print(cor[j]);
    Serial.print(j < 5 ? ":" : "\n");
  }
  Serial.println("\n");
}

void loop() {
  if (Serial.available() > 0) {
    String inputData = Serial.readStringUntil('\n'); // Read the incoming data until newline
    inputData.trim(); // Remove any whitespace or newline characters

    //Serial.println("Received: " + inputData); // Debug print the received data

    // Check if the received data has the correct length
    if (inputData.length() == 6) {
      for (int j = 0; j < 6; j++) {
        cor[j] = inputData[j] - '0'; // Convert each character to an integer
      }

      // Apply the forward kinematics
      setForward(cor[0], cor[1], cor[2] , cor[3], cor[4], cor[5]); 
    } else {
      //Serial.println("Invalid data length or format.");
    }
  }
}
