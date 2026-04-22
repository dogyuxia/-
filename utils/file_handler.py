import hashlib
import os.path
from typing import Optional
from xml.dom.minidom import Document

from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader

from utils.logger_handler import logger


# 计算文件的MD5哈希值
def get_file_md5_hex(filepath : str)->Optional[str]:
    if not os.path.exists(filepath):
        print(f"错误：文件 {filepath} 不存在")
        return None
    if not os.path.isfile(filepath):
        print(f"错误：{filepath} 不是有效文件")
        return None

    md5_obj = hashlib.md5()
    chunk_size = 4096

    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)

                """
                chunk = f.read(chunk_size)
                while True:
                    md5_obj.update(chunk)
                    chunk = f.read(chunk_size)
                """
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"[md5]计算shibai{str(e)}")



def listdir_with_allowed_type(path:str , allowed_types:tuple[str]):
    file = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]错误")
        return tuple(file)
    for f in os.listdir(path):
        if f.endswith(allowed_types):
            file.append(os.path.join(path,f))

    return tuple(file)

def pdf_loader(filepath:str,passwd = None) -> list[Document]:
    return PyPDFLoader(filepath,passwd).load()

def txt_loader(filepath:str) -> list[Document]:
    return TextLoader(filepath,encoding="UTF-8").load()
def csv_loader(filepath: str, source_column=None, encoding='utf-8', csv_args=None) -> list[Document]:
    loader = CSVLoader(
        filepath,
        source_column=source_column,
        encoding=encoding,
        csv_args=csv_args,
    )
    return loader.load()



