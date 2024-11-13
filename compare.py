import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def read_img(path_1, path_2):
    # 读取图片
    img1 = cv2.imread(path_1)
    img2 = cv2.imread(path_2)
    
    # 确保两张图片尺寸相同
    if img1.shape != img2.shape:
        return None, None
    return img1.copy(), img2.copy()


#assert img1.shape == img2.shape, "两张图片尺寸不一致"

def pre_process(img1, img2):
    # 转换为灰度图
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)




    #cv2.imshow('1',gray1)
    #cv2.imshow('2',gray2)
    #cv2.waitKey(0)
    
    return gray1, gray2
    
def judge_diff(gray1,gray2):


    (score,diff) = ssim(gray1,gray2,full = True)
    
    if score < 0.5:
        return -1, None

    diff2 = (diff *255).astype("uint8")

    diff2 = cv2.convertScaleAbs(diff2)

    print("SSIM:{}".format(score))
    #cv2.imshow('Difference2', diff2)
    #cv2.waitKey(0)
    
    return score, diff2

def find_diff(img1, img2):
    diff = cv2.absdiff(img1, img2)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Difference2', diff)
    #cv2.waitKey(0)
    return gray_diff

def draw_contours(diff2,img1,img2):


    # 阈值处理
    _, thresh = cv2.threshold(diff2, 30, 255, cv2.THRESH_BINARY)

    # 找到差异区域
    contours, hierarchy  = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(hierarchy)
    height, width = diff2.shape
    root_contour = -2

    # 在原图上标记出差异点
    for i, contour in enumerate(contours):
        
        # 计算轮廓的边界框
        x, y, w, h = cv2.boundingRect(contour)
        print(x,y,w,h)
        if w == width and h == height:
            root_contour = i
            continue
        
        current_hierarchy = hierarchy[0][i]
        # 获取父轮廓的索引
        parent_index = current_hierarchy[3]
        
        # 如果父轮廓索引非-1，则说明当前轮廓是子轮廓
        if parent_index != -1 and parent_index != root_contour:
            # 获取父轮廓
            parent_contour = contours[parent_index]
            print(f"轮廓 {i} 被轮廓 {parent_index} 包含。")
            continue
        
        # 在原图上画出边界框
        cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 2)


    
    return img1, img2


def main():
    img1, img2 = read_img('image1.jpg','image2.jpg')
    if img1 is None:
        return "img size file"
    gray1, gray2 = pre_process(img1, img2)
    score, diff2 = judge_diff(gray1,gray2)
    if score == -1:
        return "img not similar"
    diff = find_diff(img1, img2)
    finalimg1, finalimg2 = draw_contours(diff, img1, img2)
    # 显示结果
    cv2.imshow('Differences in Image 1', finalimg1)
    cv2.imshow('Differences in Image 2', finalimg2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def main_app(path1, path2):
    print(path1,path2)
    img1, img2 = read_img(path1,path2)
    if img1 is None:
        return "img size file", None, None
    gray1, gray2 = pre_process(img1.copy(), img2.copy())
    score, diff2 = judge_diff(gray1.copy(),gray2.copy())
    if score == -1:
        return "img not similar",None, None
    diff = find_diff(img1.copy(), img2.copy())
    finalimg1, finalimg2 = draw_contours(diff, img1, img2)
    # 显示结果
    finalimg1 = cv2.cvtColor(finalimg1, cv2.COLOR_BGR2RGB)
    finalimg2 = cv2.cvtColor(finalimg2, cv2.COLOR_BGR2RGB)
    return "success", finalimg1, finalimg2
    