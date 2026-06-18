#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GB/T 20438国家标准PDF内容提取脚本
尝试多种方法提取PDF内容
"""

import fitz  # PyMuPDF
import os

def extract_with_ocr(pdf_path, start_page=0, end_page=15):
    """使用PyMuPDF的OCR功能提取文本"""
    result = {
        "文件名": os.path.basename(pdf_path),
        "页数": 0,
        "内容": []
    }

    try:
        doc = fitz.open(pdf_path)
        result["页数"] = len(doc)

        for page_num in range(start_page, min(end_page, len(doc))):
            page = doc[page_num]

            # 方法1: 直接提取文本
            text = page.get_text()

            # 方法2: 提取文本块
            if not text or len(text.strip()) < 50:
                blocks = page.get_text("blocks")
                if blocks:
                    text = "\n".join([b[4] for b in blocks if len(b) > 4])

            # 方法3: 使用getTextDict
            if not text or len(text.strip()) < 50:
                text_dict = page.get_text("dict")
                extracted = []
                for block in text_dict.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                extracted.append(span["text"])
                if extracted:
                    text = " ".join(extracted)

            # 方法4: 提取图片并检查尺寸
            if not text or len(text.strip()) < 50:
                images = page.get_images(full=True)
                if images:
                    text = f"[本页包含 {len(images)} 张图片，需要OCR处理]"

            page_info = {
                "页码": page_num + 1,
                "文本": text.strip() if text else "",
                "图片数": len(page.get_images()) if page.get_images() else 0
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
            print(f"\n--- 第 {page['页码']} 页 (图片数: {page['图片数']}) ---")
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

    for pdf_file, description in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        if os.path.exists(pdf_path):
            print(f"\n\n{'#' * 100}")
            print(f"# 文件: {pdf_file}")
            print(f"# 描述: {description}")
            print("#" * 100)

            result = extract_with_ocr(pdf_path, start_page=0, end_page=20)
            print_summary(result)
        else:
            print(f"文件不存在: {pdf_path}")

if __name__ == "__main__":
    main()