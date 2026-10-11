package org.barsides.rideallday;

/**
 * Wristband validation. The night crew moved the check into native code
 * so nobody could read it in a decompiler.
 */
final class Gate {

    static {
        System.loadLibrary("wristband");
    }

    private Gate() {
    }

    /** True when the code printed on the wristband is genuine. */
    static native boolean scan(String code);
}
