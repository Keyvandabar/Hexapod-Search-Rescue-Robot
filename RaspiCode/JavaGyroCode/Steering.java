class Steering {
    private static final int STEERING_CENTER = 1400;
    private static final int STEERING_RIGHT_MAX = 1130;
    private static final int STEERING_LEFT_MAX = 1670;

    private static final int GPIO_PINX = 22;
    private static final int PINY = 23;

    public native int turnWheels(int pin, int pulseWidth);
    public native int turnWheelsY(int pinY, int pulseWidthY);

    static {
        System.loadLibrary("steering");
	//System.loadLibrary("steeringY");
    }	
	
    public static void main(String args[]) {
        Steering steering = new Steering();
	//Steering steeringY = new Steering();
        try {
            steering.turnWheels(GPIO_PINX, STEERING_CENTER);
            Thread.sleep(3_000);
            steering.turnWheels(GPIO_PINX, STEERING_RIGHT_MAX);
            Thread.sleep(3_000);
            steering.turnWheels(GPIO_PINX, STEERING_LEFT_MAX);
            Thread.sleep(3_000);
            steering.turnWheelsY(PINY, STEERING_CENTER);
            Thread.sleep(3_000);
            steering.turnWheelsY(PINY, STEERING_RIGHT_MAX);
            Thread.sleep(3_000);
            steering.turnWheelsY(PINY, STEERING_LEFT_MAX);
            Thread.sleep(3_000);
            steering.testFullRange();
	    //steeringY.testFullRange();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
	
    void testFullRange() {
        try {
            boolean goingDown = true;
            int x = STEERING_LEFT_MAX;
	    int y = STEERING_LEFT_MAX;
            while (true) {
                turnWheels(GPIO_PINX, x);
		Thread.sleep(20);
		turnWheelsY(PINY, y);
		Thread.sleep(20);
		
                if (goingDown) {
                    x-=5;
		    y-=5;
                } else {
                    x+=5;
		    y+=5;	
                }
                if (x < STEERING_RIGHT_MAX) { goingDown = false; }
                if (x > STEERING_LEFT_MAX) { goingDown = true; }
		if (y < STEERING_RIGHT_MAX) { goingDown = false; }
                if (y > STEERING_LEFT_MAX) { goingDown = true; }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}