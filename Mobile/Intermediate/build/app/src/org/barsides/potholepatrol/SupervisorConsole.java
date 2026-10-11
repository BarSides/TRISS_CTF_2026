package org.barsides.potholepatrol;

import android.content.Context;

/**
 * Supervisor console: shows the crew's repair authorization once a supervisor
 * signs in. The sign-in screen was cut from v2.3, so nothing calls this yet.
 *
 * The authorization is stored sealed so it doesn't show up in a strings dump.
 */
final class SupervisorConsole {

    private static final byte[] SEALED = {
        1, 51, 51, 7, 44, 54, 72, 48, 41, 53, 56, 89, 92, 94, 94, 38,
        33, 30, 36, 36, 38, 78, 43, 55, 33, 8, 76, 64, 110, 64, 54, 60,
        53, 61, 40, 55, 80
    };

    private SupervisorConsole() {
    }

    static String repairAuthorization(Context ctx) {
        String key = ctx.getString(R.string.dispatch_key);
        return unseal(SEALED, key);
    }

    private static String unseal(byte[] data, String key) {
        char[] out = new char[data.length];
        for (int i = 0; i < data.length; i++) {
            out[i] = (char) ((data[i] ^ key.charAt(i % key.length())) & 0xff);
        }
        return new String(out);
    }
}
