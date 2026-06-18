#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GB/T 20438国家标准PDF内容提取脚本
用于提取PDF前10页的关键信息
"""

import pdfplumber
import os

def extract_pdf_info(pdf_path, pages_to_read=10):
    """提取PDF文件的关键信息"""
    result = {
        "文件名": os.path.basename(pdf_path),
        "页数": 0,
        "内容": [],
        "表格": []
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            result["页数"] = len(pdf.pages)

            # 读取前N页
            for i, page in enumerate(pdf.pages[:pages_to_read]):
                page_info = {
                    "页码": i + 1,
                    "文本": "",
                    "表格": []
                }

                # 提取文本
                text = page.extract_text()
                if text:
                    page_info["文本"] = text

                # 提取表格
                tables = page.extract_tables()
                if tables:
                    for j, table in enumerate(tables):
                        if table:
                            page_info["表格"].append({
                                "表格序号": j + 1,
                                "内容": table
                            })

                result["内容"].append(page_info)

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
        print(f"\n--- 第 {page['页码']} 页 ---")

        # 打印文本（限制长度）
        text = page["文本"]
        if text:
            # 只打印前2000字符
            if len(text) > 2000:
                print(text[:2000])
                print(f"... [已截断，原文共 {len(text)} 字符]")
            else:
                print(text)

        # 打印表格信息
        if page["表格"]:
            print(f"\n[本页包含 {len(page['表格'])} 个表格]")
            for table_info in page["表格"]:
                print(f"表格 {table_info['表格序号']}:")
                table = table_info["内容"]
                for row in table[:10]:  # 只打印前10行
                    print(f"  {row}")
                if len(table) > 10:
                    print(f"  ... [表格共 {len(table)} 行]")

def main():
    pdf_dir = "d:/Code/FunctionalSafety/IEC61508国标_GB-T20438/"
    pdf_files = [
        "GBT20438.1-2006.pdf",
        "GBT20438.2-2006.pdf",
        "GBT20438.3-2006.pdf",
        "GBT20438.4-2006.pdf",
        "GBT20438.5-2006.pdf",
        "GBT20438.6-2006.pdf",
        "GBT20438.7-2006.pdf"
    ]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        if os.path.exists(pdf_path):
            print(f"\n\n{'=' * 100}")
            print(f"正在处理: {pdf_file}")
            print("=" * 100)

            result = extract_pdf_info(pdf_path, pages_to_read=10)
            print_summary(result)
        else:
            print(f"文件不存在: {pdf_path}")

if __name__ == "__main__":
    main()
