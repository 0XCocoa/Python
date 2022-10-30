from pathlib import Path
from datetime import datetime

import sys
sys.path.append('D:\Tools\VS Code\Python')
from _formal.Tkinter import choose_path

class Files:
    def __init__(self, target_path=None):
        self._oris = []
        self._files = []
        if target_path: self.get_files(target_path)

    def get_files(self, path):
        if (path := Path(path)) not in self._oris and path.is_dir(): 
            self._oris.append(path)
        self._files += [{
            'tag':None,
            'Path':file, 
            'path':str(file), 
            'size':f'{round(file.stat().st_size/1024/1024, 1)} MB', 
            'mtime':(mtime := datetime.fromtimestamp(file.stat().st_mtime)), 
            'time':f'{mtime.year}-{mtime.month}-{mtime.day}', 
            'name':file.name
        } for file in path.glob('**/*') if file.is_file()]

    def append_file(self, path, tag=None):
        path = Path(path)
        self._files += [{
            'tag':tag, 
            'Path':path, 
            'path':str(path), 
            'size':f'{round(path.stat().st_size/1024/1024, 2)} MB', 
            'mtime':(mtime := datetime.fromtimestamp(path.stat().st_mtime)), 
            'time':f'{mtime.year}-{mtime.month}-{mtime.day}', 
            'name':path.name
        }]

    def exclude(self, path):
        if (path := Path(path)).is_dir and path in self._oris:
            self._oris.remove(path)
        self._files = [file for file in self._files if str(path) not in str(file['Path'])]
    
    def rglob(self, dir=None):
        self._files = []
        for ori in ([dir] if dir and (dir := Path(dir)).is_dir() else self._oris):
            self.get_files(ori)

    

    def sort_bySuffix(self):
        import shutil
        deleted = self._oris[0]/'deleted'
        if not deleted.exists():
            deleted.mkdir()
        for file in self._files:
            dir = self._oris[0]/file['Path'].suffix
            if not dir.exists():
                dir.mkdir()
            shutil.copy(file['Path'], deleted)
            file['Path'].replace(dir/file['Path'].name)

        self.rglob()
        self.exclude(deleted)
            
    def change_toPng(self, ori='.bmp', end='.png'):
        from PIL import Image
        if ori[0] != '.':
            ori = '.' + ori
        if end[0] != '.':
            end = '.' + end
        dir = self._oris[0]/'deleted'
        if self._files and not dir.exists():
            dir.mkdir()
        for file in self._files:
            if file['Path'].suffix == ori:
                Image.open(file['Path']).save(file['Path'].with_suffix(end))
                file['Path'].replace(dir/file['Path'].name)
        
        self.rglob()
        self.exclude(dir)

    def img_info(self, img_path=None):
        if not img_path:
            return
        import re
        import exifread
        with open(str(img_path),'rb') as f:
            contents = exifread.process_file(f)
            for key in contents:
                if key == "GPS GPSLongitude":
                    print("经度: ", contents[key],contents['GPS GPSLatitudeRef'])
                    print("纬度: ",contents['GPS GPSLatitude'],contents['GPS GPSLongitudeRef'])
                    print("高度基准: ",contents['GPS GPSAltitudeRef'])
                    print("海拔高度: ",contents['GPS GPSAltitude'])
                if re.match('Image Make', key):
                    print('品牌信息: ' , contents[key])
                if re.match('Image Model', key):
                    print('具体型号: ' , contents[key])
                if re.match('Image DateTime', key):
                    print('拍摄时间: ' , contents[key])
                if re.match('EXIF ExifImageWidth', key):
                    print('照片尺寸: ' , contents[key],'*',contents['EXIF ExifImageLength'])
                if re.match('Image ImageDescription',key):
                    print('图像描述: ' , contents[key])

    def rename(self):
        items = {}
        for file in self._files:
            if file['time'] not in items:
                items[file['time']] = 0
            items[file['time']] += 1
            file['Path'].rename(file['Path'].with_stem(f'{file["time"]} {str(items[file["time"]]).rjust(2, "0")}'))
