import subprocess
import sys
import importlib
from typing import List, Tuple
import logging


def deps_check(packages: str|List[str]|Tuple[str], install:bool=True):
    """Check whether the specified packages are installed, and optionally install them if not.

    Args:
        packages (str | List[str] | Tuple[str]): Package names to check.
        install (bool, optional): True to install if not installed. Defaults to True.
    """
    if isinstance(packages, str):
        packages = [packages]
    for pkg in packages:
        try:
            importlib.import_module(pkg)
            logging.info(f"[✔] 已安装: {pkg}")
        except ImportError:
            logging.warning(f"[⚠] 未检测到包 {pkg}，正在安装...")
            if install:
                try:
                    subprocess.check_call([
                        sys.executable, "-m", "pip", "install",
                        "-i", "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple",
                        pkg
                    ])
                    logging.info(f"[✔] 安装完成: {pkg}")
                except subprocess.CalledProcessError as e:
                    logging.error(f"[❌] 安装失败: {pkg}, 错误: {e}")
            else:
                logging.error(f"[❌] 包 {pkg} 未安装，且未启用自动安装。请手动安装。")

if __name__ == '__main__':
    deps_check(["numpy"], install=True)
