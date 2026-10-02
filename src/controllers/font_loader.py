import ctypes
import ctypes.util
import os
import platform


class FontLoader:

    @staticmethod
    def load_font(font_path: str) -> bool:
        abs_path = os.path.abspath(font_path)
        if not os.path.exists(abs_path):
            print(f"[FontLoader] Missing font file: {abs_path}")
            return False

        system = platform.system()

        # --- WINDOWS (GDI) ---
        if system == "Windows":
            try:
                path_buf = ctypes.create_unicode_buffer(abs_path)
                FR_PRIVATE = 0x10  # Process-scoped font
                res = ctypes.windll.gdi32.AddFontResourceExW(
                    path_buf, FR_PRIVATE, 0
                )
                return res > 0
            except Exception as e:
                print(f"[FontLoader] Windows error: {e}")
                return False

        # --- MACOS (CoreText) ---
        elif system == "Darwin":
            try:
                cf_lib = ctypes.util.find_library("CoreFoundation")
                ct_lib = ctypes.util.find_library("CoreText")
                if not cf_lib or not ct_lib:
                    return False

                cf = ctypes.cdll.LoadLibrary(cf_lib)
                ct = ctypes.cdll.LoadLibrary(ct_lib)

                # Set 64-bit argument and return types to prevent segmentation faults
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

                # Convert path to CFString -> CFURL
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

                # kCTFontManagerScopeProcess = 1 (Scope strictly to Python process)
                success = ct.CTFontManagerRegisterFontsForURL(cf_url, 1, None)
                cf.CFRelease(cf_url)

                return bool(success)
            except Exception as e:
                print(f"[FontLoader] macOS error: {e}")
                return False

        return True
