# Face-Haar-Flann-Recognition
use Haar and Flann to do the Recognition<br>
使用Surf方法进行人脸识别："FaceDection - Flann.py"<br>
使用phash方法进行人脸识别："FaceDection - phash.py"<br>
使用神经网络开源库进行人脸识别："FaceDection.py"<br>
使用Haar分类器方法进行人脸检测："FaceDection - Haar.py"<br>
使用动体追踪方法进行人像区域提取："Faild-BackGround.py"<br>

使用的开源库为ageitgey / face_recognition，但是效果极差，不建议尝试，
除了"FaceDection.py"外，其他文件只依赖python3+opencv3.4.1+contrib

功能最完整的是"FaceDection - Flann.py"，运行前先修改好里面的路径：
需要准备face.xml和人脸数据集，人脸数据集规格最好为256*256，只保留下吧到额头的部分，命名为XXX.JPG，注意.JPG大写，人像数据放在一个全英文路径且有访问权限的文件下，然后在程序中
修改
handCascade = cv2.CascadeClassifier('D:\\face.xml')
为face.xml路径

修改：
FileDir = "D:\\FaceLib\\"
为人像文件夹路径。

