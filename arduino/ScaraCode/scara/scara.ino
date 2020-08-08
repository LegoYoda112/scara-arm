#include <AccelStepper.h>
#define ACTIVE = 7

// Define a stepper and the pins it will use
AccelStepper stepperA(1, 3, 4); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
AccelStepper stepperB(1, 5, 6); 

boolean moving = false;

void setup()
{  
  Serial.begin(9600);
  Serial.println("Scara starting");
  Serial.println("ok");
  
  // Change these to suit your stepper if you want
  stepperA.setMaxSpeed(500);
  stepperA.setAcceleration(200);
  stepperB.setMaxSpeed(500);
  stepperB.setAcceleration(200);
}

void loop()
{
    // If at the end of travel go to the other end
    if (moving && (stepperA.distanceToGo() == 0) && (stepperB.distanceToGo() == 0)){
      Serial.println("ok");
      moving = false;
    }

    if(Serial.available() > 0){
      Serial.println("Started parsing");
      char c = 'a';
      int inputIndex = 0;
      String inputString = "";
      String inputArgs[5];
      Serial.print("Receiving string: ");
      while(c != '\n'){
        delay(1);
        if(Serial.available() > 0) {
          c = Serial.read();
          inputString += c;
          Serial.print(c);
        }
        
        if(c == ' '){
          inputString[inputString.length()-1] = '\0';
          inputArgs[inputIndex] = inputString;
          inputIndex += 1;
          inputString = "";
        }
      }
      inputString[inputString.length()-1] = '\0';
      inputArgs[inputIndex] = inputString;
      
      Serial.println("Finished parsing");
      Serial.print("Command: ");
      Serial.println(inputArgs[0]);


      // ============= PARSE COMMANDS AND ARGUMENTS ================
      String cmd = inputArgs[0];
      
      if(cmd == "M20"){ // Move individual axis
        Serial.println("Performing axis move");
        moving = true;
        Serial.println(moving);
        
        for(int i = 1; i < 5; ++i){
          
          char arg = inputArgs[i][0];
          String valS = inputArgs[i];
          valS.remove(0, 1);
          double val = valS.toDouble();
          
          if(arg == 'A'){
            Serial.print("Moving axis A to: ");
            Serial.println(val);
            stepperA.moveTo(val);
          }else if(arg == 'B'){
            Serial.print("Moving axis B to: ");
            Serial.println(val);
            stepperB.moveTo(val);
          }else if(arg == 'C'){
            Serial.print("Moving axis C to: ");
            Serial.println(val);
            
          }else if(arg == 'D'){
            Serial.print("Moving axis D to: ");
            Serial.println(val);
            
          }
        }
      }

      if(cmd == "M25"){ // Set individual axis max speeds
        Serial.println("Setting axis max speeds");
        moving = true;
        Serial.println(moving);
        
        for(int i = 1; i < 5; ++i){
          
          char arg = inputArgs[i][0];
          String valS = inputArgs[i];
          valS.remove(0, 1);
          double val = valS.toDouble();
          
          if(arg == 'A'){
            Serial.print("Setting axis A max to: ");
            Serial.println(val);
            stepperA.setMaxSpeed(val);
          }else if(arg == 'B'){
            Serial.print("Setting axis B max to: ");
            Serial.println(val);
            stepperB.setMaxSpeed(val);
          }else if(arg == 'C'){
            Serial.print("Setting axis C max to: ");
            Serial.println(val);
            
          }else if(arg == 'D'){
            Serial.print("Setting axis D max to: ");
            Serial.println(val);
            
          }
        }
      }

      if(cmd == "M26"){ // Set individual acceleration
        Serial.println("Setting axis acceleration");
        moving = true;
        Serial.println(moving);
        
        for(int i = 1; i < 5; ++i){
          
          char arg = inputArgs[i][0];
          String valS = inputArgs[i];
          valS.remove(0, 1);
          double val = valS.toDouble();
          
          if(arg == 'A'){
            Serial.print("Setting axis A accel to: ");
            Serial.println(val);
            stepperA.setAcceleration(val);
          }else if(arg == 'B'){
            Serial.print("Setting axis B accel to: ");
            Serial.println(val);
            stepperB.setAcceleration(val);
          }else if(arg == 'C'){
            Serial.print("Setting axis C accel to: ");
            Serial.println(val);
            
          }else if(arg == 'D'){
            Serial.print("Setting axis D accel to: ");
            Serial.println(val);
            
          }
        }
      }
    }

    stepperA.run();
    stepperB.run();
}
