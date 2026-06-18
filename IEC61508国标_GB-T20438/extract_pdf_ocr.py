#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GB/T 20438国家标准PDF内容提取脚本
使用EasyOCR进行中文PDF图片文字识别
"""

import fitz  # PyMuPDF
import easyocr
import numpy as np
from PIL import Image
import os
import io

# 初始化EasyOCR（支持中英文）
print("正在初始化EasyOCR（首次运行需要下载模型，请耐心等待）...")
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
print("EasyOCR初始化完成！")

def pdf_page_to_image(page, dpi=150):
    """将PDF页面转换为PIL Image"""
    mat = fitz.Matrix(dpi/72, dpi/72)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_data))
    return img

def extract_text_with_ocr(page, dpi=150):
    """使用OCR提取页面文字"""
    # 先尝试直接提取文本
    text = page.get_text()
    if text and len(text.strip()) > 50:
        return text.strip()

    # 转换为图片并进行OCR
    img = pdf_page_to_image(page, dpi)
    img_array = np.array(img)

    # 使用EasyOCR识别
    results = reader.readtext(img_array)

    # 组合识别结果
    text_parts = []
    for detection in results:
        text_parts.append(detection[1])

    return " ".join(text_parts)

def extract_pdf_with_ocr(pdf_path, pages_to_read=12):
    """使用OCR提取PDF内容"""
    result = {
        "文件名": os.path.basename(pdf_path),
        "页数": 0,
        "内容": []
    }

    try:
        doc = fitz.open(pdf_path)
        result["页数"] = len(doc)

        for i in range(min(pages_to_read, len(doc))):
            page = doc[i]
            print(f"  处理第 {i+1} 页...")

            text = extract_text_with_ocr(page)

            page_info = {
                "页码": i + 1,
                "文本": text
            }
            result["内容"].append(page_info)

        doc.close()

    except Exception as e:
        result["错误"] = str(e)

    return result

def print_summary(result):
    """打印提取的内容摘要"""
    print("=" * 80)
    print(f"文件: {result['文件名']}")
    print(f"总页数: {result['页数']}")
    if "错误" in result:
        print(f"错误: {result['错误']}")
    print("=" * 80)

    for page in result["内容"]:
        text = page["文本"]
        if text:
            print(f"\n--- 第 {page['页码']} 页 ---")
            if len(text) > 2000:
                print(text[:2000])
                print(f"\n... [已截断，原文共 {len(text)} 字符]")
            else:
                print(text)

def main():
    pdf_dir = "d:/Code/FunctionalSafety/IEC61508国标_GB-T20438/"
    pdf_files = [
        ("GBT20438.1-2006.pdf", "第1部分：一般要求"),
        ("GBT20438.2-2006.pdf", "第2部分：电气/电子/可编程电子安全相关系统的要求"),
        ("GBT20438.3-2006.pdf", "第3部分：软件要求"),
        ("GBT20438.4-2006.pdf", "第4部分：定义和缩略语"),
        ("GBT20438.5-2006.pdf", "第5部分：确定安全完整性等级的方法示例"),
        ("GBT20438.6-2006.pdf", "第6部分：GB/T 20438.2和GB/T 20438.3的应用指南"),
        ("GBT20438.7-2006.pdf", "第7部分：技术和措施概述")
    ]

    all_results = {}

    for pdf_file, description in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        if os.path.exists(pdf_path):
            print(f"\n\n{'#' * 100}")
            print(f"# 文件: {pdf_file}")
            print(f"# 描述: {description}")
            print("#" * 100)

            result = extract_pdf_with_ocr(pdf_path, pages_to_read=12)
            print_summary(result)
            all_results[pdf_file] = result
        else:
            print(f"文件不存在: {pdf_path}")

    return all_results

if __name__ == "__main__":
    main()