import os
import sys
import requests
import pandas as pd
from qqwry import QQwry
from IPy import IP
from datetime import datetime

class IPQueryTool:
    def __init__(self):
        """初始化IP查询工具"""
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.script_dir, "qqwry_lastest.dat")
        self.qqwry = QQwry()
        
    def check_and_download_db(self):
        """检查并下载纯真IP数据库，必要时更新"""
        if not os.path.exists(self.db_path):
            print("未找到纯真IP数据库，开始下载...")
            try:
                self._download_db()
                print("数据库下载完成")
            except Exception as e:
                print(f"下载失败: {e}")
                sys.exit(1)
        else:
            # 检查是否需要更新
            if self._is_db_outdated():
                print("检测到数据库已过期，开始更新...")
                try:
                    # 备份旧数据库
                    self._backup_old_db()
                    self._download_db()
                    print("数据库更新完成")
                except Exception as e:
                    print(f"更新失败: {e}")
                    print("将使用现有数据库继续运行")
            
            self._print_db_info()
            
    def _is_db_outdated(self):
        """检查数据库是否过期（比当前日期早7天以上）"""
        db_mtime = datetime.fromtimestamp(os.path.getmtime(self.db_path))
        days_diff = (datetime.now() - db_mtime).days
        
        print(f"当前数据库更新日期: {db_mtime.strftime('%Y-%m-%d')}")
        print(f"距离现在已有: {days_diff} 天")
        
        return days_diff > 7
                
    def _backup_old_db(self):
        """备份旧的数据库文件"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = os.path.join(self.script_dir, f"qqwry_lastest_{timestamp}.bak")
        os.rename(self.db_path, backup_path)
        print(f"已备份旧数据库到: {backup_path}")
            
    def _download_db(self):
        """下载纯真IP数据库文件"""
        url = "https://raw.githubusercontent.com/out0fmemory/qqwry.dat/master/qqwry_lastest.dat"
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(self.db_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
    def _print_db_info(self):
        """打印数据库版本和发布日期信息"""
        self.qqwry.load_file(self.db_path)
        
        # 获取数据库版本信息
        try:
            # 查询一个保留IP获取版本信息
            _, version = self.qqwry.lookup("127.0.0.1")
            print(f"数据库版本: {version}")
        except Exception as e:
            print(f"获取数据库版本失败: {e}")
        
        # 打印文件修改日期作为更新日期
        db_mtime = datetime.fromtimestamp(os.path.getmtime(self.db_path))
        print(f"数据库更新日期: {db_mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        
    def run(self):
        """运行主程序"""
        self.check_and_download_db()
        
        while True:
            print("\n===== IP地址归属地查询工具 =====")
            print("1. 单个IP查询")
            print("2. 从txt文件批量查询")
            print("3. 从Excel文件批量查询")
            print("4. 退出")
            
            choice = input("请选择查询方式 (1-4): ")
            
            if choice == "1":
                self._query_single_ip()
            elif choice == "2":
                self._query_from_txt()
            elif choice == "3":
                self._query_from_excel()
            elif choice == "4":
                print("感谢使用，再见！")
                break
            else:
                print("无效选择，请重新输入")
    
    def _query_single_ip(self):
        """单个IP查询模式"""
        self.qqwry.load_file(self.db_path)
        
        while True:
            ip = input("\n请输入IP地址 (输入n返回上一级): ").strip()
            
            if ip.lower() == 'n':
                break
                
            try:
                IP(ip)  # 验证IP格式
                result = self.qqwry.lookup(ip)
                
                if result:
                    country, area = result
                    print(f"{ip} 归属地: {country} {area}")
                else:
                    print(f"{ip} 未找到匹配信息")
                    
            except Exception as e:
                print(f"无效的IP地址: {e}")
    
    def _query_from_txt(self):
        """从txt文件批量查询"""
        txt_files = self._get_files_by_extension('.txt')
        
        if not txt_files:
            print("未找到txt文件")
            return
            
        selected_file = self._select_file(txt_files)
        ip_list = self._read_ips_from_file(selected_file)
        
        if not ip_list:
            print("文件中没有有效的IP地址")
            return
            
        results = self._batch_query(ip_list)
        output_path = self._save_to_excel(results, selected_file, "txt")
        
        print(f"查询完成，结果已保存到: {output_path}")
    
    def _query_from_excel(self):
        """从Excel文件批量查询"""
        excel_files = self._get_files_by_extension(('.xlsx', '.xls'))
        
        if not excel_files:
            print("未找到Excel文件")
            return
            
        selected_file = self._select_file(excel_files)
        ip_list = self._read_ips_from_excel(selected_file)
        
        if not ip_list:
            print("文件中没有有效的IP地址")
            return
            
        results = self._batch_query(ip_list)
        output_path = self._save_to_excel(results, selected_file, "excel")
        
        print(f"查询完成，结果已保存到: {output_path}")
    
    def _get_files_by_extension(self, extensions):
        """获取指定扩展名的文件列表"""
        return [f for f in os.listdir(self.script_dir) 
                if f.endswith(extensions) and f != "qqwry_lastest.dat"]
    
    def _select_file(self, files):
        """显示文件列表并让用户选择"""
        print("\n找到以下文件:")
        for i, filename in enumerate(files, 1):
            print(f"{i}. {filename}")
            
        while True:
            try:
                choice = int(input("请选择文件编号: "))
                if 1 <= choice <= len(files):
                    return os.path.join(self.script_dir, files[choice - 1])
                else:
                    print("输入无效，请输入有效的编号")
            except ValueError:
                print("输入无效，请输入数字")
    
    def _read_ips_from_file(self, file_path):
        """从文本文件读取IP地址"""
        try:
            with open(file_path, 'r') as f:
                lines = f.read().splitlines()
            
            valid_ips = []
            invalid_ips = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    IP(line)
                    valid_ips.append(line)
                except Exception:
                    invalid_ips.append(line)
            
            if invalid_ips:
                print(f"发现 {len(invalid_ips)} 个无效IP地址，已自动忽略")
                
            return valid_ips
            
        except Exception as e:
            print(f"读取文件失败: {e}")
            return []
    
    def _read_ips_from_excel(self, file_path):
        """从Excel文件读取IP地址"""
        try:
            df = pd.read_excel(file_path)
            # 尝试查找可能包含IP地址的列
            ip_columns = []
            
            for col in df.columns:
                # 检查列中是否有IP地址格式的数据
                sample = str(df[col].iloc[0]) if not df[col].empty else ""
                if self._is_ip_like(sample):
                    ip_columns.append(col)
            
            if not ip_columns:
                print("未找到包含IP地址的列")
                return []
                
            # 使用第一个包含IP地址的列
            ip_list = df[ip_columns[0]].dropna().astype(str).tolist()
            
            valid_ips = []
            invalid_ips = []
            
            for ip in ip_list:
                try:
                    IP(ip)
                    valid_ips.append(ip)
                except Exception:
                    invalid_ips.append(ip)
            
            if invalid_ips:
                print(f"发现 {len(invalid_ips)} 个无效IP地址，已自动忽略")
                
            return valid_ips
            
        except Exception as e:
            print(f"读取Excel文件失败: {e}")
            return []
    
    def _is_ip_like(self, text):
        """检查文本是否类似IP地址格式"""
        parts = text.split('.')
        return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)
    
    def _batch_query(self, ip_list):
        """批量查询IP地址归属地"""
        self.qqwry.load_file(self.db_path)
        results = []
        
        for ip in ip_list:
            result = self.qqwry.lookup(ip)
            if result:
                country, area = result
                results.append((ip, country, area))
            else:
                results.append((ip, "未找到匹配信息", ""))
        
        return results
    
    def _save_to_excel(self, results, input_file, file_type):
        """保存结果到Excel文件，时间格式为：年月日-时分秒"""
        input_filename = os.path.basename(input_file)
        base_name = os.path.splitext(input_filename)[0]
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_filename = f"{base_name}_result_{timestamp}.xlsx"
        output_path = os.path.join(self.script_dir, output_filename)
        
        df = pd.DataFrame(results, columns=['IP地址', '国家', '地区'])
        
        # 合并国家和地区列
        df['归属地'] = df['国家'] + ' ' + df['地区']
        df = df[['IP地址', '归属地']]  # 只保留两列
        
        try:
            df.to_excel(output_path, index=False)
            return output_path
        except Exception as e:
            print(f"保存Excel文件失败: {e}")
            # 尝试保存为CSV
            csv_path = os.path.splitext(output_path)[0] + '.csv'
            try:
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                return csv_path
            except Exception as e2:
                print(f"保存CSV文件也失败: {e2}")
                return None

if __name__ == "__main__":
    tool = IPQueryTool()
    tool.run()    
