#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GB/T 20438国家标准PDF内容提取脚本
使用PyMuPDF (fitz) 读取扫描版PDF
"""

import fitz  # PyMuPDF
import os

def extract_pdf_info(pdf_path, pages_to_read=15):
    """提取PDF文件的关键信息"""
    result = {
        "文件名": os.path.basename(pdf_path),
        "页数": 0,
        "内容": []
    }

    try:
        doc = fitz.open(pdf_path)
        result["页数"] = len(doc)

        # 读取前N页
        for i in range(min(pages_to_read, len(doc))):
            page = doc[i]
            page_info = {
                "页码": i + 1,
                "文本": ""
            }

            # 提取文本
            text = page.get_text()
            if text:
                page_info["文本"] = text.strip()

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
    print("=" * 80)

    for page in result["内容"]:
        text = page["文本"]
        if text and len(text) > 50:  # 只打印有实质内容的页面
            print(f"\n--- 第 {page['页码']} 页 ---")
            # 打印前1500字符
            if len(text) > 1500:
                print(text[:1500])
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
            print(f"\n\n{'=' * 100}")
            print(f"正在处理: {pdf_file}")
            print(f"描述: {description}")
            print("=" * 100)

            result = extract_pdf_info(pdf_path, pages_to_read=15)
            print_summary(result)
        else:
            print(f"文件不存在: {pdf_path}")

if __name__ == "__main__":
    main()