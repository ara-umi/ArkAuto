import os
import time

import cv2

from base import MyCv2
from helper.helper import now_time

default_record_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + r"\record"
template_method = cv2.TM_SQDIFF_NORMED


class Template(MyCv2):
    def __init__(self):
        super(Template, self).__init__()
        self._record = self.make_record()

    @staticmethod
    def make_record():
        if not os.path.exists(default_record_dir):
            os.mkdir(default_record_dir)

        record_name = now_time() + ".txt"
        record_path = default_record_dir + "\\" + record_name
        with open(record_path, "a+"):
            pass
        return record_path

    @property
    def record(self):
        return self._record

    def write_record(self, txt, time_on=False):
        with open(self._record, "a+") as f:
            if time_on:
                f.write(f"\n{(time.strftime('%m-%d %H:%M:%S', time.localtime()))}")
            f.write(f"{txt}\n")

    @staticmethod
    def _get_radius(h, w):
        """
        在多处定位时，用圆蒙盖住前一次定位结果，再进行下一次定位
        更好的方法是直接对原图进行蒙盖，可优化
        """
        return (h + w) // 4

    def get_location(self, template_path, image_path, thresh, flags, k, draw=False):
        """
        指定模板和待匹配图片路径进行模板匹配
        default method: cv2.TM_SQDIFF_NORMED
        :param template_path: template path
        :param image_path: image path
        :param thresh: in this method, thresh close to 1 indicates good effect
        :param flags: # 1 for BGR/ 0 for gray
        :param k: knn
        :param draw: show result
        :return: List(tuple) if find else []
        """
        template_name = template_path.split("/")[-1]
        image_name = image_path.split("/")[-1]

        self.write_record(f"\n开始匹配对象：{template_name}", time_on=True)

        template = self.read(template_path, flags)
        image = self.read(image_path, flags)

        shape = template.shape
        h, w = shape[0], shape[1]

        res = cv2.matchTemplate(image, template, method=template_method)

        centers = []

        # 多对象匹配循环
        for i in range(k):
            (min_val, _, min_loc, _) = cv2.minMaxLoc(res)

            if min_val < 1 - thresh:
                # print(min_val)
                radius = self._get_radius(h, w)
                res = cv2.circle(res, min_loc, radius, 1, -1)
                left_top = min_loc
                center = left_top[0] + w // 2, left_top[1] + h // 2
                centers.append(center)
            else:
                break

        if not centers:
            self.write_record(f"定位为空:{template_name}")
            return []
        else:
            self.write_record(f"找到{len(centers)}处匹配 (当前最大匹配数：{k})")
            if k == 1:
                self.write_record(f"匹配位置信息：{centers[0]}")
            else:
                self.write_record(f"匹配位置信息：{centers}")
        # 展示结果
        if draw:
            canvas = image.copy()
            for i, center in enumerate(centers):
                p1 = center[0] - w // 2, center[1] - h // 2
                p2 = center[0] + w // 2, center[1] + h // 2

                canvas = cv2.rectangle(canvas, p1, p2, (0, 255, 0), 2)

                # 这个偏移参数是根据特定字体大小来调的，具体大小可以用cv2.getTextSize()查看
                text_center = center[0] - 8, center[1] + 11

                canvas = cv2.putText(canvas, str(i + 1), text_center, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            self.show_np(canvas, template_name + "->" + image_name)
        return centers


template = Template()

if __name__ == '__main__':
    pass
