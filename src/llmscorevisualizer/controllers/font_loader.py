import ctypes
import ctypes.util
import os
import platform
import tkinter.font as tkfont


class FontLoader:
    @staticmethod
    def load_font(font_path: str) -> bool:
        """Loads a font dynamically for the current process/user session on

        Windows (GDI), macOS (CoreText), and Linux (Fontconfig).
        """
        abs_path = os.path.abspath(font_path)
        if not os.path.exists(abs_path):
            print(f"[FontLoader] Missing font file at: {abs_path}")
            return False

        system = platform.system()
        success = False

        # --- 1. WINDOWS (GDI) ---
        if system == "Windows":
            try:
                path_buf = ctypes.create_unicode_buffer(abs_path)
                FR_PRIVATE = 0x10  # Process-scoped font
                res = ctypes.windll.gdi32.AddFontResourceExW(
                    path_buf, FR_PRIVATE, 0
                )
                success = res > 0
            except Exception as e:
                print(f"[FontLoader] Windows error: {e}")
                return False

        # --- 2. MACOS (CoreText) ---
        elif system == "Darwin":
            try:
                cf_lib = ctypes.util.find_library("CoreFoundation")
                ct_lib = ctypes.util.find_library("CoreText")
                if not cf_lib or not ct_lib:
                    return False

                cf = ctypes.cdll.LoadLibrary(cf_lib)
                ct = ctypes.cdll.LoadLibrary(ct_lib)

                # Set explicit 64-bit function signatures
                cf.CFStringCreateWithCString.argtypes = [
                    ctypes.c_void_p,
                    ctypes.c_char_p,
                    ctypes.c_uint32,
                ]
                cf.CFStringCreateWithCString.restype = ctypes.c_void_p

                cf.CFURLCreateWithFileSystemPath.argtypes = [
                    ctypes.c_void_p,
                    ctypes.c_void_p,
                    ctypes.c_long,
                    ctypes.c_bool,
                ]
                cf.CFURLCreateWithFileSystemPath.restype = ctypes.c_void_p

                ct.CTFontManagerRegisterFontsForURL.argtypes = [
                    ctypes.c_void_p,
                    ctypes.c_uint32,
                    ctypes.c_void_p,
                ]
                ct.CTFontManagerRegisterFontsForURL.restype = ctypes.c_bool

                cf.CFRelease.argtypes = [ctypes.c_void_p]

                abs_bytes = abs_path.encode("utf-8")
                cf_str = cf.CFStringCreateWithCString(
                    None, abs_bytes, 0x08000100
                )
                if not cf_str:
                    return False

                cf_url = cf.CFURLCreateWithFileSystemPath(
                    None, cf_str, 0, False
                )
                cf.CFRelease(cf_str)
                if not cf_url:
                    return False

                # kCTFontManagerScopeUser = 2 (Exposes font to Cocoa/Tkinter enumerator)
                kCTFontManagerScopeUser = 2
                success = ct.CTFontManagerRegisterFontsForURL(
                    cf_url, kCTFontManagerScopeUser, None
                )
                cf.CFRelease(cf_url)
            except Exception as e:
                print(f"[FontLoader] macOS error: {e}")
                return False

        # --- 3. LINUX (Fontconfig) ---
        elif system == "Linux":
            try:
                fc_lib_path = ctypes.util.find_library("fontconfig")
                if not fc_lib_path:
                    # Fallback lookup for common Linux distribution paths
                    fc_lib_path = "libfontconfig.so.1"

                fc = ctypes.cdll.LoadLibrary(fc_lib_path)

                # FcBool FcConfigAppFontAddFile(FcConfig *config, const FcChar8 *file)
                fc.FcConfigAppFontAddFile.argtypes = [
                    ctypes.c_void_p,
                    ctypes.c_char_p,
                ]
                fc.FcConfigAppFontAddFile.restype = ctypes.c_bool

                # Passing None/NULL as FcConfig uses the current default Fontconfig instance
                abs_bytes = abs_path.encode("utf-8")
                success = fc.FcConfigAppFontAddFile(None, abs_bytes)
            except Exception as e:
                print(f"[FontLoader] Linux error: {e}")
                return False

        # Refresh Tkinter internal font cache so newly added fonts show up in tkfont.families()
        if success:
            _ = tkfont.families()

        return success