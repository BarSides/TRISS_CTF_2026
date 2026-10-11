/*
 * Ride All Day: native wristband check.
 *
 * Built freestanding (no libc, no NDK): the only outside calls are through the
 * JNIEnv function table, so a tiny hand-written jni header is enough.
 * Compiled at -O1 with vectorizing and unrolling off so the loop stays readable
 * in Ghidra.
 */
#include "jni_min.h"

#define CODE_LEN 38

static const unsigned char PUNCH[8] = { 'K', 'E', 'N', 'N', 'Y', 'W', 'D', '!' };

static const unsigned char EXPECTED[CODE_LEN] = {
    0x48, 0x32, 0x03, 0x1b, 0xc5, 0xee, 0x6f, 0x09, 0x09, 0xf2, 0x23, 0x8c, 0x4d,
    0xe6, 0xf7, 0xf2, 0x51, 0x72, 0x83, 0x9c, 0x84, 0x86, 0xf7, 0xc9, 0xd1, 0xf2,
    0x42, 0xac, 0x5d, 0x86, 0x07, 0xa1, 0xc0, 0x4a, 0x23, 0xac, 0x45, 0xc6
};

static unsigned char scramble(unsigned char c, int i)
{
    unsigned char x = c ^ PUNCH[i % 8];
    x = (unsigned char)((x << 3) | (x >> 5));
    return (unsigned char)(x + 17 * i);
}

static int check_band(const char *code, int len)
{
    if (len != CODE_LEN)
        return 0;
    int bad = 0;
    for (int i = 0; i < CODE_LEN; i++)
        bad |= scramble((unsigned char)code[i], i) ^ EXPECTED[i];
    return bad == 0;
}

JNIEXPORT jboolean JNICALL
Java_org_barsides_rideallday_Gate_scan(JNIEnv *env, jclass cls, jstring code)
{
    (void)cls;
    if (code == 0)
        return JNI_FALSE;
    jsize len = (*env)->GetStringUTFLength(env, code);
    const char *chars = (*env)->GetStringUTFChars(env, code, 0);
    if (chars == 0)
        return JNI_FALSE;
    int ok = check_band(chars, len);
    (*env)->ReleaseStringUTFChars(env, code, chars);
    return ok ? JNI_TRUE : JNI_FALSE;
}

JNIEXPORT jint JNICALL JNI_OnLoad(void *vm, void *reserved)
{
    (void)vm;
    (void)reserved;
    return 0x00010006; /* JNI_VERSION_1_6 */
}
