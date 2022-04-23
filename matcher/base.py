import cv2


class MyCv2(object):
    def __init__(self):
        pass

    @staticmethod
    def read(path, flags=1):
        """
        读取图片
        :param path:全路径，记得带上后缀
        :param flags: 默认1彩图
        :return: None
        """
        return cv2.imread(path, flags)

    def show_path(self, path, flags=1):
        """
        根据路径直接显示图片
        :param path:全路径，记得带上后缀
        :param flags: 默认1彩图
        :return: None
        """
        image = self.read(path, flags)
        self.show_np(image, title=path)

    @staticmethod
    def show_np(image, title="default"):
        """
        根据np.ndarray展示图片
        :param image: np.ndarray
        :param title: 标题
        :return: None
        """
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    my_cv2 = MyCv2()
    my_cv2.show_path("...")
