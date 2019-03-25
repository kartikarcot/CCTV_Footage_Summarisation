import cv2
import numpy as np
import blend

# open input video
capVid = cv2.VideoCapture('DubRun.mp4')
cap1 = cv2.VideoCapture('masked1.avi')
cap2 = cv2.VideoCapture('masked2.avi')
# cap3 = cv2.VideoCapture('masked3.avi')
# cap4 = cv2.VideoCapture('masked4.avi')
capBG = cv2.VideoCapture('DubBG.avi')

frame_width = int(capVid.get(3))
frame_height = int(capVid.get(4))

video = []
bg = []
mask1 = []
newMask1 = []
mask2 = []
newMask2 = []
mask3 = []
mask4 = []
obj1 = []
obj2 = []
obj3 = []
obj4 = []

while(capVid.isOpened()):
    ret, frame = capVid.read()
    if ret is True:
        video.append(frame)
    else:
        break
        
while(capBG.isOpened()):
    ret, frame = capBG.read()
    if ret is True:
        bg.append(frame)
    else:
        break

while(cap1.isOpened()):
    ret, frame = cap1.read()
    if ret is True:
        mask1.append(frame)
        
        s = np.sum(frame)
        
        if s > 0:
            newMask1.append(frame)
    else:
        break
        
while(cap2.isOpened()):
    ret, frame = cap2.read()
    if ret is True:
        mask2.append(frame)
        
        s = np.sum(frame)
        
        if s > 0:
            newMask1.append(frame)
    else:
        break
        
# while(cap3.isOpened()):
#     ret, frame = cap3.read()
#     if ret is True:
#         mask3.append(frame)
#     else:
#         break
        
# while(cap4.isOpened()):
#     ret, frame = cap4.read()
#     if ret is True:
#         mask4.append(frame)
#     else:
#         break
        
capVid.release()
cap1.release()
cap2.release()
# cap3.release()
# cap4.release()
capBG.release()


print(np.shape(video))
print(np.shape(bg))
print('done')

for i, frame in enumerate(mask1):
    
     # fix JPEG compression issues
    frame[frame>50] = 255
    frame[frame!=255] = 0
    
    event = cv2.bitwise_and(video[i],frame)
    sum = np.sum(event)
    
    if sum > 0:
        obj1.append(event)
        
        
for i, frame in enumerate(mask2):
    
     # fix JPEG compression issues
    frame[frame>50] = 255
    frame[frame!=255] = 0
    
    event = cv2.bitwise_and(video[i],frame)
    sum = np.sum(event)
    
    if sum > 0:
        obj2.append(event)
        
        
for i, frame in enumerate(mask3):
    
     # fix JPEG compression issues
    frame[frame>50] = 255
    frame[frame!=255] = 0
    
    event = cv2.bitwise_and(video[i],frame)
    sum = np.sum(event)
    
    if sum > 0:
        obj3.append(event)
        
        
for i, frame in enumerate(mask4):
    
     # fix JPEG compression issues
    frame[frame>50] = 255
    frame[frame!=255] = 0
    
    event = cv2.bitwise_and(video[i],frame)
    sum = np.sum(event)
    
    if sum > 0:
        obj4.append(event)
        
print('done')

for i, frame in enumerate(obj1):
    
#     mask = frame.copy()
#     mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#     mask[mask!=0] = 255    
#     mask[mask!=255] = 0
#     mask = cv2.bitwise_not(mask)
    
#     mask = np.ones((frame_width, frame_height), dtype=np.uint8)
    
#     mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
#     np.shape(mask)
#     bg[i] = cv2.bitwise_and(bg[i],mask)

#     mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#     bg[i] = cv2.add(bg[i], frame)
#     bg[i] = cv2.seamlessClone(frame, bg[i], mask, (200,200), cv2.NORMAL_CLONE)



#     cv2.imshow('frame',frame)
#     cv2.imshow('bg[i]',bg[i])
#     cv2.imshow('mask',mask)
    
    mask = cv2.cvtColor(newMask1[i], cv2.COLOR_BGR2GRAY)
    
    bg[i] = blend.blend_image(bg[i], frame, mask)
    
#     cv2.imshow('blended',bg[i])
#     cv2.waitKey(0)
#     output = cv2.seamlessClone(src, dst, src_mask, center, cv2.NORMAL_CLONE)
    
cv2.destroyAllWindows()

out = cv2.VideoWriter('FINALNEWBLEND.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame_width,frame_height))

for frame in bg:
    cv2.imshow('frame',frame)
    cv2.waitKey(0)
    out.write(frame)

cv2.destroyAllWindows()
out.release()

cv2.imshow('frame', obj1[i])
cv2.waitKey(0)
cv2.destroyAllWindows()

