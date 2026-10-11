/*
 * The few JNI pieces wristband.c uses, laid out exactly like the standard
 * JNINativeInterface table (jni.h), so no NDK is needed to build it.
 */
#ifndef JNI_MIN_H
#define JNI_MIN_H

typedef unsigned char jboolean;
typedef int jint;
typedef jint jsize;
typedef void *jobject;
typedef jobject jclass;
typedef jobject jstring;

#define JNI_FALSE 0
#define JNI_TRUE 1
#define JNIEXPORT __attribute__((visibility("default")))
#define JNICALL

struct JNINativeInterface;
typedef const struct JNINativeInterface *JNIEnv;

struct JNINativeInterface {
    void *reserved_and_unused[168];      /* slots 0..167 */
    jsize (*GetStringUTFLength)(JNIEnv *, jstring);                       /* 168 */
    const char *(*GetStringUTFChars)(JNIEnv *, jstring, jboolean *);      /* 169 */
    void (*ReleaseStringUTFChars)(JNIEnv *, jstring, const char *);       /* 170 */
};

#endif
