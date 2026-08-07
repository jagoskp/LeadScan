plugins {
    id("com.android.application")
    id("kotlin-android")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

project.layout.buildDirectory.set(file("${rootProject.projectDir.parentFile}/build/app"))

android {
    namespace = "com.example.leadscan_mobile"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    defaultConfig {
        applicationId = "com.example.leadscan_mobile"
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("debug")
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

flutter {
    source = "../.."
}

tasks.whenTaskAdded {
    if (name == "assembleDebug") {
        doLast {
            val src = file("${project.layout.buildDirectory.get()}/outputs/apk/debug/app-debug.apk")
            val dstDir = file("${rootProject.projectDir.parentFile}/build/app/outputs/flutter-apk")
            if (src.exists()) {
                dstDir.mkdirs()
                src.copyTo(file("${dstDir}/app-debug.apk"), overwrite = true)
            }
        }
    }
    if (name == "assembleRelease") {
        doLast {
            val src = file("${project.layout.buildDirectory.get()}/outputs/apk/release/app-release.apk")
            val dstDir = file("${rootProject.projectDir.parentFile}/build/app/outputs/flutter-apk")
            if (src.exists()) {
                dstDir.mkdirs()
                src.copyTo(file("${dstDir}/app-release.apk"), overwrite = true)
            }
        }
    }
}
