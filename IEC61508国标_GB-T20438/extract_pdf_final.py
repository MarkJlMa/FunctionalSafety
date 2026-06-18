#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GB/T 20438国家标准PDF内容提取脚本
使用pdf2image和pytesseract进行OCR
"""

import os
import sys

# 检查是否有可用的OCR
USE_OCR = False
try:
    import pytesseract
    from pdf2image import convert_from_path

    # 检查tesseract是否可用
    result = os.popen('tesseract --version 2>&1').read()
    if 'tesseract' in result.lower() or 'Tesseract' in result:
        USE_OCR = True
        print("Tesseract OCR 可用")
    else:
        print("Tesseract OCR 未安装，将仅提取可提取的文本")
except ImportError as e:
    print(f"缺少OCR库: {e}")

import pdfplumber

def extract_pdf_content(pdf_path, pages_to_read=15):
    """提取PDF内容"""
    result = {
        "文件名": os.path.basename(pdf_path),
        "页数": 0,
        "内容": [],
        "表格": []
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            result["页数"] = len(pdf.pages)

            for i, page in enumerate(pdf.pages[:pages_to_read]):
                page_info = {
                    "页码": i + 1,
                    "文本": "",
                    "图片数": 0
                }

                # 提取文本
                text = page.extract_text()
                if text and len(text.strip()) > 0:
                    page_info["文本"] = text.strip()

                # 检查图片数量
                images = page.images if hasattr(page, 'images') else []
                page_info["图片数"] = len(images)

                # 提取表格
                tables = page.extract_tables()
                if tables:
                    for j, table in enumerate(tables):
                        if table and len(table) > 0:
                            result["表格"].append({
                                "页码": i + 1,
                                "表格序号": j + 1,
                                "内容": table
                            })

                result["内容"].append(page_info)

    except Exception as e:
        result["错误"] = str(e)

    return result

def print_summary(result, is_scanned=False):
    """打印提取的内容摘要"""
    print("=" * 80)
    print(f"文件: {result['文件名']}")
    print(f"总页数: {result['页数']}")
    if "错误" in result:
        print(f"错误: {result['错误']}")
    print("=" * 80)

    # 检查是否是扫描版PDF
    total_text = sum(len(p["文本"]) for p in result["内容"])
    total_images = sum(p["图片数"] for p in result["内容"])

    print(f"\n统计信息:")
    print(f"  - 提取的文本总字符数: {total_text}")
    print(f"  - 图片总数: {total_images}")

    if total_text < 100 and total_images > 0:
        print("\n[警告] 此PDF可能是扫描版，文本内容较少，建议使用OCR处理")

    # 打印有文本内容的页面
    for page in result["内容"]:
        if page["文本"] and len(page["文本"]) > 50:
            print(f"\n--- 第 {page['页码']} 页 ---")
            text = page["文本"]
            if len(text) > 1500:
                print(text[:1500])
                print(f"\n... [已截断，原文共 {len(text)} 字符]")
            else:
                print(text)

    # 打印表格
    if result["表格"]:
        print(f"\n\n共发现 {len(result['表格'])} 个表格:")
        for t in result["表格"][:5]:  # 只打印前5个表格
            print(f"\n表格 {t['表格序号']} (第{t['页码']}页):")
            table = t["内容"]
            for row in table[:10]:  # 只打印前10行
                print(f"  {row}")
            if len(table) > 10:
                print(f"  ... [表格共 {len(table)} 行]")

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

            result = extract_pdf_content(pdf_path, pages_to_read=20)
            print_summary(result)
            all_results[pdf_file] = result
        else:
            print(f"文件不存在: {pdf_path}")

    return all_results

if __name__ == "__main__":
    main()