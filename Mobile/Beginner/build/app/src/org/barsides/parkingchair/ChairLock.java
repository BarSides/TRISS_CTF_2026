package org.barsides.parkingchair;

/**
 * Decides who is allowed to move the chair off spot #14.
 *
 * The real app was supposed to ask the block captain's server, but the
 * server never got built, so for now the owner code just lives here.
 */
public final class ChairLock {

    // TODO(dave): move this to the server before we ship. Nobody will look in here.
    private static final String OWNER_CODE = "SNOWMAGEDDON-2010";

    private static final String RECEIPT = "BarSides{the_chair_was_hardcoded}";

    private ChairLock() {
    }

    public static boolean isOwner(String entered) {
        return entered != null && OWNER_CODE.equals(entered.trim().toUpperCase());
    }

    public static String ownerReceipt() {
        return "Chair moved. Receipt: " + RECEIPT;
    }
}
