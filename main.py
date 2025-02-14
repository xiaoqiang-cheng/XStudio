import os

def main():
    system_platform = platform.platform()
    dirname = os.path.dirname(GuiCoreLib.__file__)
    if "Windows" in system_platform:
        import ctypes
        plugin_path = os.path.join(dirname,'plugins', 'platforms')
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
    elif "Linux" in system_platform:
        plugin_path = os.path.join(dirname,'Qt', 'plugins', 'platforms')
    else:
        plugin_path = ""

    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    _log_sys_init()
    obj = Controller()
    signal.signal(signal.SIGINT, obj.sigint_handler)
    obj.run()





if __name__=="__main__":
    main()