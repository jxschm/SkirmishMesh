# Nach dem Bauen: Bootloader, Partitionstabelle, boot_app0 und Anwendung zu einem
# Image zusammenführen, das der Desktop-Planer in einem Schritt an Adresse 0x0 flasht.
Import("env")  # noqa: F821  (von PlatformIO bereitgestellt)

import os


def merge_bin(source, target, env):
    build_dir = env.subst("$BUILD_DIR")
    out = os.path.join(build_dir, "skirmishmesh-%s.factory.bin" % env.subst("$PIOENV"))
    esptool = os.path.join(env.PioPlatform().get_package_dir("tool-esptoolpy"), "esptool.py")
    args = [
        env.subst("$PYTHONEXE"), esptool,
        "--chip", env.BoardConfig().get("build.mcu", "esp32"),
        "merge_bin", "-o", out, "--flash_mode", "dio", "--flash_size", "keep",
    ]
    for offset, image in env.get("FLASH_EXTRA_IMAGES", []):
        args += [offset, env.subst(image)]
    args += [env.subst("$ESP32_APP_OFFSET"), os.path.join(build_dir, "firmware.bin")]
    env.Execute(" ".join('"%s"' % a for a in args))
    print("Factory-Image:", out)


env.AddPostAction("$BUILD_DIR/firmware.bin", merge_bin)  # noqa: F821
